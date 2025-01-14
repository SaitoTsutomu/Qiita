title: Polarsを使って、Python-MIPの数理モデルを作ってみよう
tags: Python pandas 最適化 python-mip Polars
url: https://qiita.com/SaitoTsutomu/items/16f588265a01feacecbe
created_at: 2024-09-21 19:11:27+09:00
updated_at: 2024-10-17 22:32:39+09:00
body:

## 概要

次の記事では、pandasを使って、Python-MIPの数理モデルを作ってみました。

https://qiita.com/SaitoTsutomu/items/c7b43c2e02710749d117

本記事では、**Polarsを使って、Python-MIPの数理モデルを作成**します。
Python-MIPの使い方については、上記記事を参照してください。
Polarsについては、公式ドキュメントを参照してください。

https://docs.pola.rs/

## 諸元

参照記事と同じように倉庫や工場の諸元を作成します。
ここでは、パッと見てわかりやすいように変数名に漢字を使っています。

```python
import polars as pl
from mip import Model, minimize, xsum

def xdot(s1: pl.Series, s2: pl.Series):
    return xsum(s1.to_numpy() * s2.to_numpy())

供給 = [44, 42, 45]
需要 = [39, 23, 22, 32]
輸送費 = [17, 16, 18, 10, 13, 15, 14, 13, 13, 10, 11, 15]

df_倉庫 = pl.DataFrame({"倉庫": ["W1", "W2", "W3"], "供給": 供給})
df_工場 = pl.DataFrame({"工場": ["F1", "F2", "F3", "F4"], "需要": 需要})
```

## 数理モデル

Polarsを使って数理モデルを作成します。

```python
# 数理モデル
m = Model()

# 変数表
_vars = m.add_var_tensor((len(輸送費),), "Var")
df_変数 = df_倉庫.join(df_工場, how="cross").with_columns(
    輸送費=pl.Series(輸送費), 変数=pl.Series(_vars)
)

# 目的関数
m.objective = minimize(xdot(df_変数.get_column("輸送費"), df_変数.get_column("変数")))

# 制約条件
for _, group in df_変数.group_by("倉庫"):
    m += xsum(group.get_column("変数")) <= group.get_column("供給")[0]
for _, group in df_変数.group_by("工場"):
    m += xsum(group.get_column("変数")) >= group.get_column("需要")[0]
```

※ `xdot`の代わりに`numpy.dot`が使えますが、効率が悪いです。

## ソルバーの実行と結果表示

```python
m.verbose = 0
m.optimize()
_values = df_変数.get_column("変数").to_numpy().astype(float)
df_変数 = df_変数.with_columns(結果=pl.Series(_values))
print(df_変数.filter(pl.col("結果") > 0))
print(f"目的関数値 = {m.objective_value}")
```

```
shape: (4, 7)
┌──────┬──────┬──────┬──────┬────────┬────────┬──────┐
│ 倉庫 ┆ 供給 ┆ 工場 ┆ 需要 ┆ 輸送費 ┆ 変数   ┆ 結果 │
│ ---  ┆ ---  ┆ ---  ┆ ---  ┆ ---    ┆ ---    ┆ ---  │
│ str  ┆ i64  ┆ str  ┆ i64  ┆ i64    ┆ object ┆ f64  │
╞══════╪══════╪══════╪══════╪════════╪════════╪══════╡
│ W1   ┆ 44   ┆ F4   ┆ 32   ┆ 10     ┆ v_03   ┆ 32.0 │
│ W2   ┆ 42   ┆ F1   ┆ 39   ┆ 13     ┆ v_04   ┆ 39.0 │
│ W3   ┆ 45   ┆ F2   ┆ 23   ┆ 10     ┆ v_09   ┆ 23.0 │
│ W3   ┆ 45   ┆ F3   ┆ 22   ┆ 11     ┆ v_10   ┆ 22.0 │
└──────┴──────┴──────┴──────┴────────┴────────┴──────┘
目的関数値 = 1299.0
```

## 数式を扱うときの注意

Polarsの特徴は、実データを含まずに、式（エクスプレッション）を記述できることです。
しかし、最適化モデルの変数を含んだ数式は、エクスプレッションとして記述できません。

たとえば、次の目的関数の式は実データで内積を取っています。

```python
xsum(df_変数.get_column("輸送費").to_numpy() * df_変数.get_column("変数").to_numpy())
```

エクスプレッションが数式を扱えれば次のように書けますが、実際には書けません。

```python
df_変数.select(pl.col("輸送費") * pl.col("変数")).sum()
```

このようにPolarsで数式を扱う場合、実データを使って計算を記述しないといけないことに注意してください。

## M1/M2 macでのインストールについて補足

Python-MIP`1.15.0`までに付属するCBCは、x86_64版なので、x86_64アーキテクチャで動作させる必要があります。しかし、M1/M2 macのx86_64では、Polarsが動きません。
その場合は、`polar`の代わりに`polars-lts-cpu`をインストールすることで、x86_64でPolarsを動かせます。

※ Python-MIP`1.16.0`が出れば、arm64でそのまま動かせるようになると思われます。

## まとめ

Polarsを使って、Python-MIPの数理モデルを作成しました。
Polarsは、DataFrameとSeriesが、1つの文で独立にメソッドチェーンを組み立てられます。
これにより、シンプルな構文のまま柔軟な処理を記述できます。
また、モデル作成の処理時間が（pandasより）高速になるかもしれません。

## 参考

https://qiita.com/SaitoTsutomu/items/bbd879280f5a934b5925

以上

