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

# この発表のゴール

* **PHPコミュニティに入ってみませんか？**
  * その入口が、**11/14(土) 朱鷺メッセ** の PHPカンファレンス新潟2026
* ゴール：チケットを買って、**11/14 に朱鷺メッセに来ていること**

<!--
導入の「PHPは社会を支えている」を受けて、ゴールを「PHPコミュニティ」に置く。最後のQRスライドで回収する。
-->

---

# アジェンダ

1. PHPコミュニティについて
2. PHPカンファレンス新潟2026の紹介
3. セッションと、セッション以外の交流

---

<!-- _class: message -->

# 1. PHPコミュニティについて<span class="sub">Community</span>

---

# 全国各地で、PHPカンファレンス

* 今年も、全国各地で開かれています
  * PHPerKaigi（東京・中野）
  * PHPカンファレンス小田原
  * フロントエンド・PHPカンファレンス北海道
  * PHPカンファレンス（東京）
  * PHPカンファレンス愛媛
  * **PHPカンファレンス新潟** ← 11/14
  * PHPカンファレンス関西（2027年1月予定）

<!--
並びは開催順（2026年）。出典は research-memo.md。日付は口頭では言わない。
-->

---

# 初心者も、PHPを書いていない人も歓迎

* 各地のカンファレンスで、**初心者向け** や **言語を問わない** トークも採択
* フロントエンドと合同の **フロントエンド・PHPカンファレンス北海道** も
* **初登壇** を後押しする取り組みも
  * 例：PHPカンファレンス関西の **プロポーザル作成ワークショップ**
* **聴くだけでも、話してみても** OK

<!--
「PHPを書いていないから関係ない」をここで外す。新潟2026の数字はこのあと（新潟の紹介）で出すので、ここでは各地の例だけ。
関西のプロポーザル作成ワークショップは 20260924-phpstudykansai の告知スライドより。
-->

---

# コミュニティに入ると、いいこと

* 全国各地で毎年カンファレンスがあり、**活動が盛ん**
* 重大な脆弱性のときも、情報や知見が **コミュニティで共有される**
* **地元にいながら**、全国のエンジニアと直接話せる
* ほかの言語のコミュニティをのぞくと、**自分の言語を見る目も変わる**

<!--
2点目で導入の PHP2Shell を回収する。
3〜4点目は KomeKaigi 参加者向け note（notes/20261029-komekaigi/note.md、ブランチ claude/loving-volta-ck6nig）と同じ主張。
-->

---

<!-- _class: message -->

# 2. PHPカンファレンス新潟2026の紹介<span class="sub">Overview</span>

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

# 3. セッションと、<br>セッション以外の交流<span class="sub">Sessions & Beyond</span>

---

# どんなセッションを選んだか

* **主なペルソナ**：この人たちに楽しんでほしい
  * **新潟で働く・暮らす技術者**（メイン言語がPHPではない方も）
  * カンファレンスの参加歴や、PHP歴が短い方
* **だから**
  * 言語を問わず楽しめるセッションが **17本**
  * 初心者向けのセッションを **8本** と多めに採用

<!--
「全国のPHPer向け」だけでなく「新潟の、PHP以外のエンジニア」「まだ慣れていない人」が楽しめるように選んだ、が軸。今日の会場はまさにこの人たち。
募集時も、PHP以外（DB・インフラ・CS・AI）の話や、新潟ゆかりの方・初登壇・初心者向けのトークを特に歓迎していた。
-->

---

<!-- _class: sessions compact -->

# PHPを書いていなくても楽しめる7本

| 時刻 | セッション | 登壇者 |
|---|---|---|
| 10:50 A | 疎結合とは何か？ソフトウェア設計における結合バランスについて考える<span class="hl"><span class="kw">設計</span>｜結合を強さ・距離・変わりやすさの3軸で整理</span> | 梶川琢馬さん |
| 14:40 A | 生成AIを用いてチーム開発する際の７つのポイント　仮説検証のポイントを漫画『瑠璃の宝石』をヒントにして<span class="hl"><span class="kw">AI・チーム開発</span>｜観察・データ・多様なチームの7ポイント</span> | 小泉岳人さん |
| 15:40 A | imagewebp()の向こう側―WebPはなぜ JPEG・PNGより軽いのか<span class="hl"><span class="kw">Web・画像</span>｜2つのコーデックを数式なしの図で解説</span> | ゆずねりさん |
| 16:25 <span class="lt">LT</span> | 手の動かし方がわからなかった私が個人開発者になるまで<span class="hl"><span class="kw">個人開発</span>｜未経験からWebアプリ公開まで</span> | ポチさん |
| 16:30 <span class="lt">LT</span> | 私のコードは、ぜんぶAIが書いていた 〜2年目、写経で取り戻す〜<span class="hl"><span class="kw">学び直し</span>｜AIの出力を写経しながら、AIと壁打ち</span> | 永瀬博之さん |
| 17:10 <span class="lt">LT</span> | The PHP Foundation ： 推しの組織は謎組織♥️<span class="hl"><span class="kw">OSS</span>｜言語を支える財団は何をしているのか</span> | fkuMnkさん |
| 17:15 <span class="lt">LT</span> | “まず動く”と、なぜ世界が広がるのか<span class="hl"><span class="kw">コミュニティ</span>｜1枚のTシャツから、新潟のコアスタッフへ</span> | 河村直樹さん |

<p class="note"><strong>7本とも Track A</strong>：<span class="tag">初心者向け</span>かつ<span class="tag">言語を問わず</span>のトーク。Track A にいれば全部聴けます</p>

<!--
公式noteのセッション紹介 第7弾（PHPを書いていない方向け）の5本に、第6弾で「PHPを書いていない方にもおすすめ」とした永瀬さん・fkuMnkさんのLTを足した7本。
fortee の「初心者向け」タグ × 「言語を問わずおすすめ」の両方がついたトークは、この7本で全部。
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

# PHPを書いている方へ：<br>コアスタッフがあえて選ぶ3選

---

# あえて選ぶ、聴きたいセッション3選

| 時刻 | セッション | 登壇者 |
|---|---|---|
| 10:50 B | エラーチャンネルのボールを拾い続けて鍛えるエンジニアの地力 | meiheiさん |
| 11:20 B | OSSコントリビュート未経験者がLaravelに新規メソッドを追加するまでの話 | あすと.さん |
| 14:40 B | AI駆動で挑む！？レガシーPHPプロダクトのバージョンアップへの軌跡 | ざきさん |

<p class="note"><strong>PHPを書いている方向け。3本とも Track B</strong>：時間が重ならないので、1日で全部聴けます</p>

<!--
「おすすめ」ではなく、コアスタッフ個人として「自分が聴きたい」3本。
共通点は、目の前の現場から一歩踏み出した人の実体験であること。
-->

---

# 1. エラーのボールを拾い続ける<span class="tag">言語を問わず</span>

<div class="pick">
<img src="./images/speakers/02-meihei.jpg" alt="meiheiさん">
<div>
<p class="pick-title">エラーチャンネルのボールを拾い続けて鍛えるエンジニアの地力</p>
<p class="pick-speaker">meiheiさん（@app1e_s）｜10:50 Track B</p>
</div>
</div>

* **選んだ理由**
  * エラー対応は、誰かが拾わないと流れていく **地味な仕事**
  * それを拾い続けることが **地力とオーナーシップ** になる、という視点
  * 言語を問わず、**明日の自分の仕事** にそのまま持ち帰れる

---

# 2. はじめてのLaravelコントリビュート<span class="tag">初登壇</span>

<div class="pick">
<img src="./images/speakers/04-asuto.png" alt="あすと.さん">
<div>
<p class="pick-title">OSSコントリビュート未経験者がLaravelに新規メソッドを追加するまでの話</p>
<p class="pick-speaker">あすと.さん（@ast_and_kaya）｜11:20 Track B</p>
</div>
</div>

* **選んだ理由**
  * 「OSSに貢献したい」と思っても、**最初のPRまでが遠い**
  * 未経験から **`whenEnum()` のPRがマージされるまで** の流れが聞ける
  * Laravelの哲学にも触れる。**Laravelを知らなくてもwelcome**

---

# 3. AIレビューでバージョンアップ<span class="tag">初登壇</span>

<div class="pick">
<img src="./images/speakers/10-zaki.jpg" alt="ざきさん">
<div>
<p class="pick-title">AI駆動で挑む！？レガシーPHPプロダクトのバージョンアップへの軌跡</p>
<p class="pick-speaker">ざきさん（@k_yamasaki_zaki）｜14:40 Track B</p>
</div>
</div>

* **選んだ理由**
  * **8万テーブルの生PHP** を、**PHP 7.3 から 8.4** へ
  * AIにレビューさせながら進める、**AI時代のレガシー改修** の実例
  * きれいな成功談だけでなく、**失敗談** も聞ける

---

<!-- _class: message -->

# セッション以外の交流

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

# セッション間は新潟企業様の飲食物で休憩

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

* **懇親会のごはん**：昨年は利き酒コーナーや、新潟名物 **タレカツ** も

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
2. 入口は **11/14(土) 朱鷺メッセ**。まずは **Track A の7本** から
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
