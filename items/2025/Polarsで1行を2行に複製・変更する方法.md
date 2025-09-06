title: Polarsで1行を2行に複製・変更する方法
tags: Python Polars
url: https://qiita.com/SaitoTsutomu/items/3802bfc82477d7825dc9
created_at: 2025-07-15 23:40:55+09:00
updated_at: 2025-07-15 23:40:55+09:00
body:

## やりたいこと

以下の`df`を考えます。

```python
import polars as pl

df = pl.DataFrame({
    "Path": ["A/B", "C/D"],
    "Score": [12, 43],
})
df
```

```
shape: (2, 2)
┌──────┬───────┐
│ Path ┆ Score │
│ ---  ┆ ---   │
│ str  ┆ i64   │
╞══════╪═══════╡
│ A/B  ┆ 12    │
│ C/D  ┆ 43    │
└──────┴───────┘
```

この`df`を下記のように変更する方法を紹介します。

```
shape: (4, 2)
┌──────┬───────┐
│ Path ┆ Score │
│ ---  ┆ ---   │
│ str  ┆ i64   │
╞══════╪═══════╡
│ A    ┆ 1     │
│ B    ┆ 2     │
│ C    ┆ 4     │
│ D    ┆ 3     │
└──────┴───────┘
```

## 準備

エクスプレッションをまとめたオブジェクトを用意しておきます。

```python
from types import SimpleNamespace

col = SimpleNamespace(
    Path=pl.col("Path"),
    Score=pl.col("Score"),
    index=pl.col("index"),
)
```

## ベタな方法

機械的に書けそうな方法です。

```python
rows = []
for row in df.rows(named=True):
    path1, path2 = row["Path"].split("/")
    score1, score2 = divmod(row["Score"], 10)
    rows.append({"Path": path1, "Score": score1})
    rows.append({"Path": path2, "Score": score2})
pl.DataFrame(rows)
```

コードは平易ですが、冗長な感じがします。

## 結合する方法

ちょっとPolarsっぽい方法です。

```python
df1 = df.select(
    col.Path.str.split("/").list[0],
    col.Score // 10,
)
df2 = df.select(
    col.Path.str.split("/").list[1],
    col.Score % 10,
)
pl.concat([df1, df2]).sort(col.Path)
```

無駄な処理がある上にメモリ効率もよくはないです。

## 長い方法

下記の処理をつなげる方法です。

* 要素をリスト化
* 1行を2行に複製
* インデックスを追加
* 奇数行か偶数行かでリストの要素を選択

```python
def divmod10(x):
    return [*divmod(x, 10)]

df.select(
    col.Path.str.split("/"),
    col.Score.map_elements(divmod10, return_dtype=list[int]),
).select(
    pl.all().repeat_by(2),
).explode(
    pl.all()
).with_row_index(
).select(
    Path=col.Path.list[col.index % 2],
    Score=col.Score.list[col.index % 2],
)
```

長いです。

## おすすめの方法

考え方は「長い方法」と似ていますが、すっきりしています。

```python
df.select(
    col.Path.str.split("/"),
    pl.concat_list([
        col.Score // 10,
        col.Score % 10,
    ]),
).explode(pl.all())
```

以上

