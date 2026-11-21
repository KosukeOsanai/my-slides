---
marp: true
theme: my-slideshow-theme
paginate: false
style: |
  /* 差し色を PHPカンファレンス新潟 公式サイト（#005aa5）に合わせる */
  :root { --color-accent: #005aa5; --color-code-bg: #f0f8ff; }
  th, td { border-bottom-color: #cce4f7; }
  .kw { color: var(--color-accent); font-weight: 700; }
  .note { font-size: 22px; font-weight: 600; color: var(--color-muted); }
  .sub { display: block; margin-top: 12px; color: var(--color-muted); font-size: 28px; font-weight: 600; }
  section.refs ul { font-size: 0.55em; line-height: 1.35; }
  section.refs li { margin: 0.2em 0; word-break: break-all; }
  /* テーマは img を display:block にするため、横並びは flex で組む */
  .row { display: flex; justify-content: center; align-items: center; gap: 24px; margin-top: 24px; }
  .row img { width: calc((100% - 48px) / 3); height: auto; }
  .row figure { margin: 0; width: calc((100% - 48px) / 3); text-align: center; font-size: 20px; line-height: 1.4; color: var(--color-muted); }
  .row figure img { width: 100%; }
  .row figcaption { margin-top: 8px; }
  .qr { display: flex; justify-content: center; gap: 120px; margin-top: 8px; }
  .qr figure { margin: 0; text-align: center; font-size: 24px; line-height: 1.4; }
  .qr figcaption { margin-top: 8px; }
  .qr .label { font-size: 28px; font-weight: 700; color: var(--color-accent); margin-bottom: 8px; }
  .qr img { width: 280px; height: 280px; margin: 0 auto; }
  .center { display: flex; justify-content: center; }
  .center img { max-width: 100%; height: 380px; width: auto; }
  /* 箇条書きの下に画像を横並びで置く */
  .imgs { display: flex; justify-content: center; align-items: flex-end; gap: 40px; margin-top: 20px; }
  .imgs figure { margin: 0; text-align: center; font-size: 20px; line-height: 1.4; color: var(--color-muted); }
  .imgs img { height: 260px; width: auto; max-width: 100%; margin: 0 auto; }
  .imgs figcaption { margin-top: 6px; }
  .imgs.large img { height: 340px; }
  /* 2つの問いを左右のカードで並べる */
  .qs { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; width: 100%; margin-top: 32px; }
  .qs .q { border: 2px solid var(--color-accent); border-radius: 16px; background: var(--color-code-bg); padding: 28px 32px; text-align: left; }
  .qs .label { font-size: 40px; font-weight: 800; color: var(--color-accent); margin-bottom: 12px; }
  .qs .text { font-size: 32px; font-weight: 700; line-height: 1.55; }
  .qs .text .kw { white-space: nowrap; }
---

<!-- _class: title -->

# PHPカンファレンス新潟がこの先生きのこるには<br>―1コアスタッフの目線から―

2026/11/21 TechRAMEN 2026 Conference

おさない

<!--
〜0:10 タイトルを読む。「新潟2026でコアスタッフをやってた、おさないです」
-->

---

# おことわり

- 本LTは発表者個人の見解であり、実行委員会の公式見解ではありません
- 特定の人物や団体を批判する意図はありません

<!--
〜0:15 さらっと読む。
-->

---

<!-- _class: message -->

# PHPカンファレンス新潟2026に参加してくださった皆さん、ありがとうございました！

<!--
〜0:30 関わってくれた皆さんへの感謝。
-->

---

# 私のロール

* 準備期間の前半：プロポーザル・タイムテーブル周り
* 準備期間の後半：SNS・note の執筆とディレクションも兼任

<div class="imgs large">
  <figure><img src="./images/niigata-2026-timetable.png" alt="PHPカンファレンス新潟2026 タイムテーブル"><figcaption>タイムテーブル（fortee のデータから作成）</figcaption></figure>
  <figure><img src="./images/note-niigata-magazine.png" alt="PHPカンファレンス新潟 note マガジンの記事一覧"><figcaption>note マガジン</figcaption></figure>
</div>

<!--
〜0:45 兼任になった理由（誰の代わりか）は言わない。
-->

---

# 開催した結果

* 参加者は92名
* 「来年もまた開催して」という声もいただいた
* 事前準備や当日の運営に課題

<div class="imgs large">
  <figure><img src="./images/niigata-2026-furikaeri.jpg" alt="エンディングで投影された「本日の振り返り」：25セッション・2トラック・92ご来場者数"><figcaption>エンディングの「本日の振り返り」（@phpcon_niigata の投稿写真より）</figcaption></figure>
</div>

<!--
〜1:00 数字は淡々と。よかったことは素直に嬉しかったと言う。課題の具体例は挙げず、さらっと流す。
-->

---

<!-- _class: message -->

# 終わってから考えた、2つの問い

<div class="qs">
  <div class="q"><div class="label">Q1</div><div class="text">PHPカンファレンス新潟は、<br><span class="kw">来年以降も開催できる体制</span>か？</div></div>
  <div class="q"><div class="label">Q2</div><div class="text">新潟2026は、新潟の<br><span class="kw">普段のコミュニティ</span>と<br>つながれていたか？</div></div>
</div>

<!--
〜1:15 本題の問い。2つとも読む。間を取る。
-->

---

# Q1. 来年以降も開催できる体制か

* なんとか形にするので精一杯だった
* スタッフが抜けたとき「拾える人が拾う」構造になった
  * 私も役割の穴を放置し、当日は Track統括とSNS発信を兼任
* この状況では、来年以降も続けられるかどうか **判断できない**

<!--
〜2:00 答えは「まだ言えない」。人数・経験が足りなかったわけではない、と口頭で添える。偏りは自分の反省として話し、「私も含めて」を必ず入れる（特定の人＝委員長の話に聞こえないように）。抜けた人数・理由は言わない。「無謀」「規模が重すぎる」とは言わない（規模と偏りのどちらが原因かは断定しない）。
-->

---

# Q2. 新潟の普段のコミュニティとつながれていたか

* 新潟の方が、新しくスタッフとして関わってくださった
* 開催2週間前に、新潟の技術イベント「Niigata 5min Tech」「Komekaigi」に参加
  * Komekaigi 経由で、参加者・当日スタッフの方につながった

<div class="imgs">
  <figure><img src="./images/niigata-5min-tech-28.png" alt="Niigata5分Tech #28"><figcaption>Niigata5分Tech #28（10/30）</figcaption></figure>
  <figure><img src="./images/komekaigi-2026-ogp.jpg" alt="KomeKaigi 2026"><figcaption>KomeKaigi 2026（10/31）</figcaption></figure>
</div>

<!--
〜2:20 「2つ目の答えは、半分かなと」から入る。希望の話として。「来てくれた人がいたのは本当に嬉しかった」
-->

---

# Q2. 新潟の普段のコミュニティとつながれていたか

* 準備期間中に新潟の勉強会へ顔を出せたのは、KomeKaigiのほかに1回
* 運営は、私も含めてほぼ県外在住
* 新潟のコミュニティの方を対象とするなら、尚更重要

<!--
〜2:40 「私が顔を出せたのは1回だけ → 運営は私も含めてほぼ県外在住 → 新潟のコミュニティの方に来てほしいなら、普段からのつながりはなおさら大事」の流れで話す。3行目は Q2 の答えの「残り半分」として言い、13枚目（Q2への答え）で「勉強会なら普段から関われる」につなぐ。「出身」ではなく「在住」。新潟在住スタッフの人数は言わず「ほぼ県外」とだけ言う。「県外の人が運営していたのが悪い」には聞こえないよう、主語に「私も含めて」を入れる。特定の人の話にはしない（勉強会の主催者は委員長本人）。
-->

---

<!-- _class: message -->

# <span class="kw">PHP勉強会in新潟</span>が続く体制をつくることが、<br><span class="kw">PHPカンファレンス新潟</span>が生きのこる道になる

<!--
〜2:50 今日いちばん言いたいことを先に言う1枚。「なので、今日いちばん言いたいのはこれです」と前置きして、ゆっくり読んで間を取る。「私がやる」「rebootする」とは言わない（主催者は委員長本人）。なぜそう言えるかは、11枚目で PHP勉強会in新潟を紹介したあと、12〜13枚目で Q1・Q2 に答える形で話す。締めは16枚目。
-->

---

# PHP勉強会in新潟とは

* 新潟でPHPについて話す勉強会（connpass: niigata.php）
* 2024年から2025年にかけて5回開催。
* 今はお休み中

<div class="imgs">
  <figure><img src="./images/php-niigata-5.png" alt="PHP勉強会in新潟（niigata.php）"><figcaption>PHP勉強会in新潟（connpass: niigata.php）</figcaption></figure>
</div>

<!--
〜3:00 県外の聴衆向けに、どんな場かを一言で。主催者が委員長であることは言わない。止まった理由・時期の解釈も言わない（言えるのは connpass の記録まで）。
-->

---

# Q1への答え：勉強会なら、小さく始めて任せられる

* 勉強会なら金銭的リスクも手間も小さく、スモールスタートできる
* 受付・告知など、運営を小さく切って任せられる
* 勉強会に携わってくださった人が、次のカンファレンスの担い手になるかも

<!--
〜3:15 最後の1行が、16枚目（締め）「勉強会の体制 → カンファレンスが生きのこる」への橋渡し。「任せられる」は Q1 の「負担が動ける人に偏った」への答え。
-->

---

# Q2への答え：勉強会なら、普段から関われる

* 課題：県外の私たちが新潟と関われたのは、カンファレンスの直前だけ
* 定期的な開催の場があれば、カンファレンスがない日もつながりを保てる

<!--
〜3:35 「直前だけ」→「普段から」の対比を意識して話す。
-->

---

# ケの日の延長に、ハレの日がある

<div class="row">
  <figure><img src="./images/techramen-2026.png" alt="TechRAMEN 2026 Conference"><figcaption>ゆるい勉強会@旭川・FuraIT@富良野<br>→ TechRAMEN</figcaption></figure>
  <figure><img src="./images/techtama-2026.png" alt="TechTAMA 2026 Conference"><figcaption>多摩.dev<br>→ TechTAMA 2026（多摩.dev #6）</figcaption></figure>
  <figure><img src="./images/dai-funabashi-dev.png" alt="大Funabashi.dev"><figcaption>Funabashi.dev<br>→ 大Funabashi.dev</figcaption></figure>
</div>

<span class="sub">新潟のPHPにも、ケの日の場をもう一度</span>

<!--
〜3:50 左から TechRAMEN（運営メンバーの多くが旭川・富良野の勉強会から）、TechTAMA 2026（多摩.dev #6）、大Funabashi.dev（Funabashi.dev の拡大版）。口頭では TechRAMEN だけ「今日のこの TechRAMEN も、運営メンバーの多くが旭川・富良野の勉強会から来ています」と会場に向けて言う。TechTAMA・大Funabashi.dev はキャプションに任せて読まない。下の1行は次の「私の次の一歩」への橋渡し。特定の人の話にはしない（勉強会の主催者は委員長本人）。「新潟には勉強会がない」とは言わない（Niigata 5min Tech・Komekaigi がある）。
-->

---

# 私の次の一歩

* PHP勉強会in新潟はできれば再開したいと話している
* 県外の私にできるのは、そこに関わり続けること
  * 勉強会で登壇する、運営を手伝う、担い手を探す
* 勉強会が続く体制になるよう、その一端を担いたい

<!--
〜4:22 「私がやります」とは言わない。頻度も言わない。出典はツナギメエフエム第188回の文字起こし（要約で伝え、一字一句の引用はしない）。
-->

---

<!-- _class: message -->

# 次は、PHP勉強会in新潟の再開から始まる

<!--
〜4:45 一番伝えたい1枚。タイトルの「生きのこる」を回収する。ゆっくり読んで、間を取る。ありがとうございました。
-->

---

<!-- _class: promo -->

# PHPカンファレンス関西2026

* 日時：2027/1/16(土)
* 会場：京都リサーチパーク 4号館（JR丹波口駅から徒歩5分）

![PHPカンファレンス関西2026](./images/kansai-2026-ogp.png)

https://2026.kphpug.jp/

<!--
ここから宣伝3枚は、時間があるときだけ（4:45 を過ぎていたら飛ばして自己紹介へ）。名前は「2026」だが開催は2027年1月。
-->

---

# このLTの続きは、関西で

<div class="center">
  <img src="./images/kansai-aki-fortee.png" alt="あき「関西のPHPコミュニティーの現在地」">
</div>

<span class="sub" style="text-align: center;">関西PHP勉強会の主催・PHPカンファレンス関西2025実行委員長のあきさんによるLT<br>勉強会とカンファレンスの「循環」の話</span>

---

# チケット販売中・当日スタッフ募集中

<div class="qr">
  <figure>
    <div class="label">チケット販売ページ</div>
    <img src="./images/kansai-ticket-qr.png" alt="チケット販売ページのQRコード">
  </figure>
  <figure>
    <div class="label">当日スタッフ募集中</div>
    <img src="./images/kansai-staff-qr.png" alt="当日スタッフ募集ページのQRコード">
  </figure>
</div>

<!--
「当日スタッフは運営が初めての方も大歓迎です。ケの日・ハレの日に関わる最初の一歩にぜひ」。
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

<!--
〜4:50 「X は @000sak000 です。このあと、ぜひ話しかけてください」の一言だけ。
-->