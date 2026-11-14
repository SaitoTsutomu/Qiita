title: Polarsのmap系メソッド完全ガイド：4つの関数の違いと使い分け
tags: Python pandas データ分析 udf Polars
url: https://qiita.com/SaitoTsutomu/items/1507f038f17679e86af8
created_at: 2025-08-17 21:30:30+09:00
updated_at: 2025-08-17 21:30:30+09:00
body:

## はじめに

この記事では、データ分析ライブラリPolarsに用意されている`map`で始まる4つのメソッドについて、それぞれの役割と使い方を解説します。

**対象読者**

* Polarsの知識をさらに深めたい方
* データ変換の選択肢を広げたい方

`map`で始まる以下の4つのメソッドを、利用できるクラスごとに整理しました。

| メソッド＼クラス | DataFrame | LazyFrame | Series | Expr  | GroupBy |
| :--------------- | :-------: | :-------: | :----: | :---: | :-----: |
| `map_rows()`     |     ◯     |     −     |   −    |   −   |    −    |
| `map_batches()`  |     −     |     ◯     |   −    |   ◯   |    −    |
| `map_elements()` |     −     |     −     |   ◯    |   ◯   |    −    |
| `map_groups()`   |     −     |     −     |   −    |   −   |    ◯    |

※ Polarsにはこの他にも`name.map`や`name.map_fields`といったメソッドがありますが、本記事では扱いません。

## サンプルデータ

以下の`DataFrame`を例に、各メソッドの動作を説明します。

```python
import polars as pl

# pl.col("カラム名") を col.カラム名 と簡潔に書くためのヘルパークラス
class Col:
    def __getattribute__(self, name):
        if name[0].isupper():
            c = pl.col(name)
            setattr(self, name, c)
            return c
        return super().__getattribute__(name)

col = Col()

df = pl.DataFrame(
    {
        "Product": ["A", "A", "B"],
        "Price": [30, 35, 50],
    }
)
lf = df.lazy()
df
```

**実行結果**

```
shape: (3, 2)
┌─────────┬───────┐
│ Product ┆ Price │
│ ---     ┆ ---   │
│ str     ┆ i64   │
╞═════════╪═══════╡
│ A       ┆ 30    │
│ A       ┆ 35    │
│ B       ┆ 50    │
└─────────┴───────┘
```

## `map_rows()`

`map_rows()`は、`DataFrame`に対し**行ごと**に変換処理を適用するメソッドです。引数として渡す関数は、行のデータをタプルで受け取り、単一の値（スカラー）を返すように定義します。

**例: `Product`と`Price`を結合した文字列を作成**

```python
def info(row: tuple) -> str:
    return f"{row[0]}_{row[1]}"

df.map_rows(info)
```

**実行結果**

```
shape: (3, 1)
┌───────┐
│ map   │
│ ---   │
│ str   │
╞═══════╡
│ A_30  │
│ A_35  │
│ B_50  │
└───────┘
```

**💡 より効率的な方法**

同じ結果は、Polarsのエクスプレッション（式）を使うことで、より高速に実現できます

```python
df.select(
    map=col.Product + "_" + col.Price.cast(pl.Utf8)
)
```

**ポイント**: `map_rows`は柔軟ですが、処理速度の面ではエクスプレッションが圧倒的に優れています。エクスプレッションで書ける処理は、そちらを使いましょう。

なお、行方向の処理が目的であれば、以下のような専用関数が便利です。

* `pl.min_horizontal()`: 複数列の最小値
* `pl.max_horizontal()`: 複数列の最大値
* `pl.sum_horizontal()`: 複数列の合計
* `pl.mean_horizontal()`: 複数列の平均
* `pl.coalesce()`: 最初の非None

## `map_batches()`

`map_batches()`は、**LazyFrame**と**Expr**（式）のコンテキストで使用でき、データのかたまり（バッチ）に対して一括で処理を適用します。

**LazyFrameでの使用**

遅延評価（LazyFrame）において、DataFrame（大規模な場合は分割されたもの）を受け取り、DataFrameを返す関数を適用します。

**例: `Price`列の値を2倍にする**

```python
def double_df(df: pl.DataFrame) -> pl.DataFrame:
    return df * 2

# map_batchesの後にselectがあることに注目
lf.map_batches(double_df).select("Price").collect()
```

**実行結果**

```
shape: (3, 1)
┌───────┐
│ Price │
│ ---   │
│ i64   │
╞═══════╡
│ 60    │
│ 70    │
│ 100   │
└───────┘
```

**🚀 遅延評価のメリット**

この例のポイントは、`map_batches`が**クエリ最適化の恩恵を受ける**点です。`map_batches`の後に`select("Price")`があるため、変換関数`double_df`に渡される`df`は、初めから`Price`列のみを含むDataFrameになります。これにより、不要なデータ処理を削減し、メモリ使用量と処理時間を節約できます。

**Exprでの使用**

`select`や`with_columns`などの式の中で、Seriesを受け取りSeriesを返す関数を適用します。

**例: Price列の値を2倍にする**

```python
def double_sr(sr: pl.Series) -> pl.Series:
    return sr * 2

df.select(col.Price.map_batches(double_sr, return_dtype=pl.Int64))
```

結果は上と同じです。もちろん、この単純な処理であれば`df.select(col.Price * 2)`と書く方がはるかに効率的です。

## `map_elements()`

`map_elements()`は、**Series**と**Expr**のコンテキストで、要素ごとに変換処理を適用します。

**例: `Price`列の値を2倍にする**

```python
def double_value(i: int) -> int:
    return i * 2

df.select(
    col.Price.map_elements(double_value, return_dtype=pl.Int64)
)
```

結果は上記までと同じです。

**⚠️ パフォーマンスに関する注意**

`map_elements()`は、Pythonの関数を要素単位で呼び出すため、**パフォーマンスが著しく低下します**。Polarsの高速性を損なう主な原因となるため、利用は慎重に検討してください。

Polarsの組み込みエクスプレッションで実現できる場合は、必ずそちらを使用しましょう。このメソッドは、どうしてもPolarsの標準機能では書けない複雑なロジックを実装する際の**最後の手段**と位置づけるのが賢明です。

## `map_groups()`

`map_groups()`は、`group_by`で作成された**グループごと**に変換処理を適用するメソッドです。グループ化されたDataFrameを受け取り、DataFrameを返す関数を定義します。

**例: Productの各グループで、最初の行だけを取得する**

```python
def first(df: pl.DataFrame) -> pl.DataFrame:
    return df[:1]

df.group_by("Product", maintain_order=True).map_groups(first)
```

```
shape: (2, 2)
┌─────────┬───────┐
│ Product ┆ Price │
│ ---     ┆ ---   │
│ str     ┆ i64   │
╞═════════╪═══════╡
│ A       ┆ 30    │
│ B       ┆ 50    │
└─────────┴───────┘
```

この処理は、`group_by`の後に使える`first()`メソッドでもっとシンプルに書けます。

```python
df.group_by("Product", maintain_order=True).first()
```

`map_groups`は、`first`のような既存の集計メソッドでは実現できない、より複雑なグループ単位の処理を実装する際に役立ちます。

## まとめ

各メソッドの役割をまとめます。

* `map_rows()`: DataFrameの**行**を単位として変換
* `map_batches()`: LazyFrameやExprで、データの**かたまり**（バッチ）を単位として変換
* `map_elements()`: SeriesやExprで、**要素**を単位として変換（⚠️ **低速なため注意**）
* `map_groups()`: GroupByオブジェクトの**グループ**を単位として変換

これらのメソッドは非常に柔軟で強力ですが、パフォーマンスの観点からは、常にPolarsの**組み込みエクスプレッションを優先して使用しましょう**。

