# my-slideshow-theme

PHPカンファレンス香川2025 前夜祭のスライドを参考にした、Marp 用の自作 CSS テーマです。  
白背景・緑枠・アクセントカラー `#6aa84f` を基調とし、5種類のスライドテンプレートを使い分けられます。

## 必要なもの

- [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) 拡張機能
- 本リポジトリを VS Code / Cursor で開く

`.vscode/settings.json` にテーマパスと HTML 有効化が設定済みです。拡張機能を入れたうえで Markdown ファイルを開くと、プレビューでスライドを確認できます。

## プロジェクト構成

```
md_slide_test/
├── README.md
├── .vscode/
│   └── settings.json           # Marp テーマ設定
├── themes/
│   ├── my-slideshow-theme.css      # テーマ本体（@theme: my-slideshow-theme）
│   └── sample-promo.svg        # 告知用サンプル画像
└── my-slides/
    └── 20260819-phpstudy/      # 発表ごとのディレクトリ
        └── 20260819-phpstudy.md
```

スライドは `my-slides/<日付-イベント名>/` に 1 発表 1 ディレクトリで置きます。  
画像など発表専用の素材も、同じディレクトリに入れると管理しやすいです。

## 基本的な使い方

Markdown ファイルの先頭に front matter を書き、スライド区切り `---` の直前にクラス指定を置きます。

```markdown
---
marp: true
theme: my-slideshow-theme
paginate: false
---

<!-- _class: title -->

# 発表タイトル

2026/08/19 イベント名

発表者名
```

| 項目 | 説明 |
|------|------|
| `marp: true` | Marp モードを有効化 |
| `theme: my-slideshow-theme` | 本テーマを適用 |
| `<!-- _class: xxx -->` | スライドにカスタムクラスを指定 |
| `---` | スライドの区切り |

### 新しい発表を追加する

1. `my-slides/` 配下に `YYYYMMDD-イベント名/` を作る
2. その中に同名の `.md` を置く（例: `my-slides/20260819-phpstudy/20260819-phpstudy.md`）
3. 必要ならアイコンやポスターも同じディレクトリに置く
4. front matter に `theme: my-slideshow-theme` を指定する

## テンプレート一覧

| クラス | 用途 | 指定方法 |
|--------|------|----------|
| `title` | タイトルスライド | `<!-- _class: title -->` |
| `message` | 1枚1メッセージ | `<!-- _class: message -->` |
| （なし） | 通常スライド | クラス指定なし |
| `profile` | 自己紹介 | `<!-- _class: profile -->` |
| `promo` | 大きな画像 + 箇条書き（告知・宣伝） | `<!-- _class: promo -->` |

---

### 1. タイトルスライド（`title`）

表紙用。タイトルを中央に大きく表示し、その下にイベント名・発表者名を灰色で配置します。

```markdown
<!-- _class: title -->

# PHPUnitのテスト実行時間も手軽に短くしたいよね<br>〜Pestを利用したアプローチ〜

2026/08/19 PHP勉強会

発表者名
```

- タイトル内で改行する場合は `<br>` を使います
- 2行目以降（日付・イベント名・名前）は通常の段落として書きます

---

### 2. メッセージスライド（`message`）

1枚に1つのメッセージを強調したいときに使います。

**パターン A: メッセージのみ（中央に大きく表示）**

```markdown
<!-- _class: message -->

# テストは、もっと速く回せる
```

**パターン B: 見出し + 本文（例: まとめスライド）**

```markdown
<!-- _class: message -->

# まとめ

Pestを利用して、テスト実行時間を手軽に短くしよう
```

- 見出し（`#`）だけのとき → 中央に大きく表示
- 見出し + 段落があるとき → 見出しは左上（通常スライドと同位置）、本文は中央に表示

---

### 3. 通常スライド（クラス指定なし）

アジェンダや説明スライドなど、一般的な内容向けです。

```markdown
# アジェンダ

1. なぜテスト実行時間が気になるのか
2. Pestでできること
3. 実際のアプローチ
```

```markdown
# なぜテスト実行時間が気になるのか

- CI がボトルネックになっている
  - 待つ時間が積み重なる
- ローカルでもフィードバックが遅い
  - 「手軽に」短くしたい
```

- 見出しは左上に固定され、下に緑の区切り線が入ります
- 入れ子の箇条書きは一段小さく表示されます

---

### 4. 自己紹介スライド（`profile`）

左にアイコン、右に名前・SNS・箇条書きを、スライドの中央に配置します。

```markdown
<!-- _class: profile -->

# 自己紹介

![profile](./my-sns-icon.jpg)

<div class="profile-body">

<p class="profile-name">おさない</p>

<p class="profile-handle">Twitter: @000sak000</p>

- PHPer歴 2年
- マイブーム: カンファレンス遠征 / カンファレンススタッフ
- 今回がカンファレンス初登壇でした

</div>
```

| 要素 | 説明 |
|------|------|
| `![profile](...)` | 左側の正方形アイコン（200×200px） |
| `.profile-name` | 名前（26px・太字） |
| `.profile-handle` | SNS など（26px・太字） |
| 箇条書き | プロフィール詳細（22px） |

HTML を使わない場合は、画像のあとに名前・SNS を段落で書いても同様のレイアウトになります。  
アイコンは発表ディレクトリ直下など、Markdown からの相対パスで指定してください。

---

### 5. 告知・宣伝スライド（`promo`）

イベント告知や画像メインのスライド向けです。  
**タイトル → 箇条書き → 大きな画像 → URL** の順に縦に並びます。

```markdown
<!-- _class: promo -->

# イベントのお知らせ

- PHPカンファレンス香川2025、ぜひご参加ください！

![イベント告知](../../themes/sample-promo.svg)

https://example.com/event
```

- 画像は残りのスペースを使って中央に大きく表示されます
- 最後の行は URL や出典として小さめの文字で表示されます
- サンプル画像は `themes/sample-promo.svg` です。ポスターを使う場合は発表ディレクトリに置いて相対パスを書き換えてください

---

## カスタマイズ

`themes/my-slideshow-theme.css` の CSS 変数を変更すると、全体の見た目を調整できます。

```css
:root {
  --color-accent: #6aa84f;   /* 枠線・区切り線の色（PHPCon関西2025 相当） */
  --color-bg: #ffffff;       /* 背景色 */
  --color-fg: #000000;       /* 文字色 */
  --color-muted: #666666;    /* タイトルスライドの副情報 */
  --slide-pad-x: 56px;       /* 左右余白 */
  --slide-pad-y: 44px;       /* 上下余白 */
  --border-width: 10px;      /* 外枠の太さ */
}
```

`--color-accent` の例:

- `#6aa84f` … PHPCon関西2025 のような緑色
- `#008000` … PHPCon新潟 のような緑色（テーマコメント参照）

アクセントカラーを変えれば、PHP 以外のイベント向けにも流用できます。

## PDF / HTML への書き出し

[Marp CLI](https://github.com/marp-team/marp-cli) を使う場合:

```bash
npx @marp-team/marp-cli \
  --theme themes/my-slideshow-theme.css \
  --html \
  --pdf \
  my-slides/20260819-phpstudy/20260819-phpstudy.md
```

VS Code 上では、Marp 拡張機能の「Export Slide Deck」から PDF / PPTX / HTML を書き出せます。

## サンプル

`my-slides/20260819-phpstudy/20260819-phpstudy.md` に全テンプレートの使用例が入っています。新しいスライドを作るときは、このディレクトリをコピーして編集してください。

## 注意事項

- `profile` テンプレートは HTML を使うため、`.vscode/settings.json` で `"markdown.marp.html": "on"` が必要です
- 画像は Markdown ファイルからの相対パスで指定してください（発表ディレクトリ基準）
- スライドサイズは 1280×720px（16:9）固定です
- front matter では `theme: my-slideshow-theme` を指定してください（CSS 先頭の `@theme` と一致）
