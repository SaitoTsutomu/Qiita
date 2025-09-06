title: PandasとPolarsで、辞書のリストの扱い方
tags: Python pandas Polars
url: https://qiita.com/SaitoTsutomu/items/a2c491207fb41b045f7b
created_at: 2025-07-03 23:04:51+09:00
updated_at: 2025-07-03 23:22:37+09:00
body:

## 概要

列の要素が辞書のリストとします。特定のキーが特定の値になる辞書の別のキーの値を取得する方法を紹介します。

## 元データ

下記を元データとします。

```python
data = [
    {
        "user_id": 101,
        "answer": [
            {"cell": 1, "text": "いいえ"},
            {"cell": 9, "text": "習慣"},
        ],
    },
    {
        "user_id": 102,
        "answer": [
            {"cell": 1, "text": "はい"},
            {"cell": 9, "text": "雰囲気"},
        ],
    },
    {
        "user_id": 103,
        "answer": [
            {"cell": 1, "text": "はい"},
        ],
    },
]
```

このデータを使って、下記の2つを求めます。

* answer内で、cellが1のときのtextの値が「はい」かどうか
* answer内で、cellが9のときのtextの値。ただし、存在しないときは空文字列

## Pandasの例

`df_pd`を元のDataFrameとします。

```python
import pandas as pd

df_pd = pd.DataFrame(data)
df_pd
```

|    |   user_id | answer                                                       |
|---:|----------:|:-------------------------------------------------------------|
|  0 |       101 | [{'cell': 1, 'text': 'いいえ'}, {'cell': 9, 'text': '習慣'}] |
|  1 |       102 | [{'cell': 9, 'text': '雰囲気'}, {'cell': 1, 'text': 'はい'}] |
|  2 |       103 | [{'cell': 1, 'text': 'はい'}]                                |

欲しい結果（`df_pd_new`）は下記のようになります。

```python
def get_target(answer_list):
    for item in answer_list:
        if item.get("cell") == 1:
            return item.get("text") == "はい"
    return False

def get_reason(answer_list):
    for item in answer_list:
        if item.get("cell") == 9:
            return item.get("text")
    return ""

df_pd_new = df_pd.assign(
    target=df_pd["answer"].map(get_target),
    resoson=df_pd["answer"].map(get_reason),
).drop("answer", axis=1)

df_pd_new
```

|    |   user_id | target   | resoson   |
|---:|----------:|:---------|:----------|
|  0 |       101 | False    | 習慣      |
|  1 |       102 | True     | 雰囲気    |
|  2 |       103 | True     |           |

## Polarsの例

`df_pl`を元のDataFrameとします。

```python
import polars as pl

df_pl = pl.DataFrame(data)
df_pl
```

```
shape: (3, 2)
┌─────────┬────────────────────────────┐
│ user_id ┆ answer                     │
│ ---     ┆ ---                        │
│ i64     ┆ list[struct[2]]            │
╞═════════╪════════════════════════════╡
│ 101     ┆ [{1,"いいえ"}, {9,"習慣"}] │
│ 102     ┆ [{9,"雰囲気"}, {1,"はい"}] │
│ 103     ┆ [{1,"はい"}]               │
└─────────┴────────────────────────────┘
```

表示では`{1,"いいえ"}`のようになっていますが、オブジェクトとしては`{'cell': 1, 'text': 'いいえ'}`です。値だけ表示されています。

欲しい結果（`df_pl_new`）は下記のようになります。

```python
df_pl_new = df_pl.select(
    "user_id",
    target=pl.col("answer").list.eval(
        pl.element().filter(
            pl.element().struct.field("cell") == 1
        ).struct.field("text") == "はい"
    ).list.first().fill_null(False),
    resoson=pl.col("answer").list.eval(
        pl.element().filter(
            pl.element().struct.field("cell") == 9
        ).struct.field("text")
    ).list.first().fill_null(""),
)

df_pl_new
```

```
shape: (3, 3)
┌─────────┬────────┬─────────┐
│ user_id ┆ target ┆ resoson │
│ ---     ┆ ---    ┆ ---     │
│ i64     ┆ bool   ┆ str     │
╞═════════╪════════╪═════════╡
│ 101     ┆ false  ┆ 習慣    │
│ 102     ┆ true   ┆ 雰囲気  │
│ 103     ┆ true   ┆         │
└─────────┴────────┴─────────┘
```

だいぶ、ややこしいですが、慣れればpandasより見やすいと思います。

簡単に解説します。

* リスト内の要素について処理をしたいときは、`list.eval()`を使います[^1]
* 要素のフィルタリングは、`pl.element().filter()`を使います[^2][^3]
* 辞書である要素の指定したキーの値は、`pl.element().struct.field()`を使います[^4]

[^1]: https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.list.eval.html
[^2]: https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.element.html
[^3]: https://docs.pola.rs/api/python/dev/reference/expressions/api/polars.Expr.filter.html
[^4]: https://docs.pola.rs/api/python/dev/reference/expressions/api/polars.Expr.struct.field.html

### 別の方法

対象の辞書がリストの固定の位置にあれば、もっと簡単にかけます。

```python
df_pl["answer"].list[0].struct[1]
```

```
shape: (3,)
Series: 'text' [str]
[
	"いいえ"
	"雰囲気"
	"はい"
]
```

今回は順番が固定でないので、上記のように求めたいものにはなりません。

以上

