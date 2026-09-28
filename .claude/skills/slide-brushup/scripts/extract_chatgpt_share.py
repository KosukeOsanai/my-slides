#!/usr/bin/env python3
"""
Extract the full conversation text from a chatgpt.com/share/<id> page.

Those pages are a JS-rendered SPA: the initial HTML has no visible message
text, only a <title>. The full conversation is embedded as a devalue/
turbo-stream style flat JSON array (objects are represented as
{"_<keyIndex>": <valueIndex>, ...} pairs referencing other array slots by
index). This script locates that array inside the raw HTML, decodes the
index references recursively, finds the `mapping` node (the conversation
tree), and writes out every user/assistant/tool message in chronological
order.

Usage:
    python3 extract_chatgpt_share.py <url-or-local-html-file> [output.txt]

If given a URL, it is fetched with a normal browser User-Agent (WebFetch
cannot render this page; a plain GET of the raw HTML is what we need here).
If given a local path, that file's content is used as-is (e.g. saved
earlier with `curl -sL -A "Mozilla/5.0 ..." <url> -o page.html`).
"""

import json
import os
import re
import sys
import urllib.request


def fetch_html(source: str) -> str:
    if os.path.exists(source):
        with open(source, encoding="utf-8") as f:
            return f.read()
    req = urllib.request.Request(
        source,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def find_chunk_array(html: str):
    """Find the big devalue/turbo-stream array embedded as a JSON string
    literal inside the page (i.e. a string whose *content* is itself a
    JSON array, double-encoded for safe embedding in a <script> tag)."""
    pattern = re.compile(r'"(?:\\.|[^"\\])*"')
    for m in pattern.finditer(html):
        s = m.group(0)
        if len(s) < 50000:
            continue
        try:
            val = json.loads(s)
        except (ValueError, RecursionError):
            continue
        if not isinstance(val, str) or not val.startswith('[{"_1"'):
            continue
        try:
            chunks = json.loads(val)
        except (ValueError, RecursionError):
            continue
        if isinstance(chunks, list) and chunks:
            return chunks
    return None


def build_resolver(chunks):
    memo = {}
    resolving = set()

    def resolve(idx, depth=0):
        if not isinstance(idx, int):
            return idx
        if idx < 0:
            return None  # devalue sentinel (undefined/NaN/-0/etc.) - not needed here
        if idx in memo:
            return memo[idx]
        if idx in resolving or depth > 120:
            return None  # break cycles / runaway recursion
        resolving.add(idx)
        v = chunks[idx]
        if isinstance(v, dict):
            if v and all(k.startswith("_") and k[1:].lstrip("-").isdigit() for k in v):
                out = {}
                for k, vi in v.items():
                    out[resolve(int(k[1:]), depth + 1)] = resolve(vi, depth + 1)
            else:
                out = v
        elif isinstance(v, list):
            out = [resolve(x, depth + 1) for x in v]
        else:
            out = v
        resolving.discard(idx)
        memo[idx] = out
        return out

    return resolve


def find_mapping(root):
    """DFS for a dict value stored under the key 'mapping' whose entries
    look like conversation nodes (each has a 'message' key)."""
    seen = set()

    def walk(obj, depth=0):
        if depth > 10 or id(obj) in seen:
            return None
        seen.add(id(obj))
        if isinstance(obj, dict):
            if "mapping" in obj and isinstance(obj["mapping"], dict):
                candidate = obj["mapping"]
                if any(
                    isinstance(v, dict) and "message" in v
                    for v in candidate.values()
                ):
                    return candidate
            for v in obj.values():
                found = walk(v, depth + 1)
                if found is not None:
                    return found
        elif isinstance(obj, list):
            for v in obj:
                found = walk(v, depth + 1)
                if found is not None:
                    return found
        return None

    return walk(root)


def extract_messages(mapping):
    out = []
    for node_id, node in mapping.items():
        if not isinstance(node, dict):
            continue
        msg = node.get("message")
        if not isinstance(msg, dict):
            continue
        author = msg.get("author") or {}
        role = author.get("role") if isinstance(author, dict) else None
        content = msg.get("content") or {}
        parts = content.get("parts") if isinstance(content, dict) else None
        if not parts:
            continue
        text = "\n".join(p for p in parts if isinstance(p, str))
        if not text.strip():
            continue
        out.append((msg.get("create_time"), role, text, node_id))
    out.sort(key=lambda x: (x[0] is None, x[0]))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    source = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "chatgpt_conversation.txt"

    html = fetch_html(source)
    chunks = find_chunk_array(html)
    if chunks is None:
        print(
            "Could not find the embedded conversation array. "
            "The page format may have changed, or this isn't a chatgpt.com/share page.",
            file=sys.stderr,
        )
        sys.exit(2)

    resolve = build_resolver(chunks)
    root = resolve(0)
    mapping = find_mapping(root)
    if mapping is None:
        print("Found the data array but no conversation `mapping` inside it.", file=sys.stderr)
        sys.exit(3)

    messages = extract_messages(mapping)
    with open(out_path, "w", encoding="utf-8") as f:
        for create_time, role, text, node_id in messages:
            f.write(f"=== [{role}] time={create_time} id={node_id} ===\n")
            f.write(text)
            f.write("\n\n")

    print(f"Wrote {len(messages)} messages to {out_path}")


if __name__ == "__main__":
    main()
