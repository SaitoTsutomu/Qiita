title: Polarsのインデックス参照
tags: Python pandas Polars
url: https://qiita.com/SaitoTsutomu/items/a9bfeaa1951e9a0fc50d
created_at: 2024-11-28 21:53:10+09:00
updated_at: 2024-12-12 07:02:58+09:00
body:

pandasのインデックス参照はかなり複雑です。

参考：pandasの基礎知識

https://docs.pyq.jp/python/pydata/pandas/basics.html

Polarsもインデックス参照が使えます。そこそこ複雑ですが、pandasよりはわかりやすいでしょう。

本記事では、PolarsのDataFrameのインデックス参照を簡単に紹介します。

## 概要

DataFrameをインデックス参照すると、要素、Series、DataFrameのいずれかを取得できます。

**行の指定にはキーとしてintなど**を、**列の指定にはキーとしてstrなど**を使います。
行の指定と列の指定のどちらかは省略できます。

https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.__getitem__.html

下記のDataFrameを使って確認しましょう。

**In**

```python
df = pl.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [30, 20],
})
df
```

**Out**

<small>shape: (2, 2)</small><table style="margin-left: 0;"><thead><tr><th>Name</th><th>Age</th></tr><tr><td>str</td><td>i64</td></tr></thead><tbody><tr><td>&quot;Alice&quot;</td><td>30</td></tr><tr><td>&quot;Bob&quot;</td><td>20</td></tr></tbody></table>

## 行指定が「intかintのスライスかintのリスト」、列指定がなし

行指定が「intかintのスライスかintのリスト」で、列指定がない場合は、指定した行（DataFrame）になります。

**In**

```python
df[0]
```

**Out**

<small>shape: (1, 2)</small><table style="margin-left: 0;"><thead><tr><th>Name</th><th>Age</th></tr><tr><td>str</td><td>i64</td></tr></thead><tbody><tr><td>&quot;Alice&quot;</td><td>30</td></tr></tbody></table>


**In**

```python
df[1:]
```

**Out**

<small>shape: (1, 2)</small><table style="margin-left: 0;"><thead><tr><th>Name</th><th>Age</th></tr><tr><td>str</td><td>i64</td></tr></thead><tbody><tr><td>&quot;Bob&quot;</td><td>20</td></tr></tbody></table>


**In**

```python
df[[1]]
```

**Out**

<small>shape: (1, 2)</small><table style="margin-left: 0;"><thead><tr><th>Name</th><th>Age</th></tr><tr><td>str</td><td>i64</td></tr></thead><tbody><tr><td>&quot;Bob&quot;</td><td>20</td></tr></tbody></table>

## 行指定がなし、列指定がstr

行指定がなく、列指定がstrの場合は、指定した列（Series）になります。

**In**

```python
df["Name"]
```

**Out**

<small>shape: (2,)</small><table style="margin-left: 0;"><thead><tr><th>Name</th></tr><tr><td>str</td></tr></thead><tbody><tr><td>&quot;Alice&quot;</td></tr><tr><td>&quot;Bob&quot;</td></tr></tbody></table>

## 行指定がなし、列指定が「strのスライスかstrのリスト」

行指定がなく、列指定が「strのスライスかstrのリスト」の場合は、指定した列（DataFrame）になります。

**In**

```python
df["Name":]
```

**Out**

<small>shape: (2, 2)</small><table style="margin-left: 0;"><thead><tr><th>Name</th><th>Age</th></tr><tr><td>str</td><td>i64</td></tr></thead><tbody><tr><td>&quot;Alice&quot;</td><td>30</td></tr><tr><td>&quot;Bob&quot;</td><td>20</td></tr></tbody></table>


**In**

```python
df[["Name"]]
```

**Out**

<small>shape: (2, 1)</small><table style="margin-left: 0;"><thead><tr><th>Name</th></tr><tr><td>str</td></tr></thead><tbody><tr><td>&quot;Alice&quot;</td></tr><tr><td>&quot;Bob&quot;</td></tr></tbody></table>

## 行指定がint、列指定がstrかint

行指定がintで、列指定がstrかintの場合は、指定した行と列の要素になります。

**In**

```python
df[0, "Name"]
```

**Out**

```
'Alice'
```

また、代入の左辺に使えます。

※ 要素が数字や文字列などの単純な型でないと代入でエラーになることがあるようです。

## 行指定が「intのスライスかintのリスト」、列指定がstrかint

行指定が「intのスライスかintのリスト」で、列指定がstrかintの場合は、指定した行の列（Series）になります。

**In**

```python
df[1:, "Name"]
```

**Out**

<small>shape: (1,)</small><table style="margin-left: 0;"><thead><tr><th>Name</th></tr><tr><td>str</td></tr></thead><tbody><tr><td>&quot;Bob&quot;</td></tr></tbody></table>

## 行指定が「intかintのスライスかintのリスト」、列指定が「strかintのスライス、または、strかintのリスト」

行指定が「intかintのスライスかintのリスト」で、列指定が「strのスライスかstrのリスト」の場合は、指定した行と指定した列（DataFrame）になります。

**In**

```python
df[1, :"Name"]
```

**Out**

<small>shape: (1, 1)</small><table style="margin-left: 0;"><thead><tr><th>Name</th></tr><tr><td>str</td></tr></thead><tbody><tr><td>&quot;Bob&quot;</td></tr></tbody></table>

## まとめ

| 行指定                          | 列指定                                           | 値        | 代入 |
| :------------------------------ | :----------------------------------------------- | :-------- | :--- |
| intかintのスライスかintのリスト | なし                                             | DataFrame | ×    |
| なし                            | str                                              | Series    | ×    |
| なし                            | strのスライスかstrのリスト                       | DataFrame | ×    |
| int                             | strかint                                         | 要素      | ◯    |
| intのスライスかintのリスト      | strかint                                         | Series    | ×    |
| intかintのスライスかintのリスト | strかintのスライス、<br>または、strかintのリスト | DataFrame | ×    |

* 行指定には、intかintのスライスかintのリスト
* 列指定には、strかstrのスライスかstrのリスト
  * ただし、第2キーのときはstrの代わりにintが可能
* 行指定なしは全行指定、列指定なしは全列指定とみなす
* 1行、1列の場合の値は、要素（代入可能）
* 複数行、1列の場合の値は、Series
* 複数列の場合の値は、DataFrame

## 感想

列の取得は、`df.get_column("Name")`や`df.to_series(0)`のように書けます。当初は、このような書き方の方が好ましいと考えてましたが、インデックス参照を使っても問題ないように考えるようになりました。
理由は、以下のようなものです。

* pandasのインデックス参照はわかりにくかったが、Polarsは無理なく覚えられる
* シンプルで柔軟に記述できる

また、エクスプレッションの方がふさわしい場合は、エクスプレッションも積極的に使っていくつもりです。

以上

