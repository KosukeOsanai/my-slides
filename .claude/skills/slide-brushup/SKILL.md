---
name: slide-brushup
description: Research a talk topic (ChatGPT share links, blog posts, official docs), then produce a sourced research memo, a timed slide outline, a Marp deck in this repo's my-slideshow-theme style, and matching speaker notes — finishing with an iterative third-party fact-check review loop. Use when creating a new deck under my-slides/, updating an existing one, or when asked to research-and-build slides, write speaker notes, or review a memo/slides/notes for accuracy and consistency.
---

# スライド作成・ブラッシュアップ フロー

`my-slides/<日付-イベント名>/` 配下で、LTスライド一式（調査メモ・スライド・スピーカーノート）を作り、
第三者視点でのファクトチェック・レビューまで通しでやり切るためのフロー。5フェーズで進める。

対象ディレクトリの命名・テーマ規約は [README.md](../../../README.md) を参照（`theme: my-slideshow-theme`、
`title`/`message`/`profile`/`promo`/`references` の5テンプレート、1280×720px固定）。

## フェーズ1: 情報収集 → 調査メモ

1. ユーザーから渡されたソース（ChatGPT共有リンク・ブログ記事URL・公式ドキュメントURL）をすべて確認する。
   - `chatgpt.com/share/...` はJSレンダリングのSPAなので、通常のWebFetchでは**タイトルしか取れない**。
     `scripts/extract_chatgpt_share.py` で会話全文を抽出すること（使い方は後述）。
   - リンクが渡されたら**まず開いて中身を確認する**。無関係な内容だった場合（URLの貼り間違い等）は
     推測で進めず、ユーザーに確認する。
2. 公式ドキュメント等は **WebSearchの要約だけで済ませず、該当ページを直接WebFetchで開いて** 一次情報を確認する。
   WebSearchの集約回答やChatGPTセッション内の引用（`citeturn...`のような出典表記）は、それ自体が
   LLM生成物であり誤り得る。**スライドで口に出す具体的な数値・事例は必ず一次ソースへの直接アクセスで裏取りする。**
3. 発表フォルダ直下に `research-memo.md` を作成し、テーマ別にセクション分けして整理する。末尾に
   「参照した公式ドキュメント」一覧（URLつき）を必ず置く。ChatGPTセッションを情報源にした場合は
   そのURLも別セクションで明記する。

## フェーズ2: 構成案（アウトライン）

1. 同じ `my-slides/` 配下にある既存デッキ（過去の発表）を読み、テンプレートクラスの使い方・トーン・
   1枚あたりの情報量・「枕→本編→まとめ→References→自己紹介→告知」という定番の流れを踏襲する。
2. 発表時間から逆算した「スライド番号｜タイトル｜役割｜目安時間」の表を作り、チャットで一度提示する。
   既存デッキを流用するか／切り口を変えるかで方針が割れる場合は、作り始める前に
   AskUserQuestionで確認する（後戻りが一番コストが高い）。

## フェーズ3: スライド作成

1. フェーズ2の表に沿って `<フォルダ名>/<フォルダ名>.md` を作成・更新する。frontmatterは
   `marp: true` / `theme: my-slideshow-theme` / `paginate: false` を維持する。
2. スライド区切りは `---`。見出し・強調・コードブロックの粒度は既存デッキに合わせる
   （1スライド1メッセージ、コマンドは短いbash/phpブロックで）。
3. 発表用の話す内容は `<!-- -->` のMarpコメントとして各スライドに残す（プレゼンターモードで見える）。
4. 実測値・ベンチマークなど手元でしか分からない値は `○○` / `○分` のように明示的なプレースホルダーにし、
   本物の数値であるかのように書かない。

## フェーズ4: スピーカーノート

1. 同フォルダに `speaker-notes.md` を作成する。冒頭に対象ファイル名・**総スライド枚数**・想定時間を明記する。
2. スライド1枚＝見出し1つで、「（〜m:ss）」の累積タイムスタンプをつけながら通しで書く。
   タイムスタンプは単調増加にし、合計が持ち時間に収まるようにする。
3. プレースホルダーが残っているスライドには「登壇前にTODO: 実測してから差し替える」のように
   明示的に注意書きを入れる。
4. 「n枚目で回収する」のような相互参照を書く場合は、実際のスライド番号と一致しているか後でgrepで確認する
   （フェーズ5でも再チェックする）。

## フェーズ5: 第三者視点レビュー（指摘がなくなるまで繰り返す）

1回のレビューサイクルは以下を**全部**やってから次のサイクルに入る。1周して新規指摘が0件になったら終了。
詳細なチェック項目は [review-checklist.md](review-checklist.md) を参照。

1. 3ファイル（メモ／スライド／スピーカーノート）を通し読みする。
2. スライドに書く・話す予定の**具体的な数値・引用文・URLをすべて洗い出し**、一次ソースへの直接
   WebFetchで裏取りする。WebSearchの集約要約やChatGPTセッションの出典表記だけを根拠にしていたものは
   このタイミングで直接確認し直す。裏が取れなければ**削除するか、確認できた事実に置き換える**。
3. スライド番号の整合性を機械的にチェックする：
   ```bash
   grep -n '^# ' <slides>.md            # 見出し一覧（bashコードブロック内の # コメント行が
                                         # 誤って混ざっていないか目視で除外すること）
   grep -c '^## [0-9]' speaker-notes.md  # ノート側の枚数と一致するか
   grep -n '枚目' speaker-notes.md       # 相互参照が実際のスライド番号と合っているか
   ```
4. 新しく足した内容が、デッキ全体の核となる主張と矛盾していないか確認する
   （例：「コードを変えなくていい」がテーマなのに、新しいスライドが暗黙に書き換えを要求する機能を
   同列に紹介していないか）。矛盾があれば注記を足して橋渡しする。
5. 削除・統合・追加したスライドの旧タイトルが、他の2ファイルに残っていないか grep する。
6. 画像・相対パスの参照先が実在するか確認する（`ls` で存在確認）。
7. 見つけた指摘点はその場で修正し、要約を短く報告してから次のサイクルへ進む。

## 補助スクリプト

- `scripts/extract_chatgpt_share.py <URL または 保存済みHTMLファイル> [出力txt]`
  `chatgpt.com/share/...` ページはNext.js的なturbo-stream/devalue形式でJS側にのみ会話データを
  埋め込んでいる。このスクリプトは生HTMLを取得し、埋め込まれた配列参照形式のJSONをデコードして、
  発言者・時刻順に並んだプレーンテキストの会話ログを書き出す。まず `curl` で保存してから渡してもよいし、
  URLを直接渡してもよい（その場合はブラウザUAで自前フェッチする）。
