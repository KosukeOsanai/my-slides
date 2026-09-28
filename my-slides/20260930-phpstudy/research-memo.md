# 調査メモ（20260930 PHPStudy 用）

発表テーマ: GitHub ActionsのRunnerをBlacksmith（Third-party Runner）に変更してCIの高速化・コスト削減を狙った話。
成功したプロダクトと、`setup-php` がボトルネックになり採用を見送ったプロダクトの両方を紹介する。

想定セッション: 約5分（2026-09-27に短縮）

> スライドは「Blacksmithとは（なぜ安くなるか：単価と性能）／導入手順／プロダクトに入れた結果」の3部。
> このメモの事実関係（料金・Quickstart・Issue #1056）はそのまま使う。
> GitHub Actionsの基礎、Runner3分類の比較表、Zenn記事の数値、depot.dev / WarpBuild は5分版では話さない。

> **note**: 既存の [20260911-phptokyo.md](./20260911-phptokyo.md)（PHPTokyo 2026/09/11 向け、5〜10分想定）が
> 本発表の土台になっている。今回はその内容を25〜30分に拡張する。構成・トーンは極力踏襲しつつ、
> GitHub Actionsの基礎知識、Runner種別の比較、コストの考え方、`setup-php` が遅くなる技術的な理由を
> より厚く説明する。

## 情報源（ChatGPT共有セッション）

- <https://chatgpt.com/share/6a9ef218-befc-83e8-832f-35c0c8549711>
  - GHA Runnerの基礎、GitHub-hosted/Self-hosted/Third-party Runnerの違い、Blacksmithの位置づけ、
    2プロダクトでの成功/失敗体験、`setup-php` のIssue #1056、20分・5〜10分それぞれの構成叩き台、
    プロポーザル文の推敲まで、既存デッキ（20260911-phptokyo.md）の元になった会話そのもの。
  - **注意**: セッション内でChatGPTが提示した「2026年3月からself-hosted runnerに$0.002/分のplatform feeが
    導入される」という情報は、セッション後半でユーザー自身の指摘によりChatGPTが誤りを認め、
    「延期・再検討中」と訂正している。本メモではこの経緯があるため、GitHub Actionsの料金体系は
    公式ドキュメントを直接確認し直した（下記4節）。
  - セッション内の`citeturn...`形式の出典表記はChatGPT側の内部引用マーカーであり、そのままでは
    リンク切れや未検証のものが含まれる（例: Blacksmithのキャッシュ高速化に関するブログ記事は
    URLが404で存在しなかった）。**本メモの数値・引用はすべて下記の一次ドキュメントへの直接アクセスで
    再確認したものに限定している。**

---

## 1. GitHub Actionsの基礎（Workflow / Job / Step / Runner）

- Workflow: `.github/workflows/*.yml` で定義するCI全体
- Job: Workflow内の実行単位（例: `test`）
- Step: Job内の個々の処理（`checkout` → `setup-php` → `composer install` → `phpunit` → `phpstan` など）
- Runner: **Jobを実際に実行するマシン**
  - 公式ドキュメントの定義: "Runners are the machines that execute jobs in a GitHub Actions workflow.
    For example, a runner can clone your repository locally, install testing software, and then run
    commands that evaluate your code."
  - `runs-on: ubuntu-latest` は「このJobをどのRunnerで実行するか」を指定している

出典: [About GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners/about-github-hosted-runners)

---

## 2. Runnerの3つの選択肢

| | GitHub-hosted | Self-hosted | Third-party（Blacksmith等） |
|---|---|---|---|
| Runnerの管理者 | GitHub | 自分たち | Third-partyサービス |
| サーバー管理の要否 | 不要 | 必要（自己責任でOS・ソフトウェア更新） | 基本不要 |
| GitHub Actionsの利用料金 | 従量課金 | **無料**（インフラ費用は別途自己負担） | サービス側の従量課金 |
| ハードウェア/OSの自由度 | 低い（GitHub管理の環境のみ） | 高い | サービスに依存（Blacksmithはある程度選べる） |

- GitHub-hosted runner: GitHubが用意・管理する仮想マシン。"GitHub provides runners that you can use
  to run your jobs, or you can host your own runners."
- Self-hosted runner: "A self-hosted runner is a system that you deploy and manage to execute jobs
  from GitHub Actions on GitHub."
  - メリット: 既存マシンの活用、ハードウェア/OS/ソフトウェアの自由度が高い（"Give you more control
    of hardware, operating system, and software tools than GitHub-hosted runners provide."）、
    GitHub Actionsの利用自体は無料
  - デメリット: OS・ソフトウェアの更新は完全に自己責任（"you are responsible for updating the
    operating system and all other software."）。セキュリティ・保守の負担が大きい
  - なお「1台のサーバーに複数のself-hosted runnerを同居させない」等の運用上の注意事項は、
    GitHub公式の self-hosted runner 概要ページ自体では確認できなかった。この文言は
    `setup-php` 側のドキュメントに明記されているものなので、出典として混同しないよう
    下記6節に切り分けて記載する
- Third-party runner（Blacksmith等）: GitHub-hosted runnerの代わりとしてサードパーティが提供する
  Runner。Self-hostedほどの管理負担なく、GitHub-hostedより高性能・低価格を狙える「中間」の選択肢。
  Workflow YAML自体は`runs-on`の指定を変えるだけで、基本的にそのまま使える。

出典:
- [About GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners/about-github-hosted-runners)
- [About self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)

---

## 3. なぜRunnerを変えると速度・コストが変わるのか

- CIの実行時間は、実行するコード（PHPUnit/PHPStan/Composerなど）だけでなく、**それを実行する
  Runnerの性能**（CPU / Memory / Disk I/O / Network / Cache）にも左右される
- コストの考え方: `CIコスト ≒ Runnerの単価 × 実行時間`
  - Runnerの単価が高くても、実行時間が大幅に短縮されればトータルコストは下がり得る
  - 逆に、単価が安くても実行時間が伸びればコストが増えることもある（今回の失敗例の構造）

---

## 4. GitHub Actionsの料金体系（公式ドキュメントで直接確認・2026年時点）

出典: [GitHub Actions billing (product-billing/github-actions)](https://docs.github.com/en/billing/concepts/product-billing/github-actions)

- GitHub-hosted runnerの分単価（一部抜粋、Linux系）
  - Linux 1-core (x64): $0.002/分
  - Linux 2-core (x64): $0.006/分
  - Linux 2-core (arm64): $0.005/分
- **Self-hosted runnerの利用自体はGitHub Actions側では無料**（"GitHub Actions usage is free for
  self-hosted runners"。ただしインフラ費用は別途発生）
- ChatGPTセッション内で言及されていた「2026年3月からself-hosted runnerに$0.002/分のplatform fee」
  という話は、**公式ドキュメントの現在のページには記載がなく、確認できなかった**。セッション内でも
  ユーザーの指摘を受けてChatGPT自身が「延期・再検討中」と訂正している。
  → **スライドではこの値上げ／platform feeの話には触れない**（未確定・裏取りできない情報のため）

---

## 5. Blacksmith（Third-party Runner）

出典: [Blacksmith Pricing](https://www.blacksmith.sh/pricing)

- 分単価（一部抜粋）
  - Ubuntu x64: $0.004/分
  - Ubuntu ARM: $0.0025/分
- Blacksmith公式が謳う効果（**あくまでBlacksmith側の主張**として扱う）
  - 「2倍高速なハードウェア」による実行時間の削減
  - GitHubの分単価と比べて33%安い
  - トータルコスト削減: Ubuntu x64で最大67%、Ubuntu ARMで75%、Windows x64で60%、macOS M4で35%
  - キャッシュのダウンロードが4倍高速
  - 月3,000分の無料枠、Docker layer caching・sticky disk・静的IPなどのオプション機能
- Workflow上の変更は`runs-on`の指定を変えるだけ
  ```yaml
  # Before
  runs-on: ubuntu-latest
  # After
  runs-on: blacksmith-4vcpu-ubuntu-2404
  ```
- **重要**: 性能・料金の数値はBlacksmith自身が公表しているものであり、発表では「Blacksmithの主張」
  として紹介し、自分たちの実測値とは区別して話す

---

## 6. `setup-php` とは

出典: [shivammathur/setup-php README](https://github.com/shivammathur/setup-php)

- "Setup PHP with required extensions, php.ini configuration, code-coverage support, and various
  tools like composer in GitHub Actions" — PHP本体・拡張・php.ini設定・Composerなどのツールを
  セットアップするAction
- self-hosted runner（Third-party runnerも同様の扱いになりやすい）で使う場合は、専用の
  Requirementsガイドに従う必要がある。GitHub-hosted runnerとまったく同じセットアップではない
- 公式の注意事項として、1台のサーバーに複数のself-hosted runnerを同居させない、GitHub-hosted
  runnerと同じlabelを使い回さない、といった制約がある（Self-hosted runner全般の注意点と共通）

---

## 7. `setup-php` Issue #1056 — Blacksmithで`setup-php`が遅い問題（一次情報で内容確認済み）

出典: [shivammathur/setup-php Issue #1056](https://github.com/shivammathur/setup-php/issues/1056)
（`gh issue view` で本文・コメントを直接取得して確認）

- 起票: 2026年1月29日。コメント数12件、直近の更新は2026年6月2日（作者本人による返信）。
  `gh issue view`で`state`を直接確認し、**現在もOpen**であることを確認済み
- 報告内容（Issue本文、原文引用）:
  > "I noticed that on GitHub-owner runners (ubuntu-latest etc.) the action setup-php takes just a
  > few seconds. ... I noticed that on Blacksmith ... it always takes over a minute. I'm testing it
  > on `runs-on: "blacksmith-2vcpu-ubuntu-2404"` and `runs-on: "blacksmith-4vcpu-ubuntu-2404"`"
  - GitHub-hosted runnerでは数秒、Blacksmithでは常に1分以上かかる、という報告
- **根本原因（setup-php作者 shivammathur本人のコメント、原文引用）**:
  > "On GitHub runners the libraries that are pre-installed are known and change rarely, so we have
  > cached builds with libraries that are not there, so it is as simple as downloading a build and
  > extracting it. On self-hosted / third party runners it installs the missing libraries using apt
  > and that adds to the runtime."
  - **技術的な核心**: GitHub-hosted runnerは事前にインストールされているライブラリの構成が
    既知かつ安定しているため、setup-php側はその構成に対応した**ビルド済みキャッシュをダウンロード
    して展開するだけ**で済む。一方、self-hosted / third-party runnerでは前提となるライブラリ構成が
    保証されないため、**不足しているライブラリを`apt`で都度インストールする**必要があり、その分
    実行時間が伸びる
  - Third-party runner用のキャッシュ対応は「メンテナンス負荷が高く、現時点では着手できない」と
    作者自身が明言している（対応予定なし、回避策はユーザー側の工夫に委ねられている）
  - **既存デッキ（20260911-phptokyo.md）にはこの根本原因の説明がなく、「類似報告あり」という
    紹介にとどまっている。今回はここを厚く説明する。**
- その他Issue内のやり取り
  - 別のサードパーティRunner（depot.dev）でも同様の事象が報告されている（`RUNNER_ENVIRONMENT`の
    検出方法に起因する可能性についてPR #1069で議論されているが、**未マージ・議論継続中**であり
    確定した解決策ではない）
  - 2026年5月にはWarpBuild runnerでも類似の遅延（最大10分）が報告されている
  - → **今回自分たちが遭遇した事象は、setup-php側でも継続的に報告されている既知のパターンの
    一つ**という位置づけで話すのが正確（「このIssueで完全に原因が解決された」とは言わない）

---

## 8. きっかけとなったZenn記事（一次情報で数値確認済み）

出典: [YAMLを数行変えただけでGithub Actionsの料金を70%削減できて実行時間まで減った話](https://zenn.dev/counterworks/articles/573954dcfa8bb6)（Zenn, counterworks）

- 自動テストの実行時間: 約55分 → 約23分（**約60%弱の高速化**）
- Dockerビルド: 約2分30秒 → 約40秒（**約70%強の高速化**）
- コスト: 前月比で約70%程度削減（コストが約1/3程度に）
- 記事の結論: 「気軽にGitHub Actionsを高速化＆コスト削減ができた」と評価しつつ、
  > "情報漏洩や提供元の破綻等々、安定と信頼のGithub提供よりリスクもあります"
  > "どの現場にも絶対おすすめ！安心安全！というわけではない"
  と明記し、リスクにも言及している
- **既存デッキではこの記事はサムネイル画像のみで具体的な数値には触れていない。今回は「きっかけ」
  パートで実際の数値を紹介し、リアリティを持たせる。**

---

## 9. Third-party Runnerのリスク（既存デッキの整理を踏襲）

- **実行環境の差**: GitHub-hostedと完全に同じ環境とは限らない（今回の`setup-php`問題がまさにこれ）
- **Actionとの互換性**: 特定のActionで想定外の挙動が出ることがある
- **サービス障害への依存**: GitHubに加えてThird-party側の障害・可用性にも依存する
- **セキュリティ**: 自社コードやSecretsを外部サービスのRunner上で実行することになる

---

## 10. 既存デッキ（20260911-phptokyo.md）との差分方針

25〜30分版として今回追加・拡張する主なポイント:

1. **GitHub Actionsの基礎を厚くする**（Workflow/Job/Step/Runnerの関係を1枚使って説明）
   - 既存デッキは「Runnerとは」からいきなり入るが、バックエンド開発者向けにWorkflow全体の
     構造から丁寧に説明する
2. **Runnerの3種類（GitHub-hosted / Self-hosted / Third-party）を表で比較**
   - 既存デッキは「GitHub-hosted」と「Self-hosted（Blacksmithなど）」の2択という粒度だが、
     公式ドキュメントに基づき、Self-hostedとThird-partyを明確に区別して説明する
3. **コストの考え方（Runnerの単価 × 実行時間）を1枚で明示**
   - 既存デッキには存在しないパートを追加
4. **きっかけとなったZenn記事の実際の数値を紹介**
   - 既存デッキはサムネイルのみ。実測値（55分→23分、コスト約70%削減）を紹介し、
     「だから自分たちも試したくなった」という説得力を強める
5. **`setup-php`が遅くなる根本原因を技術的に掘り下げる**
   - 既存デッキの「Issue #1056に類似報告あり」という紹介から一歩進め、
     「事前ビルド済みキャッシュ vs apt都度インストール」という一次情報ベースの技術的説明を追加
6. **GitHub Actionsの料金体系（現在確定している範囲）を軽く紹介**
   - 未確定情報（platform fee等）は含めず、確認できた事実のみ（self-hosted無料、
     GitHub-hosted分単価）を紹介
7. 骨格（プロダクトA成功→プロダクトB失敗→原因調査→Third-party Runnerのリスク→
   導入/切り戻しの容易さ→まとめ）は既存デッキを踏襲する

### 10.1 追加ラウンド（36枚→38枚、約25分→約26〜28分）

25〜30分の枠にもう少し余裕を持たせるため、既存の一次情報から未使用だった部分を2枚追加した。
新規の裏取りは発生していない（すべて上記1〜9節の出典に基づく）。

1. **「Blacksmithが謳うメリット」を追加**（5節の内容を初めてスライド化）
   - 2倍高速なハードウェア／33%安い／キャッシュ4倍高速／コスト最大67%削減、を紹介
   - GitHub-hostedの分単価スライドの直後に置き、「単価の比較」という伏線を回収する位置に配置
   - 「あくまでBlacksmith公式の主張」という区別を必ず明言する（プロダクトBの悪化事例と矛盾して
     聞こえないようにするため）
2. **「実はBlacksmith固有の問題ではない」を追加**（7節の未使用情報をスライド化）
   - depot.dev・WarpBuildでの類似報告、`RUNNER_ENVIRONMENT`検出方法に関するPR #1069（未マージ）
   - 「今回の事象はBlacksmithが悪いのではなく、Third-party Runner全般のパターン」と一段抽象化し、
     話の一般性・信頼性を上げる。時間調整が必要な場合に削る候補としても位置づける

---

## 11. 3プロダクトの導入前後（2026-09-27 に Actions API で集計）

スライド上の呼び方（登壇ではこの名前だけ使う）:

- プロダクトA — 待ちもコストも大きく下がった Test
- プロダクトB — Unit Test と静的解析の両方が下がった
- プロダクトC — setup-php で全体が悪化し、見送り

スライドの結果は公式の試算ではなく、成功 run から取った実測。
コストは請求書の実額ではなく、ジョブ秒を1分へ切り上げ × 公開単価の推定。

- GitHub-hosted（private の `ubuntu-latest`、2 vCPU）: $0.006/分
- Blacksmith `blacksmith-2vcpu-ubuntu-2404`: $0.004/分
- Blacksmith `blacksmith-4vcpu-ubuntu-2404`: $0.008/分（プロダクトCの試行のみ。スライドの比較表には出さない）

待ちは対象ジョブの最長。Slack 通知など数十秒未満のジョブは除く。

| 対象 | 導入前 | 導入後（2vCPU） | サンプル |
|---|---|---|---|
| プロダクトA Test 待ち / コスト | 583秒 / $0.192（32分） | 236秒 / $0.056（14分） | 成功18 runずつ。前 2026-08-01〜08-25、後 2026-08-27〜09-27 |
| プロダクトB Unit Test | 447秒 / $0.048 | 242秒 / $0.020 | テストを実行した run。前11・後13 |
| プロダクトB 静的解析（待ち） | 194秒 / $0.060 | 106秒 / $0.024 | 前7・後8。Larastan が最長 |
| プロダクトC のテストジョブ | ジョブ69秒、本体38秒、setup-php 10秒 | ジョブ103秒、本体15秒、setup-php 78秒 | 2vCPU との比較。未マージでクローズ |

プロダクトCの3ジョブの従量は、2vCPU で $0.024 → $0.024（4分→6分）。4vCPU は $0.048。
phpstan・phparkitect の公式側の秒数はプロダクトCの測定メモ（40秒・26秒）で、どちらも1分以内なので切り上げ後の金額は変わらない。近くの公式 run でも 30秒・18秒だった。

## 参照した公式ドキュメント・一次情報一覧

1. About GitHub-hosted runners
   https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners/about-github-hosted-runners
2. About self-hosted runners
   https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners
3. GitHub Actions billing（料金体系）
   https://docs.github.com/en/billing/concepts/product-billing/github-actions
4. Blacksmith Pricing
   https://www.blacksmith.sh/pricing
5. shivammathur/setup-php README
   https://github.com/shivammathur/setup-php
6. shivammathur/setup-php Issue #1056（`gh issue view`で本文・コメント直接確認）
   https://github.com/shivammathur/setup-php/issues/1056
7. Zenn — YAMLを数行変えただけでGithub Actionsの料金を70%削減できて実行時間まで減った話
   https://zenn.dev/counterworks/articles/573954dcfa8bb6

## 情報源（ChatGPT共有セッション）

- <https://chatgpt.com/share/6a9ef218-befc-83e8-832f-35c0c8549711>
  （既存デッキ 20260911-phptokyo.md の元になった構成検討セッション。本メモはこのセッションの
  内容を踏まえつつ、数値・引用はすべて上記一次ドキュメントで再確認している）
