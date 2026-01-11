title: GeminiはPolars 100+ノックに正解するか？（後編）
tags: Python データ分析 AI Polars
url: https://qiita.com/SaitoTsutomu/items/5dad18c83b15a4eb61b9
created_at: 2025-09-22 20:07:32+09:00
updated_at: 2025-09-22 20:07:32+09:00
body:

## はじめに

Gemini 2.5 Proで下記のPolars 100+ノックを解いてみました。

https://qiita.com/SaitoTsutomu/items/1a19dd484c88b77a4f2a

本記事は以下の記事の後編になります。

https://qiita.com/SaitoTsutomu/items/c509d8391e61048897c7

Polarsのバージョンは1.33.1を使い、Google AI StudioのGemini 2.5 ProにGrounding with Google Searchツールをオンにして実行しました。

### 対象読者

* Polarsを学習している方
* LLMのコード生成の精度に関心がある方
* Polarsの最新仕様と過去バージョンの違いを理解したい方

## 全体の正解率と考察

**総合正解率は83%**（109問中91問）でした。

練習問題は「Part 1: 基本編」から始まり、「Part 5: Polarsエコシステムと総合演習」と進むにつれて難易度が上がる構成ですが、前編後編とも同じくらいの正解率でした。これは、ツール利用が関係しているかもしれません。

以下に、正解したものの改善の余地がある解答と、不正解だった解答について詳しく解説します。

-----

## 正解と模範解答

Geminiの解答の中には、正解ではあるものの、よりシンプルでPolarsらしい書き方ができるものがありました。

### `問題 5.3.1` 折れ線グラフ

> `_df`を使って次の要件で折れ線グラフを作成し、変数`ans`に代入してください。
> 
> * X軸は列`Name`
> * Y軸は列`Score`
> * Y軸のラベルは`得点`
> * 列`Subject`ごとに線を引くこと
> 
> ```python
> import altair as alt
> 
> _df = pl.DataFrame({
>     "Name": ["A", "A", "B", "B", "C", "C"],
>     "Subject": ["Math", "Music", "Math", "Music", "Math", "Music"],
>     "Score": [85, 90, 94, 88, 80, 93],
> })
> ```

**Geminiの解答**

```python
ans = alt.Chart(_df).mark_line().encode(
    x="Name",
    y=alt.Y("Score", title="得点"),
    color="Subject"
)
```

**模範解答**

```python
ans = _df.plot.line(
    x="Name",
    y=alt.Y("Score", title="得点"),
    color="Subject",
)
```

**補足**

Geminiの解答はグラフ描画ライブラリ**Altair**の一般的な記法です。
一方で、模範解答は`_df.plot.line()`という**PolarsのPlotting API**（Altairの糖衣構文）です。Polarsの学習においては、こちらの簡潔な書き方を覚える方が効率的でしょう。

### `問題 5.3.2` 散布図

> `_df`を使って次の要件で散布図を作成し、変数`ans`に代入してください。
> 
> * X軸は列`Math`
> * Y軸は列`Music`
> * タイトルは`2教科の関係`
> 
> ```python
> import altair as alt
> 
> _df = pl.DataFrame({
>     "Math": [33, 21, 42],
>     "Music": [23, 34, 26],
> })
> ```

**Geminiの解答**

```python
ans = alt.Chart(_df).mark_circle().encode(
    x='Math',
    y='Music'
).properties(
    title='2教科の関係'
)
```

**模範解答**

```python
ans = _df.plot.scatter(
    x="Math",
    y="Music",
).properties(
    title="2教科の関係",
)
```

**補足**

前問と同じく糖衣構文を使っていません。散布図なので`plot.scatter()`で覚えた方がよいでしょう。


## 不正解の解答

### `問題 4.1.2` グループ内累積和

> `df_weather`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 年ごとに日々の降水量(PRCP)の累積和を計算する
>   * 列名を`CumulativePRCP`とする

**Geminiの解答**

```python
ans = df_weather.with_columns(
    pl.col('PRCP').cumsum().over(pl.col('DATE').dt.year()).alias('CumulativePRCP')
)
```

**模範解答**

```python
ans = df_weather.with_columns(
    CumulativePRCP=col.PRCP.cum_sum().over(col.DATE.dt.year()),
)
```

**補足**

`cumsum()`はバージョン0.20で廃止されました。`cum_sum()`に直せば正解です。

### `問題 4.1.8` 条件付きウィンドウ

> 4.1.1の`df_titanic`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 各客室クラス (Pclass) 内で、運賃が50以上の乗客のみを対象に、運賃の累積和を計算する
>   * 運賃が50未満の乗客は運賃を0とみなす
>   * 列名を`ConditionalCumulativeFare`とする

**Geminiの解答**

```python
ans = df_titanic.with_columns(
    pl.when(pl.col("Fare") >= 50)
    .then(pl.col("Fare"))
    .otherwise(0)
    .cumsum()
    .over("Pclass")
    .alias("ConditionalCumulativeFare")
)
```

**模範解答**

```python
ans = df_titanic.with_columns(
    ConditionalCumulativeFare=pl.when(col.Fare >= 50)
    .then(col.Fare)
    .otherwise(0)
    .cum_sum()
    .over("Pclass")
)
```

**補足**

この解答も`cumsum()`を`cum_sum()`に直せば正解です。
AIが作成するコードでは古いバージョンによるエラーに注意しましょう。

### `問題 4.4.2` 行ごとに関数を適用 (map_rows)

> `_df`を次の条件で修正し、変数`ans`に代入してください。
> 
> * 各行に関数`value`を適用した列だけにする
>  * 列名をValとする
> * 関数`_value`を使うこと
> 
> ```python
> _df = pl.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
> 
> def _value(row: tuple[int, int]) -> int:
>     return row[0] + 2 * row[1]
> ```

**Geminiの解答**

```python
ans = _df.map_rows(_value).alias("Val").to_frame()
```

**模範解答**

```python
ans = _df.map_rows(_value).rename({"map": "Val"})
```

**補足**

`map_rows()`の後の処理が誤っています。`map_rows()`は新しいDataFrameを返しますが、そのままでは列名が`"map"`となるため、`rename()`での変更が必要です。

### `問題 5.2.3` DataFrameに直接SQL実行

> 次の要件でDataFrameを作成し、変数`ans`に代入してください。
> 
> * グローバルスコープにあるDataFrameに対して `pl.sql()`を使って直接クエリを実行する
> 
> ```python
> _query = "SELECT COUNT(*) as num_passengers FROM df_titanic"
> ```

**Geminiの解答**

```python
context = pl.SQLContext()
context.register("df_titanic", df_titanic)
ans = context.execute(_query)
```

**模範解答**

```python
ans = pl.sql(_query).collect()
```

**補足**

`.collect()`をつければ正解と同じ値にはなりますが、問題で指示されている`pl.sql()`を使っていません。

### `問題 5.2.4` SQLでテーブル作成

> 5.2.1の`ctx`から次の要件でDataFrameを作成し、変数`ans`に代入してください。
> 
> * 登録した'titanic'テーブルから、新しいテーブル作成のSQLクエリを実行する
> 
> ```python
> _query = "CREATE TABLE survivors AS SELECT * FROM titanic WHERE Survived = 1"
> ```

**Geminiの解答**

```python
ans = ctx.execute(query).collect()
```

**模範解答**

```python
ans = ctx.execute(_query).collect()
```

**補足**

問題文に与えられた`_query`を無視して`query`を使っています。
「クエリと言えば`query`」というようなある種の思い込みは他でもよく見られます。

### `問題 5.4.2` 顧客のRFM分析

> この最終演習では、Online Retailデータセットを用いて、顧客セグメンテーションの一般的な手法であるRFM（Recency, Frequency, Monetary）分析を行います。これは、データクリーニング、時系列処理、複雑な集計など、多くのスキルを統合する実践的な課題です。
> 
> `_df`を元に、各顧客についてRFM指標を計算し、最終結果を変数`ans`に代入してください。
> 
> **手順**
> 
> 1. データクリーニング
>   * InvoiceDateをdatetime型に変換(`format="%m/%d/%y %H:%M"`)
>   * Quantity > 0、UnitPrice > 0、CustomerIDが欠損以外でフィルタリング
> 
> 2. RFM指標を計算
>   * CustomerIDでグループ化し以下を修正
>     * 列`Recency`として、「グループ化前のInvoiceDateの最大値」からInvoiceDateの最大値を引い> た日数+1
>     * 列`Frequency`として、InvoiceNoのユニーク数
>     * 列`Monetary`として、(Quantity * UnitPrice)の合計
> 
> 3. 列`Monetary`で降順に、列`CustomerID`で昇順にソート
> 
> 最初の3行が下記のようになること。

| CustomerID | Recency | Frequency |  Monetary |
| ---------: | ------: | --------: | --------: |
|      14646 |       7 |        29 | 121973.65 |
|      18102 |      12 |        20 | 106601.55 |
|      12346 |     160 |         1 |   77183.6 |

**Geminiの解答**

```python
df_cleaned = _df.with_columns(
    pl.col("InvoiceDate").str.to_datetime(format="%m/%d/%y %H:%M")
).filter(
    (pl.col("Quantity") > 0)
    & (pl.col("UnitPrice") > 0)
    & (pl.col("CustomerID").is_not_null())
)

snapshot_date = df_cleaned.select(pl.max("InvoiceDate")).collect().item()

ans = (
    df_cleaned.group_by("CustomerID")
    .agg(
        Recency=(snapshot_date - pl.max("InvoiceDate")).dt.days() + 1,
        Frequency=pl.n_unique("InvoiceNo"),
        Monetary=(pl.col("Quantity") * pl.col("UnitPrice")).sum(),
    )
    .sort(["Monetary", "CustomerID"], descending=[True, False])
    .collect()
)
```

**模範解答**

```python
# 1. データクリーニング
_tmp = _df.with_columns(
    col.InvoiceDate.str.to_datetime(format="%m/%d/%y %H:%M"),
).filter(
    col.Quantity > 0,
    col.UnitPrice > 0,
    col.CustomerID.is_not_null(),
)

# 2. RFM指標を計算
_tmp = (
    _tmp.with_columns(
        Recency=(
            col.InvoiceDate.max() - col.InvoiceDate.max().over("CustomerID")
        ).dt.total_days() + 1,
    )
    .group_by("CustomerID")
    .agg(
        col.Recency.first(),
        Frequency=col.InvoiceNo.n_unique(),
        Monetary=(col.Quantity * col.UnitPrice).sum(),
    )
)

# 3. 列`Monetary`で降順に、列`CustomerID`で昇順にソート
ans = _tmp.sort(["Monetary", "CustomerID"], descending=[True, False]).collect()
```

**補足**

`dt.days()`というメソッドはPolarsに存在しません。これを`dt.total_days()`に変えれば正解になります。

## まとめ

Gemini 2.5 Proを使ってPolars 100+ノックを解いてみた結果、正解率は`83%`でした。
多くの解答は模範解答として使えそうです。ただし、AIが生成したコードを鵜呑みにするのではなく、**きちんと確認する**ことが重要です。

実は、Geminiの解答を確認していく中で問題の不備を見つけることができました。
AIを学習ツールとして活用する際は、単に答え合わせをするだけでなく、「**なぜこのコードが生成されたのか**」「**より良い書き方はないか**」といった視点で検証することで、より深い理解に繋がると感じました。

