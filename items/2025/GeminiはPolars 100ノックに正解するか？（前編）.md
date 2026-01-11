title: GeminiはPolars 100+ノックに正解するか？（前編）
tags: Python データ分析 AI Polars
url: https://qiita.com/SaitoTsutomu/items/c509d8391e61048897c7
created_at: 2025-09-21 23:24:18+09:00
updated_at: 2025-09-22 20:08:42+09:00
body:

## はじめに

Gemini 2.5 Proを用いて、下記のPolars 100+ノックを解いてみました。使用したPolarsのバージョンは1.33.1です。

https://qiita.com/SaitoTsutomu/items/1a19dd484c88b77a4f2a

**Polars 100+ノックの各パート**

* Part 1: 基本編 - Polarsへの第一歩 (Knocks 1-20)
* Part 2: 式 (Expression) の習得 - Polarsの心臓部 (Knocks 21-45)
* Part 3: データの集計と再形成 (Knocks 46-73)
* Part 4: 高度なテクニックとパフォーマンス (Knocks 74-97)
* Part 5: Polarsエコシステムと総合演習 (Knocks 98-109)

なお、途中でGemini 2.5 Proの上限に達したため、本記事はPart 3までの73問を対象としています。Part 4以降の後編は以下になります。

https://qiita.com/SaitoTsutomu/items/5dad18c83b15a4eb61b9

### 対象読者

* Polarsを学習している方
* LLMのコード生成の精度に関心がある方
* Polarsの最新仕様と過去バージョンの違いを理解したい方

## 正解だが気になった解答

正解率は`84%`（`= 61/73`）でした。

以降は正解でしたが気になった解答です。

### `問題 1.2.4` 正規表現で列を選択

> 1.1.3の`df_titanic`の`P`で始まる列名を持つすべての列を選択し、変数`ans`に代入してください。

**Geminiの解答**

```python
ans = df_titanic.select(cs.matches("^P"))
```

**模範解答**

```python
ans = df_titanic.select(pl.col("^P.*$"))
```

**補足**

正規表現には`cs.matches()`が使えますが、模範解答のように`pl.col()`も使えます。`pl.col()`はよく使うので、`pl.col()`で覚えた方がよいと思いました。

https://docs.pola.rs/api/python/stable/reference/selectors.html#polars.selectors.matches

### `問題 3.1.7` 条件を満たす行数

> 2.3.9の`df_titanic`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 客室クラス (Pclass) ごとに、30歳以上の乗客の数を数える
>   * 列名を`CountOver30`とする
> * 列`Pclass`で昇順にソートする

**Geminiの解答**

```python
ans = (
    df_titanic
    .filter(pl.col("Age") >= 30) # 30歳以上でフィルタリング
    .group_by("Pclass")          # 客室クラスでグループ化
    .agg(pl.len().alias("CountOver30")) # 各グループの行数を数え、列名を変更
    .sort("Pclass")              # Pclassで昇順ソート
)
```

**模範解答**

```python
ans = (
    df_titanic.group_by("Pclass")
    .agg(CountOver30=col.Age.filter(col.Age >= 30).len())
    .sort("Pclass")
)
```

**補足**

出題意図としては`agg()`内で`filter()`をさせる問題でしたが、外側でも正解になっていました。

### `問題 3.1.8` グループ化の結果のフィルタリング(having句相当)

> 2.3.9の`df_titanic`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 客室クラス (Pclass) ごとに乗客数を計算
>   * 乗客数が200人以上のみ残す
>   * 列名を`PassengerCount`とする
> * 列`Pclass`で昇順にソートする

**Geminiの解答**

```python
ans = df_titanic.group_by("Pclass").agg(
    pl.count().alias("PassengerCount")
).filter(
    pl.col("PassengerCount") >= 200
).sort("Pclass")
```

**模範解答**

```python
ans = (
    df_titanic.group_by("Pclass")
    .agg(PassengerCount=pl.len())
    .filter(col.PassengerCount > 200)
    .sort("Pclass")
)
```

**補足**

正解ですが、`pl.count()`はDeprecatedです。

### `問題 3.4.9` 非等価結合

> 各イベントがどの時間枠に含まれるかを判定して結合し、event_timeでソートして、変数`ans`に代入してください。
> 
> ```python
> events = pl.DataFrame(
>     {
>         "event_time": [1.5, 2.8, 3.5, 5.1],
>         "event_type": ["a", "b", "c", "d"],
>     }
> )
> windows = pl.DataFrame(
>     {
>         "window_id": ["x", "y", "z"],
>         "start_time": [1.0, 3.0, 5.0],
>         "end_time": [2.0, 4.0, 6.0],
>     }
> )
> ```

**Geminiの解答**

```python
ans = (
    events.sort("event_time")
    .join_asof(
        windows.sort("start_time"), 
        left_on="event_time", 
        right_on="start_time"
    )
    .filter(pl.col("event_time") <= pl.col("end_time"))
    .sort("event_time")
)
```

**模範解答**

```python
ans = events.join_where(
    windows,
    (pl.col("event_time") >= pl.col("start_time"))
    & (pl.col("event_time") < pl.col("end_time")),
).sort("event_time")
```

**補足**

正解ですが、もっとシンプルに書けます。

### `問題 3.5.1` 縦持ち変換 (unpivot)

> `df_wide`は、生徒ごとの各科目の点数を横持ちで保持しています。このDataFrameを「生徒(`Student`)」「科目(`Subject`)」「点数(`Score`)」を列に持つ縦長の形式に変換し、変数`ans`に代入してください。
> 
> ```python
> df_wide = pl.DataFrame({
>     "Student": ["Alice", "Bob", "Carol"],
>     "Math": [90, 88, 92],
>     "Science": [85, 91, 89],
> })
> ```

**Geminiの解答**

```python
ans = df_wide.melt(
    id_vars="Student", 
    variable_name="Subject", 
    value_name="Score"
)
```

**模範解答**

```python
ans = df_wide.unpivot(
    on=["Math", "Science"],
    index="Student",
    variable_name="Subject",
    value_name="Score"
)
```

**補足**

`melt()`はDeprecatedです。

### `問題 3.5.2` 横持ち変換 (pivot)

> 問題 3.5.1で作成した縦長のDataFrame`df_long`を、再び生徒ごとに行を持ち、各科目が列となる横長の形式に変換し、変数`ans`に代入してください。
> 
> ```python
> df_long = pl.DataFrame({
>     "Student": ["Alice", "Bob", "Carol", "Alice", "Bob", "Carol"],
>     "Subject": ["Math", "Math", "Math", "Science", "Science", "Science"],
>     "Score": [90, 88, 92, 85, 91, 89],
> })
> ```

**Geminiの解答**

```python
ans = df_long.pivot(
    index="Student", 
    columns="Subject", 
    values="Score"
)
```

**模範解答**

```python
ans = df_long.pivot(
    on="Subject",
    index="Student",
    values="Score",
)
```

**補足**

引数`columns`はDeprecatedです。

## 不正解の解答

不正解には、以下のようなものがありました。

* ちょっとした間違い
* バージョンが古いもの
* まるっきり違うもの

### `問題 1.2.6` ANDでフィルタリング

> 1.1.3の`df_titanic`の30歳より年上で、かつ女性の乗客を抽出し、変数`ans`に代入してください。

**Geminiの解答**

```python
ans = df_titanic.filter(
    (pl.col("age") > 30) & (pl.col("sex") == "female")
)
```

**模範解答**

```python
ans = df_titanic.filter(
    (pl.col("Age") > 30) & (pl.col("Sex") == "female")
)
```

**補足**

列名の大文字／小文字が違うだけなので、ほぼ正解です。
※ 本問では列名が明示されていませんが、少し前の問題で出ています。

### `問題 2.1.10` 列の並べ替え

> 1.1.3の`df_titanic`を次の条件で修正し、変数`ans`に代入してください。
>
> * 列`Survived`、列`Pclass`、列`Name`、列`Sex`、列`Age`の順に列を並べ替え、残りの列をその後ろに配置する
> 
> ```python
> _cols = "Survived", "Pclass", "Name", "Sex", "Age"
> ```

**Geminiの解答**

```python
ans = df_titanic.select(
    _cols + [pl.all().exclude(_cols)]
)
```

**模範解答**

```python
ans = df_titanic.select(*_cols, pl.exclude(_cols))
```

**補足**

ほとんど正解に見えますが、`_cols`がタプルであるため `+` 演算子でリストと結合できず、このコードはエラーになります。また、`pl.all().exclude()`ではなく、模範解答のように `pl.exclude()` を使うのが現在の推奨される書き方です。

### `問題 2.3.1` 文字列の長さ(.str)

> 1.1.3の`df_titanic`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 列`Name`の乗客の名前の長さ
>   * 列名を`NameLength`とする

**Geminiの解答**

```python
ans = df_titanic.with_columns(
    pl.col("Name").str.len().alias("NameLength")
)
```

**模範解答**

```python
ans = df_titanic.with_columns(
    NameLength=col.Name.str.len_chars()
)
```

**補足**

バージョン0.18以降に`str.len()`はありません。

### `問題 2.3.4` 正規表現で抽出

> 1.1.3の`df_titanic`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 列`Name`から敬称（例: Mr., Mrs., Miss.）を正規表現で抽出する（ピリオドを除く）
>   * 列名を`Title`とする

**Geminiの解答**

```python
ans = df_titanic.with_columns(
    pl.col("Name").str.extract(r"([A-Za-z]+)\.", 1).alias("Title")
)
```

**模範解答**

```python
ans = df_titanic.with_columns(
    Title=col.Name.str.extract(r"(Mr|Mrs|Miss)\."),
)
```

**補足**

正解に近いのですが、`Mr`、`Mrs`、`Miss`だけを抽出できていません。

### `問題 2.3.10` カテゴリカル型へ変更

> 2.3.9の`df_titanic`を次の条件で修正し、変数`ans`に代入してください。
>
> * 列`Pclass`を`1st`、`2nd`、`3rd`という値のカテゴリカル型に変換にする

**Geminiの解答**

```python
ans = df_titanic.with_columns(
    pl.col('Pclass')
    .map_dict({1: '1st', 2: '2nd', 3: '3rd'})
    .cast(pl.Categorical)
)
```

**模範解答**

```python
ans = df_titanic.with_columns(
    col.Pclass.replace_strict(
        {1: "1st", 2: "2nd", 3: "3rd"}
    ).cast(pl.Categorical)
)
```

**補足**

`map_dict()`はバージョン0.20で廃止されました。代わりに`replace()`や`replace_strict()`を使います。

https://docs.pola.rs/docs/python/version/0.19/reference/expressions/api/polars.Expr.map_dict.html

### `問題 3.1.4` 数値列の集計

> 2.3.9の`df_titanic`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 性別 (Sex) ごとに、すべての数値列の平均値を計算する
>   * 列名のサフィックスに`Mean`をつける
> * 列`Sex`で昇順にソートする

**Geminiの解答**

```python
ans = (
    df_titanic.group_by("Sex")
    .agg(cs.numeric().mean().suffix("Mean"))
    .sort("Sex")
)
```

**模範解答**

```python
ans = (
    df_titanic.group_by("Sex")
    .agg(cs.numeric().mean().name.suffix("Mean"))
    .sort("Sex")
)
```

**補足**

ほとんど正解ですが`name`が抜けています。

### `問題 3.2.3` 年ごとの集計(開始点変更)

> 3.2.1の`df_weather`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 毎年7月を開始点として年間の降雪量(SNOW)の合計を計算する(例：2020/7/1 - 2021/6/30)
>   * 列名を`TotalSnow`とする

**Geminiの解答**

```python
df_with_season = df_weather.with_columns(
    (pl.when(pl.col("DATE").dt.month() >= 7)
     .then(pl.col("DATE").dt.year())
     .otherwise(pl.col("DATE").dt.year() - 1))
    .alias("season_start_year")
)
ans = (
    df_with_season.group_by("season_start_year")
    .agg(pl.col("SNOW").sum().alias("TotalSnow"))  # 列名をTotalSnowに変更
    .sort("season_start_year")  # 結果を見やすくするためにソート
)
```

**模範解答**

```python
ans = df_weather.group_by_dynamic(
    index_column="DATE",
    every="1y",
    offset="6mo",  # 7月を開始点にするため、6ヶ月オフセット
).agg(TotalSnow=col.SNOW.sum())
```

**補足**

だいぶややこしい解答を作成していますが不正解です。`group_by_dynamic()`は苦手なのかもしれません。

### `問題 3.2.4` カテゴリカルキーと時間でグループ化

> `_df`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 地点(Station)ごと、かつ10年ごとに平均最高気温（TMAXの平均）を計算する
>   * 列名を`AvgTMAX/decade`とする
> 
> ```python
> # ダミーの観測地点列を追加
> _df = df_weather.with_columns(
>     Station=pl.when(col.DATE.dt.year() < 1950)
>     .then(pl.lit("StationA"))
>     .otherwise(pl.lit("StationB"))
> )
> ```

**Geminiの解答**

```python
ans = (
    _df.group_by(
        "Station",
        pl.col("DATE").dt.year().floordiv(10).mul(10).alias("decade")
    )
    .agg(pl.col("TMAX").mean().alias("AvgTMAX/decade"))
    .sort("Station", "decade")
)
```

**模範解答**

```python
ans = _df.group_by_dynamic(
    index_column="DATE",
    every="10y",  # 10年ごとに集計
    group_by="Station",  # カテゴリカルキーを指定
).agg(col.TMAX.mean().alias("AvgTMAX/decade"))
```

**補足**

この問題も`group_by_dynamic()`を使うべきところで`group_by()`を使って不正解になっています。

### `問題 3.2.5` ローリング集計

> 3.2.1の`df_weather`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 7日間の移動平均最高気温を計算する
>   * 列名を`AvgTMAX/7d`とする
> * `DATE`と`AvgTMAX/7d`の2列とする

**Geminiの解答**

```python
ans = (
    df_weather
    .sort("DATE") # 日付でソート
    .select(
        pl.col("DATE"),
        pl.col("TMAX")
        .rolling(window_size="7d", by="DATE") # 日付を基準に7日間の移動平均を計算
        .mean()
        .alias("AvgTMAX/7d") # 列名を変更
    )
)
```

**模範解答**

```python
ans = df_weather.select(
    col.DATE,
    col.TMAX.rolling_mean(window_size=7).alias("AvgTMAX/7d"),
)
```

**補足**

Geminiは時間軸を考慮した `rolling(...).mean()` を使おうとしていますが、引数の `window_size` や `by` が古いAPIのもので、現在のバージョンではエラーになります。この場合は、よりシンプルに記述できる `rolling_mean()` を使うのが適切です。

### `問題 3.4.3` 完全外部結合

> `df_a`と`df_b`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 完全外部結合する

**Geminiの解答**

```python
ans = df_a.join(df_b, on="key", how="outer").sort("key")
```

**模範解答**

```python
ans = df_a.join(df_b, on="key", how="full")
```

**補足**

ほぼ正解なのですが、不要なソートをしています。また、`how="outer"`はDeprecatedです。

### `問題 3.4.6` セミ結合

> `df_a`と`df_b`を次の条件で修正し、変数`ans`に代入してください。
> 
> * df_aのキーがdf_bにも存在する行のみを、df_aの列だけで抽出する

**Geminiの解答**

```python
ans = df_a.semi_join(df_b, on="key")
```

**模範解答**

```python
ans = df_a.join(df_b, on="key", how="semi")
```

**補足**

`semi_join()`というメソッドは存在しません。

### `問題 3.4.8` Asof結合

> 時系列データで、各注文日に最も近い過去の市場価格を結合し、変数`ans`に代入してください。
>
> ```python
> market_prices = pl.DataFrame({
>     'time': pl.date_range(pl.date(2023, 1, 2), pl.date(2023, 1, 8), '2d', eager=True),
>     'price': range(2, 9, 2),
> })
> orders = pl.DataFrame({
>     'order_time': [date(2023, 1, 1), date(2023, 1, 5), date(2023, 1, 9)],
>     'volume': [100, 120, 180],
> })
> ```

**Geminiの解答**

```python
ans = orders.join_asof(
    market_prices,
    on='time',
    by='order_time')
```

**模範解答**

```python
ans = orders.join_asof(
    market_prices,
    left_on="order_time",
    right_on="time",
    strategy="nearest",
)
```

**補足**

似ているけど、いろいろ違います。

## 前編のまとめ

Gemini 2.5 Proを使ってPolars 100+ノック（Part 1～3）を解いてみた結果、正解率は約84%でした。
正しい解答も多かった一方で、以下の点が課題として見えました。

* **模範解答との差**：正解でも学習効果が低い解答
* **Deprecated**：`pl.count()`、`melt()`、`columns`引数など
* **不正解のパターン**：存在しない関数、`group_by_dynamic()`などの理解不足

概ね正しいコードを生成していましたが、最新仕様が把握できていないことが多々見られました。
また、シンプルに書けることを複雑に書いていることもあり、注意が必要だと感じました。

