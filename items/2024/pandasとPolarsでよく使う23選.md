title: pandasとPolarsでよく使う23選
tags: Python pandas Polars
url: https://qiita.com/SaitoTsutomu/items/6087017c0da36d7b752f
created_at: 2024-11-01 00:06:50+09:00
updated_at: 2024-11-03 23:45:32+09:00
body:

次の記事を少しアレンジしてPolarsでもやってみました。

https://qiita.com/tapitapi/items/fdd86439840dfa96c312

いろいろな書き方がありますが、修正しやすさとわかりやすさで選びました。
なお、結果は完全に同じではないです。
出力にはわかりやすいように改行を追加しています。

## データとモジュールの準備

```python
from pathlib import Path
from dataclasses import make_dataclass
import pandas as pd
import polars as pl

dct = {
    "data": [
        ["2024-01-04", "A", "家電", "電球", 4, 1000, 4000],
        ["2024-02-06", "A", "家電", "電子レンジ", 1, 50000, 50000],
        ["2024-03-10", "A", "家電", "テレビ", 1, 150000, 150000],
        ["2024-05-06", "B", "家電", "洗濯機", 1, 200000, 200000],
        ["2024-05-04", "B", "家電", "エアコン", 1, 180000, 180000],
        ["2024-07-10", "B", "家電", "照明器具", 1, 10000, 10000],
        ["2024-10-13", "B", "家電", "電池", 5, 300, 1500],
        ["2024-01-06", "C", "家具", "椅子", 4, 10000, 40000],
        ["2024-02-07", "C", "家具", "机", 1, 50000, 50000],
        ["2024-03-10", "D", "家具", "タンス", 1, 70000, 70000],
        ["2024-06-10", "D", "家具", "布団", 2, 30000, 60000],
        ["2024-10-06", "D", "家具", "枕", 2, 5000, 10000],
        ["2024-07-04", "C", "文具", "シャープペンシル", 3, 600, 1800],
        ["2024-08-09", "C", "文具", "ボールペン", 3, 300, 900],
        ["2024-10-10", "C", "文具", "消しゴム", 5, 100, 500],
        ["2024-05-06", "A", "文具", "ノート", 10, 100, 1000],
        ["2024-07-03", "B", "文具", "ノート", 10, 100, 1000],
        ["2024-04-12", "B", "文具", "ボー ルペン", 1, 300, 300],
    ],
    "columns": ["日付", "購入店", "種類", "名称", "数量", "単価", "価格"],
}
```

## pandas

```python
df = pd.DataFrame(**dct)

print("1.行列の数", df.shape)
print("2.行名", df.index)
print("3.列名", df.columns)
print("4.列の種類\n", df.dtypes)
print("5.特定の列のパラメータ種類", df["種類"].unique())
print("6.特定の列のパラメータの集計\n", df["種類"].value_counts())
print("7.列の切り取り\n", df[["種類", "名称"]].head(3))
print("8.先頭から指定した行数\n", df.head(3))
print("9.先頭から指定した行数\n", df.tail(3))
print("10.行と列の幅を絞る\n", _df := df.iloc[1:4,3:])
print("11.行列入れ替え\n", _df.transpose())
print("12.各列の集計\n", df[["数量", "単価", "価格"]].sum())
print("13.昇順でソート\n", df.sort_values("単価").head(3))
print("14.フィルタ:文字列指定\n", df[df["購入店"].isin({"A", "C"})].head(3))
print("15.フィルタ:含む文字列\n", df[df["日付"].str.contains("2024-05")])
print("16.フィルタ:終端文字列比較\n", df[df["種類"].str.endswith("具")].head(3))
print("17.フィルタ:開始文字列比較\n", df[df["種類"].str.startswith("文")].head(3))
print("18.フィルタ:正規表現文字列比較\n", df[df["名称"].str.match("^.{3}$")])
print("19.フィルタ\n", df.query('価格 > 10000 and 購入店 == "A"'))
print("20.指定列の最大値の行\n", df.iloc[df["価格"].idxmax()])
print("21.指定列の最小値の行\n", df.iloc[df["価格"].idxmin()])
print("22.欠損値を'0'で埋める\n", df.fillna(0).head(3))
# 23.出力
df.to_json("out.json")
df.to_html("out.html")
df.to_string("out.txt")
df.to_clipboard()
```

**出力**

```
1.行列の数 (18, 7)

2.行名 RangeIndex(start=0, stop=18, step=1)

3.列名 Index(['日付', '購入店', '種類', '名称', '数量', '単価', '価格'], dtype='object')

4.列の種類
 日付     object
購入店    object
種類     object
名称     object
数量      int64
単価      int64
価格      int64
dtype: object

5.特定の列のパラメータ種類 ['家電' '家具' '文具']

6.特定の列のパラメータの集計
 種類
家電    7
文具    6
家具    5
Name: count, dtype: int64

7.列の切り取り
    種類     名称
0  家電     電球
1  家電  電子レンジ
2  家電    テレビ

8.先頭から指定した行数
            日付 購入店  種類     名称  数量      単価      価格
0  2024-01-04   A  家電     電球   4    1000    4000
1  2024-02-06   A  家電  電子レンジ   1   50000   50000
2  2024-03-10   A  家電    テレビ   1  150000  150000

9.先頭から指定した行数
             日付 購入店  種類      名称  数量   単価    価格
15  2024-05-06   A  文具     ノート  10  100  1000
16  2024-07-03   B  文具     ノート  10  100  1000
17  2024-04-12   B  文具  ボー ルペン   1  300   300

10.行と列の幅を絞る
       名称  数量      単価      価格
1  電子レンジ   1   50000   50000
2    テレビ   1  150000  150000
3    洗濯機   1  200000  200000

11.行列入れ替え
         1       2       3
名称  電子レンジ     テレビ     洗濯機
数量      1       1       1
単価  50000  150000  200000
価格  50000  150000  200000

12.各列の集計
 数量        56
単価    757800
価格    831000
dtype: int64

13.昇順でソート
             日付 購入店  種類    名称  数量   単価    価格
15  2024-05-06   A  文具   ノート  10  100  1000
14  2024-10-10   C  文具  消しゴム   5  100   500
16  2024-07-03   B  文具   ノート  10  100  1000

14.フィルタ:文字列指定
            日付 購入店  種類     名称  数量      単価      価格
0  2024-01-04   A  家電     電球   4    1000    4000
1  2024-02-06   A  家電  電子レンジ   1   50000   50000
2  2024-03-10   A  家電    テレビ   1  150000  150000

15.フィルタ:含む文字列
             日付 購入店  種類    名称  数量      単価      価格
3   2024-05-06   B  家電   洗濯機   1  200000  200000
4   2024-05-04   B  家電  エアコン   1  180000  180000
15  2024-05-06   A  文具   ノート  10     100    1000

16.フィルタ:終端文字列比較
            日付 購入店  種類   名称  数量     単価     価格
7  2024-01-06   C  家具   椅子   4  10000  40000
8  2024-02-07   C  家具    机   1  50000  50000
9  2024-03-10   D  家具  タンス   1  70000  70000

17.フィルタ:開始文字列比較
             日付 購入店  種類        名称  数量   単価    価格
12  2024-07-04   C  文具  シャープペンシル   3  600  1800
13  2024-08-09   C  文具     ボールペン   3  300   900
14  2024-10-10   C  文具      消しゴム   5  100   500

18.フィルタ:正規表現文字列比較
             日付 購入店  種類   名称  数量      単価      価格
2   2024-03-10   A  家電  テレビ   1  150000  150000
3   2024-05-06   B  家電  洗濯機   1  200000  200000
9   2024-03-10   D  家具  タンス   1   70000   70000
15  2024-05-06   A  文具  ノート  10     100    1000
16  2024-07-03   B  文具  ノート  10     100    1000

19.フィルタ
            日付 購入店  種類     名称  数量      単価      価格
1  2024-02-06   A  家電  電子レンジ   1   50000   50000
2  2024-03-10   A  家電    テレビ   1  150000  150000

20.指定列の最大値の行
 日付     2024-05-06
購入店             B
種類             家電
名称            洗濯機
数量              1
単価         200000
価格         200000
Name: 3, dtype: object

21.指定列の最小値の行
 日付     2024-04-12
購入店             B
種類             文具
名称         ボー ルペン
数量              1
単価            300
価格            300
Name: 17, dtype: object

22.欠損値を'0'で埋める
            日付 購入店  種類     名称  数量      単価      価格
0  2024-01-04   A  家電     電球   4    1000    4000
1  2024-02-06   A  家電  電子レンジ   1   50000   50000
2  2024-03-10   A  家電    テレビ   1  150000  150000
```

## Polars

```python
df = pl.DataFrame(*dct.values(), orient="row")
# 列のエクスプレッション
col = make_dataclass("Col", df.columns)(*map(pl.col, df.columns))

print("1.行列の数", df.shape)
print("2.行名\n", df.with_row_index().get_column("index"))
print("3.列名", df.columns)
print("4.列の種類", df.dtypes)
print("5.特定の列のパラメータ種類\n", df.select(col.種類.unique()))
print("6.特定の列のパラメータの集計\n", df.select(col.種類.value_counts()))
print("7.列の切り取り\n", df.select(col.種類, col.名称).head(3))
print("8.先頭から指定した行数\n", df.head(3))
print("9.先頭から指定した行数\n", df.tail(3))
print("10.行と列の幅を絞る\n", _df := df.slice(1, 3).select(df.columns[3:]))
print("11.行列入れ替え\n", _df.transpose())
print("12.各列の集計\n", df.select(col.数量, col.単価, col.価格).sum())
print("13.昇順でソート\n", df.sort(col.単価).head(3))
print("14.フィルタ:文字列指定\n", df.filter(col.購入店.is_in({"A", "C"})).head(3))
print("15.フィルタ:含む文字列\n", df.filter(col.日付.str.contains("2024-05")))
print("16.フィルタ:終端文字列比較\n", df.filter(col.種類.str.ends_with("具")).head(3))
print("17.フィルタ:開始文字列比較\n", df.filter(col.種類.str.starts_with("文")).head(3))
print("18.フィルタ:正規表現文字列比較\n", df.filter(col.名称.str.contains("^.{3}$")))
print("19.フィルタ\n", df.filter((col.価格 > 10000) & (col.購入店 == "A")))
print("20.指定列の最大値の行\n", df.filter(col.価格 == col.価格.max()))
print("21.指定列の最小値の行\n", df.filter(col.価格 == col.価格.min()))
print("22.欠損値を'0'で埋める\n", df.fill_null(0).head(3))
# 23.出力
df.write_json("out.json")
Path("out.html").write_text(df._repr_html_())
Path("out.txt").write_text(str(df))
df.write_clipboard()
```

**出力**

```
1.行列の数 (18, 7)

2.行名
 shape: (18,)
Series: 'index' [u32]
[
	0
	1
	2
	3
	4
	…
	13
	14
	15
	16
	17
]

3.列名 ['日付', '購入店', '種類', '名称', '数量', '単価', '価格']

4.列の種類 [String, String, String, String, Int64, Int64, Int64]

5.特定の列のパラメータ種類
 shape: (3, 1)
┌──────┐
│ 種類 │
│ ---  │
│ str  │
╞══════╡
│ 文具 │
│ 家具 │
│ 家電 │
└──────┘

6.特定の列のパラメータの集計
 shape: (3, 1)
┌────────────┐
│ 種類       │
│ ---        │
│ struct[2]  │
╞════════════╡
│ {"家具",5} │
│ {"文具",6} │
│ {"家電",7} │
└────────────┘

7.列の切り取り
 shape: (3, 2)
┌──────┬────────────┐
│ 種類 ┆ 名称       │
│ ---  ┆ ---        │
│ str  ┆ str        │
╞══════╪════════════╡
│ 家電 ┆ 電球       │
│ 家電 ┆ 電子レンジ │
│ 家電 ┆ テレビ     │
└──────┴────────────┘

8.先頭から指定した行数
 shape: (3, 7)
┌────────────┬────────┬──────┬────────────┬──────┬────────┬────────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称       ┆ 数量 ┆ 単価   ┆ 価格   │
│ ---        ┆ ---    ┆ ---  ┆ ---        ┆ ---  ┆ ---    ┆ ---    │
│ str        ┆ str    ┆ str  ┆ str        ┆ i64  ┆ i64    ┆ i64    │
╞════════════╪════════╪══════╪════════════╪══════╪════════╪════════╡
│ 2024-01-04 ┆ A      ┆ 家電 ┆ 電球       ┆ 4    ┆ 1000   ┆ 4000   │
│ 2024-02-06 ┆ A      ┆ 家電 ┆ 電子レンジ ┆ 1    ┆ 50000  ┆ 50000  │
│ 2024-03-10 ┆ A      ┆ 家電 ┆ テレビ     ┆ 1    ┆ 150000 ┆ 150000 │
└────────────┴────────┴──────┴────────────┴──────┴────────┴────────┘

9.先頭から指定した行数
 shape: (3, 7)
┌────────────┬────────┬──────┬─────────────┬──────┬──────┬──────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称        ┆ 数量 ┆ 単価 ┆ 価格 │
│ ---        ┆ ---    ┆ ---  ┆ ---         ┆ ---  ┆ ---  ┆ ---  │
│ str        ┆ str    ┆ str  ┆ str         ┆ i64  ┆ i64  ┆ i64  │
╞════════════╪════════╪══════╪═════════════╪══════╪══════╪══════╡
│ 2024-05-06 ┆ A      ┆ 文具 ┆ ノート      ┆ 10   ┆ 100  ┆ 1000 │
│ 2024-07-03 ┆ B      ┆ 文具 ┆ ノート      ┆ 10   ┆ 100  ┆ 1000 │
│ 2024-04-12 ┆ B      ┆ 文具 ┆ ボー ルペン ┆ 1    ┆ 300  ┆ 300  │
└────────────┴────────┴──────┴─────────────┴──────┴──────┴──────┘

10.行と列の幅を絞る
 shape: (3, 4)
┌────────────┬──────┬────────┬────────┐
│ 名称       ┆ 数量 ┆ 単価   ┆ 価格   │
│ ---        ┆ ---  ┆ ---    ┆ ---    │
│ str        ┆ i64  ┆ i64    ┆ i64    │
╞════════════╪══════╪════════╪════════╡
│ 電子レンジ ┆ 1    ┆ 50000  ┆ 50000  │
│ テレビ     ┆ 1    ┆ 150000 ┆ 150000 │
│ 洗濯機     ┆ 1    ┆ 200000 ┆ 200000 │
└────────────┴──────┴────────┴────────┘

11.行列入れ替え
 shape: (4, 3)
┌────────────┬──────────┬──────────┐
│ column_0   ┆ column_1 ┆ column_2 │
│ ---        ┆ ---      ┆ ---      │
│ str        ┆ str      ┆ str      │
╞════════════╪══════════╪══════════╡
│ 電子レンジ ┆ テレビ   ┆ 洗濯機   │
│ 1          ┆ 1        ┆ 1        │
│ 50000      ┆ 150000   ┆ 200000   │
│ 50000      ┆ 150000   ┆ 200000   │
└────────────┴──────────┴──────────┘

12.各列の集計
 shape: (1, 3)
┌──────┬────────┬────────┐
│ 数量 ┆ 単価   ┆ 価格   │
│ ---  ┆ ---    ┆ ---    │
│ i64  ┆ i64    ┆ i64    │
╞══════╪════════╪════════╡
│ 56   ┆ 757800 ┆ 831000 │
└──────┴────────┴────────┘

13.昇順でソート
 shape: (3, 7)
┌────────────┬────────┬──────┬──────────┬──────┬──────┬──────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称     ┆ 数量 ┆ 単価 ┆ 価格 │
│ ---        ┆ ---    ┆ ---  ┆ ---      ┆ ---  ┆ ---  ┆ ---  │
│ str        ┆ str    ┆ str  ┆ str      ┆ i64  ┆ i64  ┆ i64  │
╞════════════╪════════╪══════╪══════════╪══════╪══════╪══════╡
│ 2024-10-10 ┆ C      ┆ 文具 ┆ 消しゴム ┆ 5    ┆ 100  ┆ 500  │
│ 2024-05-06 ┆ A      ┆ 文具 ┆ ノート   ┆ 10   ┆ 100  ┆ 1000 │
│ 2024-07-03 ┆ B      ┆ 文具 ┆ ノート   ┆ 10   ┆ 100  ┆ 1000 │
└────────────┴────────┴──────┴──────────┴──────┴──────┴──────┘

14.フィルタ:文字列指定
 shape: (3, 7)
┌────────────┬────────┬──────┬────────────┬──────┬────────┬────────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称       ┆ 数量 ┆ 単価   ┆ 価格   │
│ ---        ┆ ---    ┆ ---  ┆ ---        ┆ ---  ┆ ---    ┆ ---    │
│ str        ┆ str    ┆ str  ┆ str        ┆ i64  ┆ i64    ┆ i64    │
╞════════════╪════════╪══════╪════════════╪══════╪════════╪════════╡
│ 2024-01-04 ┆ A      ┆ 家電 ┆ 電球       ┆ 4    ┆ 1000   ┆ 4000   │
│ 2024-02-06 ┆ A      ┆ 家電 ┆ 電子レンジ ┆ 1    ┆ 50000  ┆ 50000  │
│ 2024-03-10 ┆ A      ┆ 家電 ┆ テレビ     ┆ 1    ┆ 150000 ┆ 150000 │
└────────────┴────────┴──────┴────────────┴──────┴────────┴────────┘

15.フィルタ:含む文字列
 shape: (3, 7)
┌────────────┬────────┬──────┬──────────┬──────┬────────┬────────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称     ┆ 数量 ┆ 単価   ┆ 価格   │
│ ---        ┆ ---    ┆ ---  ┆ ---      ┆ ---  ┆ ---    ┆ ---    │
│ str        ┆ str    ┆ str  ┆ str      ┆ i64  ┆ i64    ┆ i64    │
╞════════════╪════════╪══════╪══════════╪══════╪════════╪════════╡
│ 2024-05-06 ┆ B      ┆ 家電 ┆ 洗濯機   ┆ 1    ┆ 200000 ┆ 200000 │
│ 2024-05-04 ┆ B      ┆ 家電 ┆ エアコン ┆ 1    ┆ 180000 ┆ 180000 │
│ 2024-05-06 ┆ A      ┆ 文具 ┆ ノート   ┆ 10   ┆ 100    ┆ 1000   │
└────────────┴────────┴──────┴──────────┴──────┴────────┴────────┘

16.フィルタ:終端文字列比較
 shape: (3, 7)
┌────────────┬────────┬──────┬────────┬──────┬───────┬───────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称   ┆ 数量 ┆ 単価  ┆ 価格  │
│ ---        ┆ ---    ┆ ---  ┆ ---    ┆ ---  ┆ ---   ┆ ---   │
│ str        ┆ str    ┆ str  ┆ str    ┆ i64  ┆ i64   ┆ i64   │
╞════════════╪════════╪══════╪════════╪══════╪═══════╪═══════╡
│ 2024-01-06 ┆ C      ┆ 家具 ┆ 椅子   ┆ 4    ┆ 10000 ┆ 40000 │
│ 2024-02-07 ┆ C      ┆ 家具 ┆ 机     ┆ 1    ┆ 50000 ┆ 50000 │
│ 2024-03-10 ┆ D      ┆ 家具 ┆ タンス ┆ 1    ┆ 70000 ┆ 70000 │
└────────────┴────────┴──────┴────────┴──────┴───────┴───────┘

17.フィルタ:開始文字列比較
 shape: (3, 7)
┌────────────┬────────┬──────┬──────────────────┬──────┬──────┬──────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称             ┆ 数量 ┆ 単価 ┆ 価格 │
│ ---        ┆ ---    ┆ ---  ┆ ---              ┆ ---  ┆ ---  ┆ ---  │
│ str        ┆ str    ┆ str  ┆ str              ┆ i64  ┆ i64  ┆ i64  │
╞════════════╪════════╪══════╪══════════════════╪══════╪══════╪══════╡
│ 2024-07-04 ┆ C      ┆ 文具 ┆ シャープペンシル ┆ 3    ┆ 600  ┆ 1800 │
│ 2024-08-09 ┆ C      ┆ 文具 ┆ ボールペン       ┆ 3    ┆ 300  ┆ 900  │
│ 2024-10-10 ┆ C      ┆ 文具 ┆ 消しゴム         ┆ 5    ┆ 100  ┆ 500  │
└────────────┴────────┴──────┴──────────────────┴──────┴──────┴──────┘

18.フィルタ:正規表現文字列比較
 shape: (5, 7)
┌────────────┬────────┬──────┬────────┬──────┬────────┬────────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称   ┆ 数量 ┆ 単価   ┆ 価格   │
│ ---        ┆ ---    ┆ ---  ┆ ---    ┆ ---  ┆ ---    ┆ ---    │
│ str        ┆ str    ┆ str  ┆ str    ┆ i64  ┆ i64    ┆ i64    │
╞════════════╪════════╪══════╪════════╪══════╪════════╪════════╡
│ 2024-03-10 ┆ A      ┆ 家電 ┆ テレビ ┆ 1    ┆ 150000 ┆ 150000 │
│ 2024-05-06 ┆ B      ┆ 家電 ┆ 洗濯機 ┆ 1    ┆ 200000 ┆ 200000 │
│ 2024-03-10 ┆ D      ┆ 家具 ┆ タンス ┆ 1    ┆ 70000  ┆ 70000  │
│ 2024-05-06 ┆ A      ┆ 文具 ┆ ノート ┆ 10   ┆ 100    ┆ 1000   │
│ 2024-07-03 ┆ B      ┆ 文具 ┆ ノート ┆ 10   ┆ 100    ┆ 1000   │
└────────────┴────────┴──────┴────────┴──────┴────────┴────────┘

19.フィルタ
 shape: (2, 7)
┌────────────┬────────┬──────┬────────────┬──────┬────────┬────────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称       ┆ 数量 ┆ 単価   ┆ 価格   │
│ ---        ┆ ---    ┆ ---  ┆ ---        ┆ ---  ┆ ---    ┆ ---    │
│ str        ┆ str    ┆ str  ┆ str        ┆ i64  ┆ i64    ┆ i64    │
╞════════════╪════════╪══════╪════════════╪══════╪════════╪════════╡
│ 2024-02-06 ┆ A      ┆ 家電 ┆ 電子レンジ ┆ 1    ┆ 50000  ┆ 50000  │
│ 2024-03-10 ┆ A      ┆ 家電 ┆ テレビ     ┆ 1    ┆ 150000 ┆ 150000 │
└────────────┴────────┴──────┴────────────┴──────┴────────┴────────┘

20.指定列の最大値の行
 shape: (1, 7)
┌────────────┬────────┬──────┬────────┬──────┬────────┬────────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称   ┆ 数量 ┆ 単価   ┆ 価格   │
│ ---        ┆ ---    ┆ ---  ┆ ---    ┆ ---  ┆ ---    ┆ ---    │
│ str        ┆ str    ┆ str  ┆ str    ┆ i64  ┆ i64    ┆ i64    │
╞════════════╪════════╪══════╪════════╪══════╪════════╪════════╡
│ 2024-05-06 ┆ B      ┆ 家電 ┆ 洗濯機 ┆ 1    ┆ 200000 ┆ 200000 │
└────────────┴────────┴──────┴────────┴──────┴────────┴────────┘

21.指定列の最小値の行
 shape: (1, 7)
┌────────────┬────────┬──────┬─────────────┬──────┬──────┬──────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称        ┆ 数量 ┆ 単価 ┆ 価格 │
│ ---        ┆ ---    ┆ ---  ┆ ---         ┆ ---  ┆ ---  ┆ ---  │
│ str        ┆ str    ┆ str  ┆ str         ┆ i64  ┆ i64  ┆ i64  │
╞════════════╪════════╪══════╪═════════════╪══════╪══════╪══════╡
│ 2024-04-12 ┆ B      ┆ 文具 ┆ ボー ルペン ┆ 1    ┆ 300  ┆ 300  │
└────────────┴────────┴──────┴─────────────┴──────┴──────┴──────┘

22.欠損値を'0'で埋める
 shape: (3, 7)
┌────────────┬────────┬──────┬────────────┬──────┬────────┬────────┐
│ 日付       ┆ 購入店 ┆ 種類 ┆ 名称       ┆ 数量 ┆ 単価   ┆ 価格   │
│ ---        ┆ ---    ┆ ---  ┆ ---        ┆ ---  ┆ ---    ┆ ---    │
│ str        ┆ str    ┆ str  ┆ str        ┆ i64  ┆ i64    ┆ i64    │
╞════════════╪════════╪══════╪════════════╪══════╪════════╪════════╡
│ 2024-01-04 ┆ A      ┆ 家電 ┆ 電球       ┆ 4    ┆ 1000   ┆ 4000   │
│ 2024-02-06 ┆ A      ┆ 家電 ┆ 電子レンジ ┆ 1    ┆ 50000  ┆ 50000  │
│ 2024-03-10 ┆ A      ┆ 家電 ┆ テレビ     ┆ 1    ┆ 150000 ┆ 150000 │
└────────────┴────────┴──────┴────────────┴──────┴────────┴────────┘
```

## 補足

Polarsの記述のいくつかでは、pandasと同じように書くこともできますが、あえて別の書き方をしています。
その結果、コード量は増えますが、わかりやすくなっていると思います。

以上

