---
marp: true
theme: my-slideshow-theme
paginate: false
---

<!-- _class: title -->

# Pestを導入して機能を活用しよう<br>〜主にCI最適化を例に〜

2026/09/24 第58回関西PHP勉強会

おさない

---

# このセッションで持ち帰って欲しいこと

* Pestは検証・導入を容易にできる
  * PHPUnitのコードベースのまま実行環境だけをPestにすることも可能
* テストを最適化するための多様な機能が公式から提供
  * PHPUnit記法のまま使える拡張も多数
  * CIの最適化以外にも「便利な機能」が公式から提供

※しゃべらないこと：Pestの詳細な記法について等

---

# Pestとは

* "The elegant testing framework for PHP developers and AI agents."
  * 関数ベースの記法、expectation API
* <a href="https://pestphp.com/">https://pestphp.com/</a>

```php
// Pest
it('performs sums', function () {
    expect(sum(1, 2))->toBe(3);
});
```

```php
// PHPUnit
public function test_performs_sums()
{
    $this->assertSame(3, sum(1, 2));
}
```
---

# Pestの特徴

1. 自然言語に近い構文
2. PHPUnitからの段階的移行が可能
3. テストを便利にする多様な機能が本体や公式プラグインに内包

※このセッションは2,3について触れます

---

# PHPUnitからの段階的移行

* Pest上でPHPUnit構文のテストを実行できる
  * *Pest is built on top of PHPUnit*
* PHPUnit → Pest への移行を補助する公式プラグイン
  * `pestphp/pest-plugin-drift`

<!--
「Pest化」と「ランナー導入」は別です。
built on top of PHPUnit なので、extends TestCase のまま ./vendor/bin/pest で動きます。
Drift がクラスから Pest 記法への変換です。Rector は移行そのものではなく、Pest の記法整理とメジャー間アップグレードです。
-->

---

# テストを便利にする機能が本体や公式プラグインに内包

* **テスト最適化**: `--parallel` / `--shard` / `--profile` / `--compact`
* **コード品質**: Mutation Testing（`--mutate`）、Architecture Testing（`arch()`）など
* **拡張**: Laravel / PHPStan / Rector / E2E など

<!--
Pestは記法だけの薄いラッパではありません。
入れてしまえば、速さと質の両方に手を伸ばせます。
-->

---

# Pest導入からCI最適化機能活用までの手順

1. Pestをエンジンとして導入する
2. CIを `./vendor/bin/pest --ci` に差し替える
3. 最適化機能を足す

---

# 1. Pestの導入

* <a href="https://pestphp.com/docs/installation">https://pestphp.com/docs/installation</a>
* 最新のPest 5は PHP 8.4 以上が必要


---

# 1. Pestの導入

* 依存関係の導入
```bash
composer remove phpunit/phpunit
composer require pestphp/pest --dev --with-all-dependencies

```

* Pestの初期化、実行
  * PHPUnitの既存テストケースはそのまま実行可能
 
```bash
./vendor/bin/pest --init
./vendor/bin/pest
```

<!--
phpunit/phpunit を外して pest と Laravel プラグインを入れ、--init で tests/Pest.php を作ります。
pest:install は使いません。既存の extends TestCase はこのままで動きます。
-->

---

# 2. CIのコマンドの置き換え

* Continuous Integration > Exampleを参照に.ymlを追加
  * <a href="https://pestphp.com/docs/continuous-integration">https://pestphp.com/docs/continuous-integration</a>

* GHAでPHPUnitを置き換える場合、`run` を置き換える

<div class="two-col">
<div>

PHPUnit

```yaml
- name: Tests
  run: ./vendor/bin/phpunit
```

</div>
<div>

Pest

```yaml
- name: Tests
  run: ./vendor/bin/pest --ci
```

</div>
</div>

<!--
公式 Continuous Integration の GitHub Actions 例は、最後のステップが ./vendor/bin/pest --ci です。
PHPUnit からの差分は、この run の1行です。--ci はフルスイートを走らせるフラグで、--tia は付けません。
-->

---

# 3. Pest テスト最適化機能の活用

* テストを最適化するための機能がPestに内包
  * <a href="https://pestphp.com/docs/optimizing-tests">https://pestphp.com/docs/optimizing-tests</a>

```text
並列化する
├─ Parallel Testing
└─ Test Sharding（Time-Balanced Sharding）

ボトルネックを把握する
└─ Profiling

失敗に集中する
└─ Compact Printer
```

<!--
公式の Optimizing Tests に並ぶ4手法です。
parallel / shard が実行時間そのものを縮める本命。
compact は失敗に集中するプリンタで、速度効果は公式どおり数ミリ秒。
profile は遅いテスト Top 10 を出す診断です。
TIAは本流CIには付けない（公式）。今日は Optimizing Tests の4手法に絞る。
-->

---

# Parallel Testing

* 同じ実行環境上で、テストを複数のプロセスで並列実行させる
 * PHPUnitにおけるParaTestのイメージ
* テストの実行時間を短縮できる

```bash
./vendor/bin/pest --parallel
```

```text
Test A → Test B → Test C → Test D
↓
Test A ─┐
Test B ─┼→ 同時実行
Test C ─┤
Test D ─┘
```

<!--
いちばん足しやすいのがparallelです。
同じ実行環境の中で複数プロセスを起動します。
プロセス数はCPUコア数に合わせて自動でも、--processes で指定もできます。
-->

---

# Test Sharding

* CIでのテスト実行時、テストを複数のCIジョブに分割
 * GitHub ActionsのMatrixのようなイメージ
* テストの実行時間を短縮できる可能性がある
```bash
./vendor/bin/pest --shard=1/4
```

```text
Test Suite → CI #1 (1/4)  CI #2 (2/4)  CI #3 (3/4)  CI #4 (4/4)
```
<!--
parallelの次です。CIジョブを増やしてスイートを分けます。
コマンドは何分割中の何番目かだけです。
-->

---

# Time-Balanced Sharding

* デフォルトの `--shard` は**テストファイル数**で分割する
  * 特定のファイルに遅いテストがあると、テスト全体実行完了が遅くなる
* 過去の**実行時間**でCIジョブを分割するTime-Balanced Sharding
  * CIジョブのボトルネックを最小限に抑えることができる

```bash
./vendor/bin/pest --update-shards
./vendor/bin/pest --shard=1/4
```

`tests/.pest/shards.json` をコミットすると、`--shard` は時間ベースになる

<!--
--update-shards で時間を記録し、shards.json をリポジトリに入れます。
コメントをコマンドに混ぜない。記録後の --shard は自動で時間ベースです。
--parallel との併用も公式どおり可能です。
-->

---

# Profiling

* 実行時間を計測し、時間がかかっているテストを表示する
* 遅いテストを特定、最適化の手がかりになる

```bash
./vendor/bin/pest --profile
```

```bash
Tests:      100 passed (153 assertions)
Duration:   11.68s

Top 10 slowest tests: 
Tests\Feature\UserTest > create user 6.27s
Tests\Feature\OrderTest > create order 4.91s
Tests\Feature\ProductTest > create product 0.24s
...
(98.88% of 11.68s) 11.55s
```

<!--
profile は高速化そのものではなく、ボトルネック調査です。
数字は公式 Optimizing Tests の出力例です。
遅い2件でスイートの大半を占めている、という読み方をします。
-->

---

# Compact Printer

* 失敗したテストだけを表示させる
* 出力が単純になるので、I/Oが減り数ミリ秒速くなることもある

```bash
./vendor/bin/pest --compact
```

```

→ ./vendor/bin/pest --compact
 
⨯ ·············································································
·······································
 
  FAILED  Tests\Unit\ExampleTest > that true is true
  Failed asserting that true is false.
 
at tests/Unit/ExampleTest.php:4
 <?php

 ```

<!--
公式 Optimizing Tests の4つ目です。
主目的は失敗に集中すること。速度効果は公式が「a few milliseconds」と書いています。
CIを大きく速くする本命ではない、と一言添えます。
-->

---

# 組み合わせるとこうなる

4ジョブに分ける（それぞれ 1/4〜4/4）

```bash
./vendor/bin/pest --ci --parallel --compact --shard=1/4
```

※ ジョブごとに番号を変える。`1/4` の1ジョブだけではスイートの 4 分の 1
※ `--update-shards` は記録用。毎回は付けない
※ `--profile` は診断用。日常CIには付けない

<!--
見せるコマンドは parallel と shard の併用です。公式の Sharding 例と同じ組み合わせです。
4ジョブに 1/4 から 4/4 を割り当てます。1ジョブだけで 1/4 だと、その分割分しか走りません。
--ci で、そのジョブの対象をフルに走らせる。compact は出力だけ。
profile と tia と update-shards は用途が違うので、この行には足さない。
-->

---

# 補足　Parallel,shardにおける注意点

* テストが分離・独立していないと失敗する場合がある
  * テスト間でのデータベースや外部リソースの競合がある場合
  * テストが実行順序に依存している場合
* 小規模なテストだとオーバーヘッドで逆に遅くなることも

--- 
# 補足 TIAモード

* TIA：変更で壊れ得るテストだけを再実行する
  * Pest5の目玉機能
  * >  The TIA engine is a game-changer for test speeds. Laravel Cloud's test suite of 19,000+ tests went from 3 minutes to 5 seconds:

* 下記2点の理由からTIAは本セッションのスコープ外
  * CI上では--tiaモードを使わないことを強く推奨
  * --tiaモードの利用にはpestのfunctional記法への書き換えが必要

<!--
TIAは、変更の影響を受けるテストだけを再実行する機能です。公式はローカル向けと書いています。
CIのテスト実行コマンドに --tia は付けない、が今日の補足です。手順や数字には入りません。
-->

---

# まとめ

* Pestは検証・導入を容易にできる
* テストを最適化するための多様な機能が公式から提供
* 「次は、Pestの導入から、始まる」 


<!--
公式の手順を復唱して閉じます。
-->

---

<!-- _class: promo -->

# PHPカンファレンス関西2026開催

* スポンサー募集中！
* プロポーザル、リクエストーク絶賛募集中！

![PHPカンファレンス関西2026](./images/phpcon-kansai-2026.jpeg)

https://2026.kphpug.jp/

---

<!-- _class: promo -->

# 新企画「リクエストーク」

* PHPカンファレンス関西2026で「聞きたいトーク」を聞かせてください
* 「聞きたい！」をプロポーザル出したい方にお届けします！
* 「新たなコミュニティへの携わり方」を作ります！

![リクエストーク](./images/phpcon-kansai-request.jpeg)

---
# 今年もプロポーザル作成ワークショップやります！

* 参加者募集開始！
* https://phpkansai.connpass.com/event/407721/

![リクエストーク](./images/image.png)

---

<!-- _class: profile -->

# 自己紹介

![profile](../../themes/my-sns-icon.jpg)

<div class="profile-body">

<p class="profile-name">おさない</p>

<p class="profile-handle">Twitter: @000sak000</p>

</div>

---

<!-- _class: promo -->

# PHPカンファレンス愛媛2026

* 2026/10/03(土) 愛媛県松山市で開催！  
* チケット発売中！
* （ここで、実行委員長のひがきさんからのありがたいお話）

![PHPカンファレンス愛媛2026](./images/phpcon-ehime-2026.png)

https://phpcon.ehime.jp/

---

<!-- _class: promo -->

# PHPカンファレンス新潟2026
* 2026/11/14(土) 新潟県新潟市で開催！
* チケット販売中！当日スタッフ募集中！

![PHPカンファレンス新潟2026](./images/phpcon-niigata-2026.png)

https://phpcon.niigata.jp/

---

<!-- _class: promo -->

# phper x 日本酒の会 #8 in 関西
* 2026/10/23(土) 大阪で開催！
* 参加者募集中！
* https://phponshu.connpass.com/event/406131/

![PHPカンファレンス新潟2026](./images/45b85a2a88c6def98a484bceb98afc59.png)
