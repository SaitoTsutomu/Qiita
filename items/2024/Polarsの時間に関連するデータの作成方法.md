title: Polarsの時間に関連するデータの作成方法
tags: Python timezone Polars
url: https://qiita.com/SaitoTsutomu/items/ec6dbb5d6f35214dfbee
created_at: 2024-11-14 19:50:03+09:00
updated_at: 2024-12-04 07:04:49+09:00
body:

## 時間の型

Polarsで時間の型は、pl.Datetime（日時）, pl.Date（日付）, pl.Time（時刻）, pl.Duration（時間間隔）があります。
これらは、**`dt`属性**を通して時間関連のメソッドが使えます。
また、関連するデータとして、pl.Utf8（文字列）、エポック（整数）、総秒数（整数）があります。
エポック（UNIX時間ともいいます）は、1970年1月1日からの形式的な経過時間です。単位は、秒やマイクロ秒などです。

## 構成要素から作成

`pl.datetime()`、`pl.date()`、`pl.time()`、`pl.duration()`に年月日時分秒などを指定して作成できます。

```python
import polars as pl

df = pl.DataFrame().with_columns(
    datetime=pl.datetime(2024, 5, 1, 2, 3),
    date=pl.date(2024, 4, 30),
    time=pl.time(10, 20),
    duration=pl.duration(days=1, hours=2, minutes=3),
)
print(df)
```

```
shape: (1, 4)
┌─────────────────────┬────────────┬──────────┬──────────────┐
│ datetime            ┆ date       ┆ time     ┆ duration     │
│ ---                 ┆ ---        ┆ ---      ┆ ---          │
│ datetime[μs]        ┆ date       ┆ time     ┆ duration[μs] │
╞═════════════════════╪════════════╪══════════╪══════════════╡
│ 2024-05-01 02:03:00 ┆ 2024-04-30 ┆ 10:20:00 ┆ 1d 2h 3m     │
└─────────────────────┴────────────┴──────────┴──────────────┘
```

## CSVファイルから読み込み時に変換

`pl.read_csv()`で、`schema`や`schema_overrides`を指定することで、CSVファイルからの読み込み時に日時、日付、時刻に変換できます。

```python
import io

data = io.StringIO(
    "datetime,date,time\n2024-05-01T02:03:00,2024-04-30,10:20:00"
)
schema = {"datetime": pl.Datetime, "date": pl.Date, "time": pl.Time}
df = pl.read_csv(data, schema=schema)
print(df)
```

```
shape: (1, 3)
┌─────────────────────┬────────────┬──────────┐
│ datetime            ┆ date       ┆ time     │
│ ---                 ┆ ---        ┆ ---      │
│ datetime[μs]        ┆ date       ┆ time     │
╞═════════════════════╪════════════╪══════════╡
│ 2024-05-01 02:03:00 ┆ 2024-04-30 ┆ 10:20:00 │
└─────────────────────┴────────────┴──────────┘
```

## 他のデータから作成

他のデータから作成するには、次表などのようにできます。

| 作成するデータ | 変換元             | 方法                                             |
| :------------- | :----------------- | :----------------------------------------------- |
| `pl.Datetime`  | 文字列             | `str.to_datetime(書式)`                          |
| `pl.Datetime`  | エポックマイクロ秒 | `cast(pl.Datetime)`                              |
| `pl.Datetime`  | エポック秒         | `pl.from_epoch()`                                |
| `pl.Datetime`  | 日時や日付と時刻   | `dt.combine(時刻)`                               |
| `pl.Datetime`  | 日時と時間間隔     | 日時 + 時間間隔など                              |
| `pl.Date`      | 文字列             | `str.to_date(書式)`                              |
| `pl.Date`      | 日時               | `dt.date()`                                      |
| `pl.Date`      | 日付と時間間隔     | 日付 + 時間間隔など                              |
| `pl.Time`      | 文字列             | `str.to_time(書式)`                              |
| `pl.Time`      | 日時               | `dt.time()`                                      |
| `pl.Duration`  | 日時や日付         | 日時 - 日時、日付 - 日付<br>日時 - 日付など      |
| `pl.Duration`  | 時間間隔と時間間隔 | 時間間隔 + 時間間隔など                          |
| `pl.Duration`  | 時刻               | `cast(pl.Duration)`                              |
| `pl.Duration`  | 総マイクロ秒数     | `cast(pl.Duration)`                              |
| `pl.Utf8`      | 日時や日付や時刻   | `dt.to_string(書式)`                             |
| `エポック`     | 日時や日付         | `dt.epoch(単位)`<br>単位のデフォルトはマイクロ秒 |
| `総秒数`       | 時間間隔           | `dt.total_seconds()`                             |

```python
print(df.select(new_datetime=pl.col("date").dt.combine(pl.col("time"))))
print(df.select(pl.col("datetime").dt.to_string("%Y-%m-%d %H:%M:%S")))
print(pl.DataFrame(["20240102"]).select(pl.first().str.to_date("%Y%m%d")))
```

```
shape: (1, 1)
┌─────────────────────┐
│ new_datetime        │
│ ---                 │
│ datetime[μs]        │
╞═════════════════════╡
│ 2024-04-30 10:20:00 │
└─────────────────────┘
shape: (1, 1)
┌─────────────────────┐
│ datetime            │
│ ---                 │
│ str                 │
╞═════════════════════╡
│ 2024-05-01 02:03:00 │
└─────────────────────┘
shape: (1, 1)
┌────────────┐
│ column_0   │
│ ---        │
│ date       │
╞════════════╡
│ 2024-01-02 │
└────────────┘
```

**to_stringで使える書式**

https://docs.rs/chrono/latest/chrono/format/strftime/index.html

## 指定した範囲のデータの作成

指定した範囲のデータを作成するには、次のようにします。

| 作成するデータ     | 方法                  |
| :----------------- | :-------------------- |
| 指定した範囲の日時 | `pl.datetime_range()` |
| 指定した範囲の日付 | `pl.date_range()`     |
| 指定した範囲の時刻 | `pl.time_range()`     |

## タイムゾーンに関する変換

基本的なタイムゾーンあり（aware）とタイムゾーンなし（naive）の変換は次のようになります。

* 同じタイムゾーン間で日時の変換は、時刻の値を変えずタイムゾーンのみを変更する`dt.replace_time_zone(対象TZ)`を使う
* 異なるタイムゾーン間でawareな日時の変換は、（UTC基準で同一時刻になるように）時刻の値を変える`dt.convert_time_zone(対象TZ)`を使う
* 文字列から日時への変換は、`str.to_datetime(対象TZ)`を使う
* 独自書式の文字列を扱うときは、`dt.to_string(書式)`や`str.to_datetime(書式)`を使う

詳細は次表のように変換できます。

| 作成するデータ | 変換元              | 方法                           |
| :------------- | :------------------ | :----------------------------- |
| naiveな日時    | awareな日時         | `cast(pl.Datetime)`            |
| naiveな日時    | naiveな文字列(同TZ) | `str.to_datetime()`            |
| awareな日時    | naiveな日時(同TZ)   | `dt.replace_time_zone(対象TZ)` |
| awareな日時    | naiveな日時(UTC)    | `dt.convert_time_zone(対象TZ)` |
| awareな日時    | awareな日時(異TZ)   | `dt.convert_time_zone(対象TZ)` |
| awareな日時    | naiveな文字列(同TZ) | `str.to_datetime(対象TZ)`      |
| awareな日時    | awareな文字列       | `str.to_datetime(対象TZ)`      |
| naiveな文字列  | naiveな日時(同TZ)   | `cast(pl.Utf8)`                |
| naiveな文字列  | awareな日時(同TZ)   | naiveな日時を経由              |
| awareな文字列  | awareな日時(同TZ)   | `cast(pl.Utf8)`                |
| awareな文字列  | naiveな文字列(同TZ) | `str.to_datetime(対象TZ)`      |
| fmtあり文字列  | 日時(同TZ)          | `dt.to_string(書式)`           |
| 日時           | fmtあり文字列(同TZ) | `str.to_datetime(書式)`        |

```python
print(df.select(pl.col("datetime").dt.replace_time_zone("Asia/Tokyo")))
```

```
shape: (1, 1)
┌──────────────────────────┐
│ datetime                 │
│ ---                      │
│ datetime[μs, Asia/Tokyo] │
╞══════════════════════════╡
│ 2024-05-01 02:03:00 JST  │
└──────────────────────────┘
```

表の対象TZ（作成するデータのタイムゾーン）は、`"UTC"`や`"Asia/Tokyo"`などが使えます。
表にないケースは、awareな日時を経由してできないか検討してみてください。

また、`pl.read_csv()`の引数`schema`で`pl.Datatime(time_zone=...)`と指定することで、awareな日時として読み込めます。

```python
data = io.StringIO("datetime\n2024-05-01T02:03:00.000000+0900")
schema = {"datetime": pl.Datetime(time_zone="Asia/Tokyo")}
df = pl.read_csv(data, schema=schema)
print(df)
```

```
shape: (1, 1)
┌──────────────────────────┐
│ datetime                 │
│ ---                      │
│ datetime[μs, Asia/Tokyo] │
╞══════════════════════════╡
│ 2024-05-01 02:03:00 JST  │
└──────────────────────────┘
```

以上


