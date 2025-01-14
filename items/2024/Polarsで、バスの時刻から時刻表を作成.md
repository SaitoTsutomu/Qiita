title: Polarsで、バスの時刻から時刻表を作成
tags: Python Polars
url: https://qiita.com/SaitoTsutomu/items/334dde068364b756c9f0
created_at: 2024-12-25 20:24:28+09:00
updated_at: 2024-12-25 20:29:04+09:00
body:

Polarsのlistを使ったサンプルです。

下記のようなバスの到着時刻の表があります。

```python
import polars as pl

times = ["07:20", "07:45", "08:10", "08:30", "08:50", "09:10", "09:30", "09:50"]
df_time = pl.Series("time", times).str.to_time("%H:%M").to_frame()
df_time
```

<small>shape: (8, 1)</small><table border="1" class="dataframe"><thead><tr><th>time</th></tr><tr><td>time</td></tr></thead><tbody><tr><td>07:20:00</td></tr><tr><td>07:45:00</td></tr><tr><td>08:10:00</td></tr><tr><td>08:30:00</td></tr><tr><td>08:50:00</td></tr><tr><td>09:10:00</td></tr><tr><td>09:30:00</td></tr><tr><td>09:50:00</td></tr></tbody></table>

この表からバスの時刻表を作成してみましょう。
バスの時刻表は、時間ごとに、分をリストで表現します。

Polarsでは次のようにできます。

```python
df_dia = df_time.group_by(
    hour=pl.col("time").dt.hour(), maintain_order=True
).agg(minute=pl.col("time").dt.minute())
df_dia
```

<small>shape: (3, 2)</small><table border="1" class="dataframe"><thead><tr><th>hour</th><th>minute</th></tr><tr><td>i8</td><td>list[i8]</td></tr></thead><tbody><tr><td>7</td><td>[20, 45]</td></tr><tr><td>8</td><td>[10, 30, 50]</td></tr><tr><td>9</td><td>[10, 30, 50]</td></tr></tbody></table>

**ポイント**

Polarsではエクスプレッションでグルーピングできます。ここでは、列timeの`dt.hour()`を使ってグルーピングしています。
`agg()`で`dt.minute()`を指定すると、分のリストになります。

元の時刻に戻すには次のようにします。

```python
df_dia.explode("minute").select(time=pl.time("hour", "minute"))
```

<small>shape: (8, 1)</small><table border="1" class="dataframe"><thead><tr><th>time</th></tr><tr><td>time</td></tr></thead><tbody><tr><td>07:20:00</td></tr><tr><td>07:45:00</td></tr><tr><td>08:10:00</td></tr><tr><td>08:30:00</td></tr><tr><td>08:50:00</td></tr><tr><td>09:10:00</td></tr><tr><td>09:30:00</td></tr><tr><td>09:50:00</td></tr></tbody></table>

**ポイント**

`explode()`でlistを行に分解します。
分解したhourとminuteから`pl.time()`で時刻を作成できます。

**参考**

https://qiita.com/SaitoTsutomu/items/ec6dbb5d6f35214dfbee

以上

