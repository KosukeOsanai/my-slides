# 調査メモ（20261125 PHP勉強会@東京 用）

発表テーマ（仮）: **なぜ `composer audit` をCIに入れるのか ― Composer 2.11 の cooldown まで**

- 持ち時間: **要確認**（ChatGPTセッションでは5分LT想定で構成案を作成）
- 一次ソースは 2026-11-12 時点で直接取得して確認済み（末尾「参照した公式ドキュメント」）
- Composer 最新は **2.11.2（2026-11-11）**。2.11.0 は 2026-10-29 リリース

### タイトル案（ChatGPTセッションより）

1. Composerの依存パッケージ、ちゃんと守っていますか？ ― auditとcooldownの話（ChatGPT推奨）
2. なぜ`composer audit`をCIに入れるのか ― Composer 2.11のcooldownまで（元テーマ維持）
3. そのComposerパッケージ、本当に安全？ ― auditと新機能cooldownで備える

### LTの核メッセージ

> 既知の問題を見つける `audit`（検出）と、公開直後のリスクを減らす `cooldown`（予防）。
> Composer標準の機能を組み合わせて依存パッケージを守ろう。

- **「依存を変えていなくても、使っているパッケージの安全性の情報は変わる」** → だからCIで継続的に audit する
- cooldown は「未知のマルウェアを検出する」機能ではなく「**検出されるまでの時間を稼ぐ**」機能

---

## 1. 自分の当初理解の答え合わせ

| 当初の理解 | 評価 | 正しくは |
|---|---|---|
| サプライチェーン攻撃で脆弱なパッケージの混入を防ぐため | △ | 「既知の脆弱性（正規パッケージのバグ）」と「悪意あるパッケージ（マルウェア）」は別物。audit は**報告済み**のものを両方検出（マルウェアは2.10〜） |
| 問題があれば exit 1 で CI が落ちる | ○ | 2.10.0 以降は 0 / 1 のみ。ただし `config.policy` で `audit: report` 等にすれば落とさない設定も可能 |
| `--locked` でバージョンを固定する | × | 固定するのは `composer.lock`。`--locked` は「vendor ではなく lock ファイルの内容を監査する」オプション |
| `composer.lock` のコミット必須 | ◎ | 公式 Basic usage に「Commit your composer.lock file to version control」 |
| `--no-dev` で本番依存に絞る | ○ | 仕様は正しい。ただし PHPStan 等の dev 依存も CI で実行されるので、CI では付けない方が安全（ChatGPTの意見） |

## 2. `composer audit` の仕様（公式 CLI ドキュメント）

- 依存ポリシー（セキュリティアドバイザリ等）に照らして監査するコマンド。Composer **2.4.0（2022-08-16）** で追加
- 検出対象: **脆弱性アドバイザリ / abandoned パッケージ / マルウェア / カスタムポリシー**
- 終了コード: `0` 問題なし / `1` ポリシー該当 or 必要パッケージ不足
- 主なオプション
  - `--locked`: vendor ではなく lock ファイルのパッケージを監査（`composer install` 不要で回せる）
  - `--no-dev`: require-dev を除外
  - `--direct (-D)`: 直接依存のみ監査（**2.11 で追加**）
  - `--format`: table / plain / json / summary
  - `--abandoned`: ignore / report / fail
  - `--ignore-severity`, `--ignore-unreachable`
- `composer install --audit` でインストール後に監査も可能
- アドバイザリ取得元: Packagist.org Security Advisory API。元データは **FriendsOfPHP/security-advisories と GitHub Advisory Database**（Packagistブログ 2024-10-09）
- → **未報告の脆弱性・未検出のマルウェアは検出できない**（cooldown への橋渡しポイント）

### 終了コードの変遷（CHANGELOG）

| バージョン | 変更 |
|---|---|
| 2.7.0（2024-02-08） | `audit.abandoned` のデフォルトが `fail` に（abandoned でも非0） |
| 2.8.4（2024-12-11） | 終了コード: 1=脆弱性 / 2=abandoned / 3=両方 |
| **2.10.0（2026-05-28）** | **BC Break: 常に 0 か 1** |

- ※ Packagistブログ（2024-10-09）の「アドバイザリ件数を終了コードで返す」は旧仕様。スライドでは引用しない

## 3. なぜ CI に入れるのか

### Composer 自体の防御機能（デフォルト挙動・2.10 ブログ）

| 対象 | update/require 時 | install 時 | audit |
|---|---|---|---|
| マルウェア | ブロック | **ブロック**（lock 後に判明しても次の install で失敗） | fail |
| 脆弱性アドバイザリ | ブロック（2.9.0〜 `block-insecure` デフォルト true） | インストール可 | fail |
| abandoned | ブロックしない | ブロックしない | report のみ（※2.10ブログの記述。CLIの`--abandoned`デフォルトは要実機確認） |

→ 問い: **「Composer自体が守ってくれるのに、なぜ CI で audit を回すのか？」**

### 答え

1. **lock 済みの依存に後から脆弱性が公表される**。脆弱性アドバイザリは install 時にはブロックされない（「影響を評価してから判断する機会を与える」設計）
2. `composer update` は毎日走るわけではない → 依存を触らない期間の新規公表に気付けない
3. CI で audit を回せば exit 1 でビルドが落ち、気付ける
4. PR 時だけでなく **定期実行（schedule）** も併用すると、コード変更がない期間もチェックできる

### タイムライン例（説明用の仮想例）

- 11/1 `example/package` 1.2.0 導入（既知脆弱性なし）
- 11/5 1.2.0 に脆弱性が公表（自分たちは何も変更していない）
- 11/6 CI の audit が照会 → 1.2.0 が脆弱と判明 → CI 失敗 → 対応

### lock ファイルの限界（Packagist 2026-05-27 記事）

- install は lock を再現するだけ。`update` / `require` を叩いた瞬間にメタデータを取り直して lock を書き換える
- lock は「意図しない新バージョンを避ける」には有効だが、「既知の問題を知らせる」ことはしない → **lock + audit の組み合わせ**

## 4. CI 導入例（GitHub Actions）

```yaml
on:
  pull_request:
  schedule:
    - cron: '17 1 * * *'   # 毎日 01:17 UTC
  workflow_dispatch:

# ... PHP / Composer セットアップ後
- name: Composer Audit
  run: composer audit --locked
```

- ChatGPT案では `composer --no-plugins audit --locked`（監査ジョブでプラグインを動かさない意図）
- 注意: 「schedule はデフォルトブランチで実行」は GitHub Docs 未確認（**TODO: 登壇前に確認**）
- 監査が落ちても本番が自動で直るわけではない → 誰が対応するか等の運用も必要

## 5. Composer 2.11 の cooldown（メインの見せ場）

### 背景（2.11 リリース記事 / 2026-05-27 記事）

- 2026年の PHP 界隈の実例: **intercom/intercom-php（4/30）**、**laravel-lang（5/22）**。乗っ取った GitHub アカウント・盗んだトークンで正規パッケージに悪意あるタグを公開
- 2.10 のマルウェアポリシーは「**フラグが立った後**」にしかブロックできない → 公開〜フラグまでの**空白時間**がある
- cooldown（別名 minimum release age）はこの空白を狭める
  - 自動スキャナは公開後**数分**で検出し得る → **1時間でも効果あり**
  - 手動レビューが必要な報告はもっとかかる → **数時間〜1日**が現実的
  - 「cooldown は悪意あるリリースが間に合って検出されることを保証しない。ただし1時間遅らせるごとに確率は上がる」

### 仕組み

- 新バージョンが**公開されてから指定期間が経過するまで、依存解決の候補から除外**する
  - 当初理解「アップデート後n日経つまで入れない」→ 主語は「自分のアップデート」ではなく「**パッケージの公開**」
- **デフォルト無効**。`config.policy.cooldown` で設定

```json
{
  "config": {
    "policy": {
      "cooldown": {
        "period": "1 day"
      }
    }
  }
}
```

- `period`: `"6 hours"` のような文字列（second / minute / hour / day / week）または秒数。グローバル設定、環境変数 `COMPOSER_POLICY_COOLDOWN_PERIOD` でも可（CI 向け）
- 効くのは **update / require**（依存解決時）。**`composer install` は lock の内容をそのまま入れる**
- 部分 update では対象外の lock 済みパッケージは触らない。full update では cooldown 中の lock 済みバージョンが古い版に戻ることがある
- dev 版（dev-main 等）・プラットフォームパッケージは対象外

### なぜ 2.10 で入らなかったか（＝ 2.11 の肝）

- 従来の `time` フィールドはタグのコミット日時 or composer.json 由来 → **公開者（攻撃者）が改ざん可能**（数週間前に遡らせればすり抜ける）
- Packagist.org が自分で記録する **`published-time`** を全バージョンに付与（composer/packagist#1765）
- published-time を返さないリポジトリだとコマンドが失敗する（黙って無効化されない）。`require-published-time: false` で time にフォールバック可

### 注意点

- **セキュリティ修正版にも cooldown がかかる**（1日設定なら修正版も1日入らない）
- アドバイザリを根拠に自動で除外しない理由: 乗っ取った攻撃者はアドバイザリ自体も出せる → 抜け道になる
- 回避: `composer update --no-cooldown vendor/package`（cooldown だけをスキップ。脆弱性・マルウェア等の他ポリシーは有効のまま。`--no-blocking` とは違う）
- 恒久除外: `ignore`（例: `"mycompany/*": "We trust the code in our own packages"`）
- 期間を長くするほど、気付いていない脆弱性の修正適用も遅れる

### cooldown を audit に効かせる: `policy.cooldown.audit`

- 2.11.0 スキーマで確認: `audit` = `ignore`（**デフォルト**）/ `report` / `fail`
- 2.11.0 の `Auditor.php` で確認: `fail` のとき cooldown 中パッケージがあれば監査結果が FAILED（exit 1）
- **設定ドキュメント本文には記載なし**（スキーマ・ソースのみ）→ 登壇で触れるなら **TODO: 2.11 で report / fail の実機確認**

```json
{ "config": { "policy": { "cooldown": { "period": "1 day", "audit": "fail" } } } }
```

- 導入初期は `report` で可視化 → 運用が固まったら `fail`（ChatGPTの意見）
- `fail` だと緊急の修正版を lock に入れた直後も CI が落ちる。期間経過で自然に解消

### audit と cooldown の対比

| | `composer audit` | `cooldown` |
|---|---|---|
| 目的 | 既知の問題を**検出** | 公開直後のバージョンを**避ける** |
| タイミング | CI・定期実行・手動 | update / require（依存解決時） |
| 判断材料 | アドバイザリ・マルウェア報告 | 公開時刻（published-time） |
| 効果 | 問題があれば exit 1 | 新バージョンの選択を一時保留 |

- cooldown の限界: 期間内に検出されなかったマルウェアは入り得る / 以前からある悪意版には無効 / lock からの install には効かない

## 6. 構成案（持ち時間5分）

前提: 過去の5分デッキ（20260930、全24枚）の型に合わせる。
タイトル → 問いかけ（message）→ 持ち帰ってほしいこと → 本編 → まとめ → 締め（message）→ 告知・自己紹介・References は投影のみ。
1分あたり約300字で話す想定。本編に使えるのは実質4分弱。

ChatGPT案（auditとcooldownを同じ比重で7枚）は約6分かかるので不採用。以下の2案を比べる。

### 案A: cooldown が主役（audit は前振り）

タイトル案: **Composer 2.11 の cooldown ― audit では間に合わない「公開直後」から守る**

| # | タイトル | 役割 | 開始 |
|---|---|---|---|
| 1 | タイトル | | 0:00 |
| 2 | 「`composer audit` をCIに入れていれば、乗っ取られたパッケージも防げる？」 | 問いかけ | 0:08 |
| 3 | 今日持ち帰ってほしいこと | 結論を先に | 0:20 |
| 4 | `composer audit` とは | 報告済みの脆弱性やマルウェアを検出し、exit 1 を返す | 0:30 |
| 5 | audit は「報告済み」しか止められない | 転換点 | 0:50 |
| 6 | 2026年に実際に起きた攻撃 | intercom-php（4/30）、laravel-lang（5/22） | 1:10 |
| 7 | 公開から検出までの「空白時間」 | 図 | 1:30 |
| 8 | Composer 2.11 の cooldown とは | 公開から一定期間は候補にしない | 1:50 |
| 9 | タイムラインで見る cooldown | 10:00 公開 / 11:00 update / 13:00 検出 | 2:10 |
| 10 | 設定はこれだけ | `"period": "1 day"` | 2:35 |
| 11 | 効くのは update / require だけ | install は lock の内容どおり入る | 2:55 |
| 12 | なぜ 2.10 では入れられなかった？ | `time` は改ざんできる → `published-time` | 3:15 |
| 13 | 注意：セキュリティ修正版も待たされる | `--no-cooldown`、`ignore` | 3:40 |
| 14 | 期間はどれくらい？ | 1時間でも効果あり、数時間〜1日が現実的 | 4:00 |
| 15 | まとめ | audit は検出、cooldown は予防 | 4:15 |
| 16 | 締めの message | 「`period` を1行足すところから」 | 4:35 |
| 17〜 | 告知・自己紹介・References | 投影のみ | 4:45 |

- 良い点
  - 1か月前（10/29）にリリースされたばかりで、知らない人が多い
  - 実際の攻撃事例 → 空白時間 → cooldown と、話が一本でつながる
  - 「なぜ 2.10 で入れられなかったか」は技術的に面白い
  - 一次ソースで裏が取れていて、実機確認が必須の内容がない
- 懸念
  - 元のテーマ「なぜCIに入れるのか」はほぼ消える（audit は2枚だけ）
  - cooldown は CI の話というより、update する人（開発者や Renovate/Dependabot）の話になる
  - 「install には効かない」「修正版も待たされる」など注意点が多く、1枚あたりの情報が詰まりやすい

### 案B: audit が主役（cooldown は最後に紹介）

タイトル案: **Composer が守ってくれるのに、なぜ `composer audit` を CI に入れるのか**

| # | タイトル | 役割 | 開始 |
|---|---|---|---|
| 1 | タイトル | | 0:00 |
| 2 | 「Composer は脆弱なバージョンもマルウェアもブロックしてくれる。じゃあ audit はいらない？」 | 問いかけ | 0:08 |
| 3 | 今日持ち帰ってほしいこと | 結論を先に | 0:20 |
| 4 | Composer はすでに守ってくれる | 2.9 で脆弱版を update 時にブロック、2.10 でマルウェアを install 時もブロック | 0:30 |
| 5 | でも脆弱性は install ではブロックされない | 「影響を評価してから判断」という設計 | 0:55 |
| 6 | lock 済みの依存に後から脆弱性が公表される | タイムライン（11/1 導入 → 11/5 公表） | 1:15 |
| 7 | update しない日にも気付きたい | だから CI | 1:40 |
| 8 | `composer audit --locked` | lock を監査する（バージョンを固定するのは lock 自身）、exit 1 | 2:00 |
| 9 | GitHub Actions に入れる | PR ＋ schedule の YAML | 2:25 |
| 10 | 落ちたら誰が直す？ | 運用の一言 | 2:50 |
| 11 | それでも audit は「報告済み」しか見えない | cooldown への橋渡し | 3:10 |
| 12 | Composer 2.11 の cooldown | 仕組みと設定を1枚で | 3:30 |
| 13 | audit と cooldown の役割分担 | 比較表 | 3:55 |
| 14 | まとめ | | 4:15 |
| 15 | 締めの message | 「`composer audit --locked` を1行足すところから」 | 4:35 |
| 16〜 | 告知・自己紹介・References | 投影のみ | 4:45 |

- 良い点
  - 元のテーマどおりで、問い（「Composer が守ってくれるのになぜ？」）に答える形になっている
  - 持ち帰ってすぐ試せる（YAML 1ステップ）
  - 「install では脆弱性はブロックされない」という設計を知らない人が多そう
- 懸念
  - audit 自体は 2022 年からある機能で、知っている人には目新しさが薄い
  - cooldown は1枚の紹介だけ。published-time や注意点まで話せない
  - GitHub Actions の schedule 仕様と、abandoned の扱いは確認が必要（7章 TODO）

### 比較

| 観点 | 案A（cooldown 主役） | 案B（audit 主役） |
|---|---|---|
| 新しさ | ◎ リリース1か月 | △ 2022年からある機能 |
| 持ち帰ってすぐ使える | ○ `composer.json` に1行 | ◎ CI に1ステップ |
| 話の一貫性 | ◎ 攻撃事例 → 空白時間 → cooldown | ○ 問い → 答え → 補足 |
| 元のテーマ（CI） | × ほぼ消える | ◎ |
| 5分に収まるか | ○ 注意点を削れば余裕 | ○ |
| 登壇前の確認 | 少ない | GitHub Docs と実機確認が必要 |

- どちらの案でも、もう一方のテーマは別の発表（10分枠や次回の勉強会）に回せる

## 7. 登壇前TODO

- [ ] 持ち時間の確認
- [ ] Composer 2.11 で `composer audit --locked` の出力・exit code を実機キャプチャ
- [ ] `policy.cooldown.audit: report / fail` の挙動を実機確認
- [ ] GitHub Actions の schedule 仕様（デフォルトブランチで動く）を GitHub Docs で確認
- [ ] 2.10 以降の abandoned の audit デフォルト（fail / report）を実機確認

---

## 参照した公式ドキュメント

- Composer CLI（audit）: <https://getcomposer.org/doc/03-cli.md#audit>
- Composer Config（policy / cooldown）: <https://getcomposer.org/doc/06-config.md#cooldown>
- Composer Basic usage（composer.lock をコミット）: <https://getcomposer.org/doc/01-basic-usage.md#commit-your-composer-lock-file-to-version-control>
- Composer CHANGELOG: <https://github.com/composer/composer/blob/main/CHANGELOG.md>
- composer-schema.json（2.11.0）: <https://github.com/composer/composer/blob/2.11.0/res/composer-schema.json>
- Auditor.php（2.11.0）: <https://github.com/composer/composer/blob/2.11.0/src/Composer/Advisory/Auditor.php>
- Composer 2.11（2026-10-29）: <https://blog.packagist.com/composer-2-11-release/>
- Composer 2.10 Release（2026-05-28）: <https://blog.packagist.com/composer-2-10-release/>
- An update on Composer & Packagist supply chain security（2026-05-27）: <https://blog.packagist.com/an-update-on-composer-packagist-supply-chain-security/>
- Discover Security Advisories with Composer's audit command（2024-10-09）: <https://blog.packagist.com/discover-security-advisories-with-composers-audit-command/>
- Packagist Security Advisories: <https://packagist.org/security-advisories/>

## 情報源にした ChatGPT セッション

- <https://chatgpt.com/share/6af5a725-5668-83ee-aa0b-d5ff10a884fb>
