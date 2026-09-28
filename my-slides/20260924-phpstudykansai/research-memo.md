# Pest 調査メモ（20260924-phpstudykansai 用）

発表テーマ: Pestについての概説 ＋ Pestの機能を使ってCIでのテスト実行時間を最適化した話

> **note**: 当初共有されたX (Twitter) の投稿はPestと無関係な内容でしたが、
> 改めて以下2つのChatGPT共有セッションを頂き、内容を確認しました。
> - <https://chatgpt.com/share/6a9edf60-78e0-83e9-a06c-ba8793cde716>（Tia EngineとCI / Pestの一般的な導入メリット）
> - <https://chatgpt.com/share/6a9ee3bb-f668-83ee-a814-7b6d40d3ffeb>（Pest parallel機能の説明 / LT構成の検討）
>
> 実はこの2つ目のセッションの検討内容が、既存の `20260924-phpstudykansai.md`
> （PHPStanの枕→Pestとは→PHPUnit資産の活用→parallel/shard/Time-Balanced Sharding→
> まとめ、という構成）の元になっていたことが判明しました。以下のメモは、
> この2つのセッションおよびPest公式ドキュメントの両方を情報源として、
> 内容を整理・裏取りしたものです。

---

## 0. 枕（PHPStan 2.2.6）の裏取り

スライド冒頭で使うCOLOPL Tech Blogの記事を直接確認した結果（レビューで実施）。

- 記事: [PHPStan 爆速化！静的解析ツール PHPStan 2.2.6 を実プロジェクトで計測してみた](https://blog.colopl.dev/entry/2026/07/28/162136)（COLOPL Tech Blog, 2026/07/28）
- 実測値（キャッシュ**なし**、2.1.32比）
  - PHPStan 2.2.6（Turbo OFF/JIT OFF）: 855.5秒 → 436.5秒（+49.0%）
  - PHPStan 2.2.6（Turbo ON/JIT ON）: → 290.5秒（+56.6%、Turbo単体効果は+21.8%）
- 実測値（キャッシュ**あり**、2.1.32比）
  - PHPStan 2.2.6は**逆に遅くなる**（-65.8%〜-75.9%）。Turbo/JITを有効にしても改善幅はごく僅か
- 記事の結論: 「開発用ツールでありバージョンアップが本番環境に影響しないため、積極的にバージョンアップすべき」
- **メモとして重要**: 当初「バージョンアップだけで10〜30%程度高速化できる余地」という表現を使う想定だったが、
  記事の実測値を直接確認したところこの数字は裏付けが取れなかった（キャッシュ無しなら最大+60%程度、
  キャッシュありだと逆に遅くなる、という条件依存の結果だった）。**スライドの表現は「条件次第では
  50%以上速くなるケースも／キャッシュ利用時は逆に遅くなるケースもあり要注意」に修正済み**

---

## 1. Pestとは何か

- キャッチコピー: **"The elegant testing framework for PHP developers and AI agents"**
- PHPUnit の上に構築されたテストフレームワーク（**"Pest is built on top of PHPUnit"**）
  - 別物ではなく、PHPUnitの資産（既存テストコード）をそのまま実行できる
- Functional Syntax（`test()` / `it()` + `expect()`）で簡潔にテストを書ける
- 主な数字（pestphp.com 公表値）
  - ダウンロード数: **70,000,000+**
  - GitHub Star: **12,000+**
  - プラグイン数: Why Pest の現行文言は **"Dozens of optional plugins"**（数十）。今回開いたホームページと Why Pest では **60+** は確認できなかった。スライドでは「数十」と書く
  - コントリビューター: **300+**
- 最新メジャーバージョンは **Pest 5**（PHP 8.4+ が必須）
  - Pest 4 では Browser / Visual / Device / Smoke テストなどフルスタックなテストが統合された
  - Pest 5 では TIA（Test Impact Analysis）、Agent Plugin、Evals など「AIエージェント時代」を意識した機能が追加

---

## 2. 導入・PHPUnitからの移行

### 2.1 インストール（テストランナーとして導入）

```bash
composer remove phpunit/phpunit
composer require pestphp/pest --dev --with-all-dependencies
./vendor/bin/pest --init   # tests/Pest.php が生成される
./vendor/bin/pest
```

- Laravel の場合は追加で Laravel プラグインを入れる
  ```bash
  composer require pestphp/pest-plugin-laravel --dev
  php artisan pest:install
  ```
  - `pestphp/pest-plugin-laravel` v5系は `PHP ^8.4` / `Laravel ^13.23.0` が必要
  - Artisanコマンド追加（`pest:test`、`pest:dataset` 等）、`actingAs` / `get` / `post` / `delete` などの名前空間関数を提供

### 2.2 既存PHPUnitテストはそのまま動く

- クラスベースの既存PHPUnitテスト（`extends TestCase`）は、コードを一切変更せずに
  `./vendor/bin/pest` で実行できる
- 「PestPHPへの書き換え」と「Pestをテストランナーとして導入」は別の話、というのが要点

### 2.3 Functional Syntaxへの自動変換（Drift）

- 既存PHPUnitテストをPestのFunctional Syntaxへ変換する公式プラグイン
  ```bash
  composer require pestphp/pest-plugin-drift --dev
  ./vendor/bin/pest --drift
  # 特定ディレクトリだけ変換する場合
  ./vendor/bin/pest --drift tests/Helpers
  ```
- 変換例
  ```php
  // Before (PHPUnit)
  class ExampleTest extends TestCase
  {
      public function test_that_true_is_true(): void
      {
          $this->assertTrue(true);
      }
  }

  // After (Pest)
  test('true is true', function () {
      expect(true)->toBeTrue();
  });
  ```
- 大部分は自動変換されるが、**手動での調整・検証が必要な場合がある**（完全自動ではない）
- 今回の発表スコープでは「書き換え」自体が主目的ではなく、CI高速化のための土台として紹介する位置づけ

---

## 3. CIのテスト実行時間を最適化する機能（本編の中心）

> **歴史の補足**: `--parallel` はPest 4で新規に入った機能ではなく、Pest 2.0（18ヶ月・
> 500コミット超の開発を経てリリース）の時点で並列実行速度が最大80%向上するなど
> 大幅に改善されている（Announcing Pest 2.0）。Pest 4で新規に入ったのは `--shard`
> （Test Sharding）の方。TIAの歴史は後述（4節）。

### 3.1 `--parallel`（並列実行）

- デフォルトは**1プロセスで直列実行**。`--parallel` で複数プロセスに同時実行する
- 使い方
  ```bash
  ./vendor/bin/pest --parallel
  ./vendor/bin/pest --parallel --processes=10   # プロセス数を明示指定も可能
  ```
- 公式の挙動
  - 指定なしだと **CPUコア数ぶんのプロセス** を作る
  - Windows では WSL 端末を使うこと（Optimizing Tests に明記）
- 公式が挙げる並列実行時の注意点（原文の3点）
  1. **Database resources may not be shared between tests**: 各テストは他テストから独立していること
  2. **Test order may not be guaranteed**: 特定の実行順に依存しないこと
  3. **Tests may be affected by race conditions**: 共有リソースへの同時アクセスでレースコンディションが起き得ること
- 既存のCIジョブ構成をほぼ変えずに試せる、最も手軽な高速化策
- 万能に速くなるわけではない → 効果はテストスイートの設計次第

### 3.2 `--shard`（CIジョブへの分割）

- テストスイートを**複数のCIジョブ（マシン）**に分割して実行する機能（Pest 4で導入）
- 使い方
  ```bash
  ./vendor/bin/pest --shard=1/4   # 4分割のうち1番目を実行
  ```
- デフォルトでは「テストファイル数」でほぼ均等に分割される
- `--parallel` と組み合わせ可能（Pest v4 の Test Sharding。**複数ジョブ**に 1/4〜4/4 を割り当てる）
  ```bash
  ./vendor/bin/pest --parallel --shard=1/4
  ```
- 1ジョブの日常CIに `--shard=1/4` だけを付けると、スイートの約 4 分の 1 しか走らない。1ジョブなら `--shard` は付けない

| | `--parallel` | `--shard` |
|---|---|---|
| 分割単位 | プロセス | CIジョブ |
| 実行場所 | 1つのCI（1マシン） | 複数のCI（複数マシン） |
| メリット | 手軽・既存CIで試しやすい | CI全体を大きく並列化できる |
| コスト面 | 追加インフラ不要 | CIジョブ（マシン）を増やす必要がある |

### 3.3 Time-Balanced Sharding（Pest 5で前面に出た機能）

- 課題: デフォルトの `--shard` はテスト**ファイル数**でほぼ均等分割する
  → テストごとの実行時間の差により偏りが出る（支払い処理・レポート生成などが遅いと、一番遅いshardの終了までCI全体が待たされる）
- Pest 5 Now Available の公式表現:
  > "Pest 4 introduced test sharding ... Pest 5 refines it with **time-balanced sharding**"
  - 過去の**実測実行時間**を基にシャードをバランスさせ、各シャードの壁時計時間がほぼ揃うようにする
- 沿革の精度（スライドではPest 5の公式表現に合わせ、詳細はここだけ）
  - `--shard` 自体はPest 4で導入
  - 時間ベース分散は Pest 4.6.0（2026-04-14）のリリースノートで `feat: time based sharding` として追加
  - Pest 5（2026-07-28）の発表記事で「Pest 4周期で熟成させて表に出した機能」の一つとして紹介
- 使い方
  ```bash
  ./vendor/bin/pest --update-shards
  # → 各テストクラスの実行時間を tests/.pest/shards.json に記録
  ./vendor/bin/pest --parallel --update-shards   # 公式どおり --parallel と併用可
  # shards.json をリポジトリにコミット
  ./vendor/bin/pest --shard=1/4
  # shards.json があるとき、--shard は自動的に時間ベースになる
  ```
- 時間ベースが有効なときの出力例（公式）
  - `Shard: 1 of 5 — 12 files ran, out of 50 (time-balanced).`
- 運用上の注意（Continuous Integration の "Keeping Shards Up to Date"）
  - ファイル追加: テストは走る。新規は均等分散、既知は時間ベース。警告あり
  - ファイル削除: 警告なし。古いtimingエントリは無視される
  - 既存ファイル内へのテスト追加: 警告なし
  - ファイルのリネーム: 警告あり（旧名は無視、新名は新規扱い）
  - `shards.json` 破損: 削除するか `--update-shards` で再生成するようエラーで止まる

### 3.4 Compact Printer（`--compact`）

公式 Optimizing Tests の4つ目の最適化手法。失敗したテストの情報だけを表示するプリンタ。

```bash
./vendor/bin/pest --compact
```

- 目的（公式の主旨）: 成功テストのノイズを消して、失敗に集中する
  - 原文: "instructs Pest to only display information regarding your test suite's failing tests"
- 速度への効果はごく小さい。公式は **「数ミリ秒速くなることもある」** と明記している
  - 原文: "since the `--compact` printer produces simpler output, test speed may improve by a few milliseconds, as there is less input/output required for each test"
- 常時有効にする設定（`tests/Pest.php`）
  ```php
  pest()->printer()->compact();
  ```
- CLI API Reference では Reporting カテゴリ（`--testdox` / `--teamcity` と同列の出力形式）
- → 「CI全体を大きく速くする」機能ではない。スライドでは「失敗に集中する」枠で扱い、速度効果は公式どおり数ミリ秒と伝える

### 3.5 Profiling（`--profile`）

公式 Optimizing Tests の2つ目。遅いテストを特定するための診断機能。

```bash
./vendor/bin/pest --profile
```

- 各テストの実行時間を集め、**最も遅いテスト Top 10** を表示する（CLI API: "Output to standard output the top ten slowest tests"）
- 公式ドキュメントの出力例（一次ソースに実在）
  - `Tests: 100 passed (153 assertions)` / `Duration: 11.68s`
  - `Tests\Feature\UserTest > create user` **6.27s**
  - `Tests\Feature\OrderTest > create order` **4.91s**
  - `Tests\Feature\ProductTest > create product` **0.24s**
  - `(98.88% of 11.68s) 11.55s`
- 使いどころ（公式）: 非効率なDBクエリや高価な処理を発見し、そのテスト自体を最適化する手がかりにする
- **高速化そのものではなく、ボトルネック調査**。並列化やShardの前の現状分析に使える
- PHPUnit形式のテストコードのままでも利用可能

---

## 4. TIA（Tia Engine / Test Impact Analysis）— 参考情報（本編スコープ外）

- Pest 5で追加された、**変更の影響を受けたテストだけを再実行する**エンジン
- 初回実行時にコードの依存関係グラフを記録し、以降は変更ファイルに関連するテストのみ実行、それ以外はキャッシュ結果を再生する
- 効果の例（公式ドキュメント`docs/tia`に実際に記載されている事例。原文: "A typical Laravel
  suite that used to take 10 minutes now replays in around 4 seconds."）
  - 通常10分かかるLaravelスイートが約4秒で完了（実行例: `774 passed, 7 affected,
    2 uncached, 765 replayed / Duration: 3.92s`）
  - ※「Laravel Cloudの19,000件超のテストが3分→5秒に短縮」という事例は、公式ドキュメント
    (`docs/tia` / `docs/pest5-now-available`) を直接確認したが**記載が見当たらなかった**ため、
    このメモでは採用しない（レビューで削除）
- 使い方
  ```bash
  ./vendor/bin/pest --tia
  ./vendor/bin/pest --parallel --tia
  ```
  - コードカバレッジドライバ（PCOV または Xdebug）が必須
  - Laravel / Symfony / Livewire / Browser など主要フレームワークの依存関係（マイグレーション、Bladeテンプレート、Inertiaページ、`config/`・`templates/`ディレクトリ等）を自動検出
- **重要な注意点**: 公式ドキュメント「The Tia Engine And CI」に明言されている通り、
  > "On CI, however, you should not pass the `--tia` flag to the command that runs your test suite."
  （CIでは、テストスイートを実行するコマンドに `--tia` フラグを渡すべきではない）
  - 通常のCIは常にフルスイートを実行すべき（`--ci` はそのためのオプション）
  - **唯一の例外**: チームで共有する「TIAのベースライン」を記録する専用ワークフロー
    （通常のテストパイプラインとは別物のジョブとして分離する）
  - TIAは**ローカル開発向け**の機能であり、通常のCIパイプラインにそのまま組み込む機能ではない
- 補足: TIAはPest 4で実験的に存在し、Pest 5で正式に公開された機能（"TIA was shipped
  quietly in Pest 4 ... The official, public launch is reserved for Pest 5."）
- → 今回の発表テーマ（CI全体のテスト実行時間の最適化）とは目的が異なるため、
  「こういう機能もあるが、CIの直接的な高速化策としては今回のスコープ外」という扱いにする
  （前回スライドの「TIAは今回は扱わない」の理由をより明確に補強できる情報）

---

## 5. PHPUnitのコードのままで使える機能・使えない機能

今回のテーマ（既存資産を変えずにCIを速くする）にとって重要な切り分け。

| Pestの機能 | PHPUnit形式のまま利用可 | 備考 |
|---|---|---|
| `--parallel` | ✅ | テスト並列実行 |
| `--profile` | ✅ | 遅いテストの特定 |
| `--shard` / `--update-shards` | ✅ | CIジョブ分割・Time-Balanced Sharding |
| `--tia` | ⚠️ 概ね可だが要検証 | PHPUnit形式でも依存グラフ自体は機能するはずだが、公式もFunctional testと全く同じ効き方をするとは限らないと示唆。またCIでの使用は非推奨（前述） |
| `--compact` | ✅ | 失敗だけ表示するプリンタ。速度効果は公式どおり数ミリ秒 |
| `--coverage` | ✅ | コードカバレッジ計測 |
| `--mutate`（Mutation Testing） | ⚠️ 要確認 | バージョン等により対応状況が異なる |
| Architecture Testing（`arch()`） | ❌ | Pest独自APIが必要 |
| Expectation API（`expect()`） | ❌ | Pest記法への書き換えが必要 |
| Dataset | ⚠️ | Pest記法中心（PHPUnitのData Providerとは別物） |

→ **今回扱う4手法（parallel / shard / compact / profile）は、いずれも
PHPUnit形式のテストコードのまま使える**、という点が今回のLTの核。

---

## 6. その他の主要プラグイン（概説パートで軽く触れる候補）

- **Laravel プラグイン**: Artisanコマンド追加、Laravelアサーション、`actingAs`/`get`/`post`/`delete` 等
- **Faker プラグイン**: `fake()` 関数でテストデータ生成、ロケール指定対応
- **Livewire プラグイン**: `livewire` 名前空間関数でLivewireコンポーネントをテスト
- **Browser プラグイン（`pest-plugin-browser`）**: Playwrightベースの実ブラウザテスト
- **Drift プラグイン（`pest-plugin-drift`）**: PHPUnit → Pest Functional Syntax の自動変換（前述）

---

## 7. 今回の発表への示唆（構成案のための整理）

1. **目的**: Pestをエンジンとして入れたあと、CI最適化機能を足すアプローチを共有する。記法移行は後回し。今日は公式ドキュメントに沿った理論・手順のみ
2. **概説パート**: Pestとは何か（PHPUnitベース／Functional Syntax／数字で見る採用状況）
3. **Pestの守備範囲を一度見せる**: CI高速化だけでなく、Mutation Testing（テストの検知力を検証）・Architecture Testing（設計ルールをテスト化）・豊富なプラグイン（Laravel/Faker/Livewire/Browser）もあることに触れたうえで、「今日はCI高速化にフォーカスする」とスコープを宣言する
4. **導入パート**: 既存PHPUnit資産を変更せずにPestで実行できること（テストランナーとしての導入）
5. **CI最適化パート（本編）**: 公式 Optimizing Tests の4手法を、公式の主旨どおりに分けて紹介する
   - `--parallel` → 手軽・同じ実行環境内の並列化（Pest 2から存在・改善）
   - `--shard` / Time-Balanced Sharding → CIジョブ自体の分割（Pest 4）＋実行時間ベース（Pest 5で前面化）
   - `--compact` → 失敗に集中するプリンタ。速度効果は公式どおり数ミリ秒なので、「CIを大きく速くする」枠には入れない
   - `--profile` → 遅いテスト Top 10。ボトルネックを把握する診断
6. **TIA**: ローカル開発向け。公式は「CIのテスト実行コマンドに付けるな」。本編では4手法に絞り、聞かれたら公式ルールだけ返す
7. **まとめ**: エンジン導入 → `--ci` → 公式の4手法を足す。自社実測・注意点の独立章は出さない

---

## 参照したPest公式ドキュメント

1. Pest ホームページ — 概要・特徴・数字
   https://pestphp.com/
2. Installation — インストール手順・要件
   https://pestphp.com/docs/installation
3. Migrating from PHPUnit Guide — PHPUnitとの関係・Driftによる自動変換
   https://pestphp.com/docs/migrating-from-phpunit-guide
4. Continuous Integration — `--parallel` / `--shard` / Time-Balanced Sharding
   https://pestphp.com/docs/continuous-integration
5. Pest 5 Now Available — Pest 5の新機能（Time-Balanced Sharding / Tia Engine / Agent Plugin）
   https://pestphp.com/docs/pest5-now-available
6. Tia Engine — Test Impact Analysisの仕組み・有効化方法・CIでの扱い（The Tia Engine And CI）
   https://pestphp.com/docs/tia
7. Plugins — 主要プラグイン一覧（Laravel / Faker / Livewire 等）
   https://pestphp.com/docs/plugins
8. Optimizing Tests — `--parallel` / `--profile` などテスト最適化の全体像
   https://pestphp.com/docs/optimizing-tests
9. CLI API Reference — `--parallel` / `--shard` / `--update-shards` / `--compact` 等のCLI仕様
   https://pestphp.com/docs/cli-api-reference
   （※ `--tia` はこのページのExecutionセクションには掲載されておらず、独立した「Tia Engine」ドキュメント側で説明されている）
10. Why Pest — Pestの基本的な特徴・導入メリット
    https://pestphp.com/docs/why-pest
11. Announcing Pest 2.0 — parallel / profileの改善の背景
    https://v3.pestphp.com/docs/announcing-pest2
12. Pest v4.6.0 リリースノート — time based sharding の追加（2026-04-14）
    https://github.com/pestphp/pest/releases/tag/v4.6.0

---

## 情報源（ChatGPT共有セッション）

- <https://chatgpt.com/share/6a9edf60-78e0-83e9-a06c-ba8793cde716> — Tia EngineとCIの関係、Pestの一般的な導入メリット、参考ドキュメントの整理
- <https://chatgpt.com/share/6a9ee3bb-f668-83ee-a814-7b6d40d3ffeb> — `--parallel`/`--shard`/Time-Balanced Shardingの整理、LT構成案の検討（既存スライドの元ネタ）
