---
marp: true
theme: my-slideshow-theme
paginate: false
style: |
  /* 差し色を PHPカンファレンス新潟2026 公式サイト（--color-primary: #005aa5）に合わせる */
  :root { --color-accent: #005aa5; --color-code-bg: #f0f8ff; }
  th, td { border-bottom-color: #cce4f7; }
  th { white-space: nowrap; }
  td:last-child { white-space: nowrap; }
  td:first-child, td:nth-child(2) { white-space: nowrap; }
  .tag {
    display: inline-block;
    margin-left: 6px;
    padding: 0 8px;
    border: 2px solid var(--color-accent);
    border-radius: 999px;
    color: var(--color-accent);
    font-size: 14px;
    line-height: 1.5;
    white-space: nowrap;
    vertical-align: middle;
  }
  .lt { color: var(--color-muted); }
  .note { font-size: 22px; font-weight: 600; }
  section.routes table { font-size: 0.62em; }
  section.routelist table { font-size: 0.64em; }
  section.routelist td { white-space: normal !important; }
  section.routelist td:first-child { white-space: nowrap !important; }
  section.routes td, section.routes th { white-space: nowrap; }
  section.sessions table { font-size: 0.72em; }
  section.sessions td:nth-child(2) { white-space: normal; }
  .kw { color: var(--color-accent); font-weight: 700; }
  section.sessions .note { margin-top: 0.4em; }
  .speakers { display: grid; grid-template-columns: repeat(8, 1fr); gap: 20px 8px; width: 100%; margin-top: 8px; }
  .speakers figure { margin: 0; text-align: center; }
  .speakers img { width: 104px; height: 104px; margin: 0 auto; border-radius: 50%; object-fit: cover; border: 3px solid var(--color-accent); background: #fff; }
  .bento { display: flex; gap: 32px; justify-content: center; margin-top: 16px; }
  .bento figure { margin: 0; text-align: center; }
  .bento img { width: 520px; height: 340px; object-fit: cover; border-radius: 12px; }
  .bento .logo-box { width: 520px; height: 340px; display: flex; align-items: center; justify-content: center; background: #fff; border: 2px solid #cce4f7; border-radius: 12px; }
  .bento .logo-box img { width: 380px; height: auto; object-fit: contain; border-radius: 0; }
  .bento figcaption { margin-top: 8px; font-size: 22px; font-weight: 700; }
  .pick { display: flex; align-items: center; gap: 24px; margin: 4px 0 12px; }
  .pick img { width: 112px; height: 112px; flex: none; border-radius: 50%; object-fit: cover; border: 3px solid var(--color-accent); background: #fff; }
  .pick-title { margin: 0; font-size: 26px; font-weight: 700; line-height: 1.4; }
  .pick-speaker { margin: 4px 0 0; font-size: 22px; font-weight: 600; color: var(--color-muted); }
  .speakers figcaption { margin-top: 6px; font-size: 16px; font-weight: 600; white-space: nowrap; }
  .globe { margin-left: 6px; font-size: 15px; }
  img.emoji { display: inline !important; height: 1em; width: auto; margin: 0 0.05em; vertical-align: -0.1em; }
  .hl { display: block; margin-top: 2px; color: var(--color-muted); font-size: 0.82em; font-weight: 500; }
  section.compact table { font-size: 0.58em; }
  section.persona table { font-size: 0.95em; width: 100%; margin-top: 24px; }
  section.persona td, section.persona th { padding: 0.6em 0.8em; white-space: normal !important; }
  section.persona .note { font-size: 26px; margin-top: 1em; }
  section.types td, section.types th { white-space: normal !important; }
  section.types table { font-size: 0.66em; width: 100%; }
  section.route table { font-size: 0.6em; }
  section.route td, section.route th { padding: 0.18em 0.5em; }
  section.route .note { margin: 0 0 0.3em; font-size: 20px; }
  section.compact td, section.compact th { padding: 0.22em 0.5em; }
  .sub { display: block; margin-top: 8px; color: var(--color-muted); font-size: 28px; font-weight: 600; }
---

<!-- _class: title -->

# PHPカンファレンス新潟2026のご紹介<br>- PHPを書いていなくても楽しめます -

2026/10/30 Niigata 5min Tech

おさない

---

<!-- _class: message -->

# 10月21日の夜、<br>何が起きたか覚えていますか？

<!--
問いかけで入る。手を挙げてもらってもよい（「対応した人？」）。
-->

---

# PHP本体に、重大な脆弱性（PHP2Shell）

* **2026/10/21**、PHP本体の重大な脆弱性2件の修正版が公開
  * 認証なしで、外部から任意のコードを実行されるおそれ（CVSS v4.0 **9.2**）
  * フレームワークやCMSの更新では直らず、**PHP本体の更新** が必要
* 国内でも、**多くのWebサービスが緊急メンテナンス** に
* **高市首相** がXで、修正パッチを **「可及的速やかに」** 適用するよう呼びかけ

<!--
CVE-2026-109618 / CVE-2026-109619。修正版は 8.5.12 / 8.4.27 / 8.3.36 / 8.2.35。
数字と日付は報道・セキュリティベンダーの解説ベース（research-memo.md 参照）。
個別のサービス名は出さない（停止時間などの情報が出典ごとに食い違うため）。
攻撃手法の詳細には触れない。
-->

---

<!-- _class: message -->

# それだけ多くのサービスを、<br>PHPが支えている

<!--
PHPを書いていない人も、毎日PHPで動くサービスを使っている。
「自分には関係ない言語」ではない、と気づいてもらう。
-->

---

# PHPコミュニティは、活動が盛ん

* 今年も、全国各地でカンファレンスが開かれています
  * PHPerKaigi（東京・中野）／PHPカンファレンス小田原
  * フロントエンド・PHPカンファレンス北海道／PHPカンファレンス（東京）
  * PHPカンファレンス愛媛／**PHPカンファレンス新潟** ← 11/14
  * PHPカンファレンス関西（2027年1月予定）
* 盛んだから、重大な脆弱性のときも **情報や知見が集まる**

<!--
並びは開催順（2026年）。出典は research-memo.md。日付は口頭では言わない。
最後の行で導入の PHP2Shell を回収する。
-->

---

# この発表のゴール

* **PHPコミュニティに入ってみませんか？**
  * その入口が、**11/14(土) 朱鷺メッセ** の PHPカンファレンス新潟2026
* ゴール：チケットを買って、**11/14 に朱鷺メッセに来ていること**

<!--
導入の「PHPは社会を支えている」を受けて、ゴールを「PHPコミュニティ」に置く。最後のQRスライドで回収する。
-->

---

# アジェンダ

1. PHPカンファレンス新潟2026とは
2. セッションの魅力
3. セッション以外のカンファレンスの魅力

---

<!-- _class: message -->

# 1. PHPカンファレンス新潟2026とは<span class="sub">Overview</span>

---

<!-- _class: promo -->

# 開催概要

* **日時**：2026/11/14(土) 10:00〜18:00（09:30 入場開始）
* **会場**：朱鷺メッセ（新潟駅から徒歩約20分 / バス約10分）
* **テーマ**：「新潟でかみしめて、つなぐ、つくる、つぎの未来へ。」

![PHPカンファレンス新潟2026](./images/phpcon-niigata-2026.png)

https://phpcon.niigata.jp/

---

# チケット

| 種別 | 内容 | 価格 |
|---|---|---|
| 一般 | 本編 ＋ お弁当 | 3,500円 |
| 一般（懇親会つき） | 本編 ＋ お弁当 ＋ 懇親会 | 8,000円 |
| 個人スポンサー | 本編 ＋ お弁当 ＋ 懇親会 ＋ 公式サイトにアイコン掲載 | 13,000円 |
| 個人スポンサー（本編参加なし） | 公式サイトにアイコン掲載 | 5,000円 |

※現地参加のチケットにはすべて新潟三新軒様のお弁当がつきます。
※私を含め、スタッフを通して買うと500円安くなります

<!--
懇親会つきの販売期限・当日券の扱いは未確定のため載せない（2026/10/29）。当日券にお弁当がつくかも未確認。
-->

---

<!-- _class: message -->

# 2. セッションの魅力<span class="sub">Sessions</span>

---

# 新潟2026がめざすこと

* テーマ：「新潟でかみしめて、**つなぐ**、つくる、つぎの未来へ。」
  * つなぐ＝人と人、地域とコミュニティ、今と未来
* 新潟の技術者と、全国のエンジニアが **つながる場** にしたい
  * PHPを書いているかどうかは関係なく
* だから、セッションも **PHPがメインではない方** や **はじめての方** に向けて選びました

<!--
テーマの各語の意味は、実行委員長 大沼佑樹「PHPカンファレンス新潟2026に向けて」より（research-memo.md）。
「つながる場にしたい」はコアスタッフとしての目標。次のスライドの「こんな方に → だから」につなぐ。
-->

---

<!-- _class: persona -->

# こんな方に楽しんでほしくて選びました

| こんな方に | だから |
|---|---|
| **PHPがメインではない方** | 言語を問わず楽しめるトークが **17本**（25本中） |
| **カンファレンスやPHPがはじめての方** | 初心者向けのトークが **8本** |

<p class="note">どう回るかは、このあとの <strong>タイプ別モデルルート</strong> で</p>

<!--
「全国のPHPer向け」だけでなく「PHP以外がメインの人」「まだ慣れていない人」が楽しめるように選んだ、が軸。
募集時も、PHP以外（DB・インフラ・CS・AI）の話や、新潟ゆかりの方・初登壇・初心者向けのトークを特に歓迎していた。
-->

---

# 当日の登壇者

<div class="speakers">
<figure><img src="./images/speakers/01-kajikawa.jpg" alt="梶川さん"><figcaption>梶川さん</figcaption></figure>
<figure><img src="./images/speakers/02-meihei.jpg" alt="meiheiさん"><figcaption>meiheiさん</figcaption></figure>
<figure><img src="./images/speakers/03-murata.png" alt="村田さん"><figcaption>村田さん</figcaption></figure>
<figure><img src="./images/speakers/04-asuto.png" alt="あすと.さん"><figcaption>あすと.さん</figcaption></figure>
<figure><img src="./images/speakers/05-tadsan.jpg" alt="tadsanさん"><figcaption>tadsanさん</figcaption></figure>
<figure><img src="./images/speakers/06-sizuhiko.jpg" alt="sizuhikoさん"><figcaption>sizuhikoさん</figcaption></figure>
<figure><img src="./images/speakers/07-kawase.jpg" alt="河瀨さん"><figcaption>河瀨さん</figcaption></figure>
<figure><img src="./images/speakers/08-matsuo.jpg" alt="松尾さん"><figcaption>松尾さん</figcaption></figure>
<figure><img src="./images/speakers/09-koizumi.jpg" alt="小泉さん"><figcaption>小泉さん</figcaption></figure>
<figure><img src="./images/speakers/10-zaki.jpg" alt="ざきさん"><figcaption>ざきさん</figcaption></figure>
<figure><img src="./images/speakers/11-wakaba.png" alt="wakabaさん"><figcaption>wakabaさん</figcaption></figure>
<figure><img src="./images/speakers/12-akama.png" alt="赤間さん"><figcaption>赤間さん</figcaption></figure>
<figure><img src="./images/speakers/13-yuzuneri.jpg" alt="ゆずねりさん"><figcaption>ゆずねりさん</figcaption></figure>
<figure><img src="./images/speakers/14-tsuttsun.jpg" alt="つっつんさん"><figcaption>つっつんさん</figcaption></figure>
<figure><img src="./images/speakers/15-aki.jpg" alt="あきさん"><figcaption>あきさん</figcaption></figure>
<figure><img src="./images/speakers/16-pochi.jpg" alt="ポチさん"><figcaption>ポチさん</figcaption></figure>
<figure><img src="./images/speakers/17-nagase.jpg" alt="永瀬さん"><figcaption>永瀬さん</figcaption></figure>
<figure><img src="./images/speakers/18-kahapipi.png" alt="かはぴぴさん"><figcaption>かはぴぴさん</figcaption></figure>
<figure><img src="./images/speakers/19-munakata.jpg" alt="ムナカタさん"><figcaption>ムナカタさん</figcaption></figure>
<figure><img src="./images/speakers/20-maguro.jpg" alt="マグロさん"><figcaption>マグロさん</figcaption></figure>
<figure><img src="./images/speakers/21-fukui.jpg" alt="福井さん"><figcaption>福井さん</figcaption></figure>
<figure><img src="./images/speakers/22-fkumnk.jpg" alt="fkuMnkさん"><figcaption>fkuMnkさん</figcaption></figure>
<figure><img src="./images/speakers/23-kawamura.jpg" alt="河村さん"><figcaption>河村さん</figcaption></figure>
<figure><img src="./images/speakers/24-akushimo.jpg" alt="あくしもさん"><figcaption>あくしもさん</figcaption></figure>
</div>

<!--
アイコンは fortee（公式サイトと同じ画像）。赤間さんはアイコン未登録のため fortee の既定アイコン。
並びはタイムテーブル順。
-->

---

<!-- _class: message -->

# タイプ別モデルルート<span class="sub">Model routes</span>

---

<!-- _class: types -->

# あなたはどのタイプ？

| タイプ | こんな方 | 選び方 → 1日で聴けるもの |
|---|---|---|
| **① はじめての方** | カンファレンスやPHPがはじめての方 | <span class="tag">初心者向け</span> を軸に → 設計・OSS・AI・テスト・画像の基本を一通り |
| **② PHPを書いていない方** | メイン言語がPHP以外の方 | <span class="tag">言語を問わず</span> を軸に → 運用・Wasm・AI・メール、コードの外の話まで |

<p class="note">どちらも朝の自己紹介から懇親会まで。気になる枠は、もう片方のトラックに移ってもOK</p>

---

<!-- _class: sessions route -->

# ルート① はじめての方

<p class="note"><strong>意図</strong>：<strong>初心者向け</strong> を軸に、朝は設計、午後は AI とテスト、夕方は同じ目線の LT で「自分もやってみよう」へ</p>

| 時刻 | 聴くもの・やること | ポイント |
|---|---|---|
| 10:00 | オープニング → **10:15 グループで自己紹介** | 最初の話し相手ができる |
| 10:50 A | 梶川琢馬さん：疎結合と結合バランス<span class="tag">初心者向け</span><span class="tag">言語を問わず</span> | 設計を3つの軸で整理 |
| 11:20 B | あすと.さん：はじめてのLaravelコントリビュート<span class="tag">初登壇</span> | Laravelを知らなくても歓迎 |
| 11:50 A | tadsanさん：PHPの静的解析<span class="tag">言語を問わず</span> | Ruby・Pythonと比べる |
| 12:10 | お昼（お弁当）・12:30 スポンサーのエレベーターピッチ／LT | 各社の技術が聞ける |
| 13:00 | アンカンファレンス・OST | その場でテーマを持ち寄る |
| 14:10 A | 河瀨翔吾さん：Eloquentでリポジトリパターン | 朝の設計の話の続き |
| 14:40 A | 小泉岳人さん：生成AIでチーム開発<span class="tag">初心者向け</span><span class="tag">言語を問わず</span> | AIをチームで使う7つのポイント |
| 15:10 B | 赤間仁志さん：PHPUnitを爆速に<span class="tag">言語を問わず</span> | 10分超を60秒に |
| 15:40 A | ゆずねりさん：WebPはなぜ軽いのか<span class="tag">初心者向け</span><span class="tag">言語を問わず</span> | 数式なしの図で |
| 16:15〜 | LT：**ポチさん**<span class="tag">初登壇</span>（個人開発）・**永瀬さん**（写経で学び直し）・**河村さん**（まず動く） | 同じ目線の話 |
| 17:30 | エンディング → **懇親会** | 1日で知り合った人ともう一歩深く |

<!--
初心者向けタグを軸に選んだルート（research-memo.md の旧ルートA）。11:20・11:50・14:10・15:10 は初心者向けタグがないので、入りやすい方を選んだ。14:10 の河瀨さんは朝の梶川さんの設計の話の続き。
-->

---

<!-- _class: sessions route -->

# ルート② PHPを書いていない方

<p class="note"><strong>意図</strong>：PHPの文法より、運用・型・AI・Webの仕組みなど、<strong>言語を越えて持ち帰れる</strong> テーマで1日を組む</p>

| 時刻 | 聴くもの・やること | ポイント |
|---|---|---|
| 10:00 | オープニング → **10:15 グループで自己紹介** | 最初の話し相手ができる |
| 10:50 B | meiheiさん：エラーのボールを拾い続ける<span class="tag">言語を問わず</span> | 明日の仕事に持ち帰れる |
| 11:20 A | 村田祐葵さん：型の本質 | 型の考え方は言語を越える |
| 11:50 B | sizuhikoさん：WasmでPHPとJSの壁を壊す<span class="tag">言語を問わず</span> | フロントの人にも |
| 12:10 | お昼（お弁当）・12:30 スポンサーのエレベーターピッチ／LT | 各社の技術が聞ける |
| 13:00 | アンカンファレンス・OST | その場でテーマを持ち寄る |
| 14:10 B | 松尾篤さん：ASTでバージョンアップを見抜く | 冒頭の脆弱性の話の続き |
| 14:40 A | 小泉岳人さん：生成AIでチーム開発<span class="tag">初心者向け</span><span class="tag">言語を問わず</span> | AIをチームで使う7つのポイント |
| 15:10 A | wakabaさん：AIの文脈を引き継ぐ<span class="tag">新潟枠</span><span class="tag">言語を問わず</span> | 作業日誌と判断基準 |
| 15:40 B | つっつんさん：メール到達性<span class="tag">言語を問わず</span> | 届かないメールの原因を追う |
| 16:15〜 | LT：**かはぴぴさん**（斧）・**fkuMnkさん**（財団）・**あくしもさん**<span class="tag">新潟枠</span>（新潟の364日） | コードの外の話も |
| 17:30 | エンディング → **懇親会** | 1日で知り合った人ともう一歩深く |

<!--
言語を問わずタグを軸に選んだルート（research-memo.md の旧ルートB）。11:20・14:10 は両トラックとも PHP寄りなので、言語に依存しにくい方（村田さん）と、冒頭の PHP2Shell につながる方（松尾さん）を選んだ。15:40 はルート①と差をつけるため、Web の運用に刺さるつっつんさんにした。
-->

---

<!-- _class: message -->

# 3. セッション以外の<br>カンファレンスの魅力<span class="sub">Beyond the sessions</span>

---

# 1人参加でも大丈夫！

* **朝 10:15〜**：3〜5人のグループで自己紹介
  * お題には「好きな日本酒」「行ってみたい新潟のスポット」も
* **昼 13:00〜14:00**：アンカンファレンス・OST
  * その場でテーマを持ち寄って、聴くも話すも自由
* **夜**：懇親会で、1日で知り合った人ともう一歩深く
* **途中参加もOK**：「午前だけ」「LTだけ」でも

<!--
お題と途中参加OKは KomeKaigi 参加者向け note と同じ内容。
OST は Open Space Technology（その場でテーマを出し合い、興味のある輪に自由に加わる）。旧版の「IRT」は誤りだったので OST に直した。
-->

---

# セッションの合間は、新潟の甘酒とコーヒーで

<div class="bento">
<figure><img src="./images/amazake-kouji.jpg" alt="今代司の甘酒"><figcaption>今代司 の甘酒</figcaption></figure>
<figure><div class="logo-box"><img src="./images/ararat-crews-logo.png" alt="ARARAT CREWS"></div><figcaption>ARARAT CREWS のコーヒー</figcaption></figure>
</div>

<p class="note">画像：今代司酒造 https://imayotsukasa.co.jp/　ロゴ：ARARAT CREWS</p>

<!--
甘酒の写真は今代司酒造の商品ページ「麹・発酵甘酒 麹（ノン・アルコール）」より。
https://imayotsukasa.co.jp/product/kouji/132/
ARARAT CREWS のロゴは NEWSCAST のプレスリリース（会社概要）に掲載のもの。
https://newscast.jp/news/0963261 （公式サイト nsaveararat.com は 2026/10/21 時点で接続できず）
-->

---

# ランチは新潟三新軒様のお弁当

* 参加チケットに含まれています
* お昼は、スポンサー企業の **エレベーターピッチ・LT** も

<div class="bento">
<figure><img src="./images/bento-2585.jpg" alt="新潟産コシヒカリと海鮮のうまいもん寿司"><figcaption>新潟産コシヒカリと海鮮のうまいもん寿司</figcaption></figure>
<figure><img src="./images/bento-794.jpg" alt="村上牛しぐれ"><figcaption>村上牛しぐれ</figcaption></figure>
</div>

<!--
画像出典: 新潟三新軒 商品ページ（新潟産コシヒカリと海鮮のうまいもん寿司 / 村上牛しぐれ）
https://www.niigata-sanshinken.co.jp/products/2585/ , https://www.niigata-sanshinken.co.jp/products/794/
-->

<p class="note">画像：新潟三新軒 https://www.niigata-sanshinken.co.jp/</p>

---
# 懇親会は新潟グルメで舌鼓を打ちましょう

* **ごはん**：新潟名物 **たれかつ**、**お刺身**、**サーモン塩辛** など
* **お酒**：新潟の日本酒の **唎酒コーナー**（ノンアルコールも）
* 朝や昼に **知り合った人** と、もう一歩深く

<p class="note">※お酒は20歳以上の方に限ります</p>

<!--
懇親会の内容は、スタッフ キムラさんの note（公開前のプレビュー、2026/10/30 時点）より。
たれかつは政家（まつりや）、お刺身は万代島鮮魚センター、オードブルは小柳食品、サーモン塩辛は三幸、唎酒は中善酒店、ジンソーダは越後薬草。お店の名前と、自己紹介のお題「好きな日本酒」の答え合わせは口頭で。
-->

---

# 会場へのアクセス

* **朱鷺メッセ**（新潟市中央区万代島）
* 新潟駅から **路線バスで約10分**（17番のりば・大人260円）
* 歩いても **約20分**
* 地元だから、**懇親会まで気軽に** 参加できます

<!--
バスは公式note「おすすめホテル10選」の記載（新潟駅17番のりば、朱鷺メッセ方面）。
徒歩・バスの所要時間は公式サイトの記載。
-->

---

# まとめ

1. PHPは社会を支えている。**PHPコミュニティに入ってみませんか？**
2. 入口は **11/14(土) 朱鷺メッセ**。迷ったら **タイプ別モデルルート** から
3. 朝の自己紹介から夜の懇親会まで、**人とつながれる**

---

<!-- _class: message -->

# 11/14(土)は朱鷺メッセに行きましょう！

---
<!-- _class: promo -->

# チケットはこちら

* 一般 3,500円 / 懇親会つき 8,000円（お弁当つき）
* `PHPCON-NIIGATA-000XYZNI` を入力すると500円安くなります！

![チケット販売ページのQRコード](./images/ticket-qr.png)

https://conference.findy-code.io/conferences/phpconniigata-2026/31/registration

<!--
QRを出したまま少し間を取る。読み取る時間をあげる。
購入後の返金は不可。学生向けは別途案内予定。
-->


---

<!-- _class: profile -->

# 自己紹介

![profile](../../themes/my-sns-icon.jpg)

<div class="profile-body">

<p class="profile-name">おさない</p>

<p class="profile-handle">X: @000sak000</p>

- PHPカンファレンス新潟2026 コアスタッフ

</div>
