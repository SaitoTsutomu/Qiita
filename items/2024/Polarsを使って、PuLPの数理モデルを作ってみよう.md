title: Polarsを使って、PuLPの数理モデルを作ってみよう
tags: Python pandas 最適化 pulp Polars
url: https://qiita.com/SaitoTsutomu/items/bbd879280f5a934b5925
created_at: 2024-09-19 19:22:44+09:00
updated_at: 2024-09-21 19:12:19+09:00
body:

## 概要

次の記事では、pandasを使って、PuLPの数理モデルを作ってみました。

https://qiita.com/SaitoTsutomu/items/070ca9cb37c6b2b492f0

本記事では、**Polarsを使って、PuLPの数理モデルを作成**します。
PuLPの使い方については、上記記事を参照してください。
Polarsについては、公式ドキュメントを参照してください。

https://docs.pola.rs/

## 諸元

参照記事と同じように倉庫や工場の諸元を作成します。
ここでは、パッと見てわかりやすいように変数名に漢字を使っています。

```python
import polars as pl
from pulp import PULP_CBC_CMD, LpProblem, LpVariable, lpDot, lpSum, value

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
m = LpProblem()

# 変数表
_vars = [LpVariable(f"v_{i:02}", lowBound=0) for i in range(len(輸送費))]
df_変数 = (
    df_倉庫.join(df_工場, how="cross")
    .with_columns(pl.Series("輸送費", 輸送費))
    .with_columns(pl.Series("変数", _vars))
)

# 目的関数
m.setObjective(lpDot(df_変数["輸送費"], df_変数["変数"]))

# 制約条件
for _, group in df_変数.group_by("倉庫"):
    m += lpSum(group["変数"]) <= group["供給"][0]
for _, group in df_変数.group_by("工場"):
    m += lpSum(group["変数"]) >= group["需要"][0]
```

## ソルバーの実行と結果表示

```python
m.solve(PULP_CBC_CMD(msg=False))
_values = df_変数["変数"].map_elements(value, return_dtype=float)
df_変数 = df_変数.with_columns(_values.alias("結果"))
print(df_変数.filter(pl.col("結果") > 0))
print(f"目的関数値 = {m.objective.value()}")
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

## まとめ

Polarsを使って、PuLPの数理モデルを作成しました。
モデル作成を（pandasより）高速化したい場合に有効かもしれません。

## 参考

https://qiita.com/SaitoTsutomu/items/16f588265a01feacecbe

以上

