title: 【Python datetime】naiveとawareの変換
tags: Python datetime
url: https://qiita.com/SaitoTsutomu/items/ad66a614b92a76316f0e
created_at: 2023-04-22 17:17:48+09:00
updated_at: 2023-04-22 17:17:48+09:00
body:

# naiveとawareの変換

Pythonのdatetimeのタイムゾーンの扱い方の紹介です。
ここでは、datetimeの日本語訳を「日付時刻」と呼ぶことにします。

- naiveとawareとは
- naiveとawareの現在時刻
- naiveとaware間の変換
- 実行例

## naiveとawareとは

naiveはタイムゾーン**なし**の日付時刻、awareはタイムゾーン**あり**の日付時刻です。

https://docs.python.org/ja/3/library/datetime.html

## naiveとawareの現在時刻

日本標準時（Japan Standard Time、JST）と、協定世界時（UTC）の現在時刻は下記のように取得できます。
ただし、ローカルタイムはJSTとします。

```py
from datetime import datetime
from zoneinfo import ZoneInfo

jst = ZoneInfo("Asia/Tokyo")
utc = ZoneInfo("UTC")

naive_jst = datetime.now()
naive_utc = datetime.utcnow()
aware_jst = datetime.now(jst)
aware_utc = datetime.now(utc)
```

- naive_jst：naiveなJST
- naive_utc：naiveなUTC
- aware_jst：awareなJST
- aware_utc：awareなUTC

JSTは、UTCに9時間足したものです。
なので、naive_jstやaware_jstが10時のとき、naive_utcやaware_utcは1時です。

## naiveとaware間の変換

変換には、replaceとastimezoneを使います。

- replace：時刻を変更せずに、タイムゾーン情報のみを追加・変更・削除します。
- astimezone
  - naiveから：ローカルタイムとみなしてタイムゾーン変更します。
  - awareから：タイムゾーン変更します。

この2関数を使って、naiveとaware間の変換を説明します。

### awareからnaiveに変換

同じタイムゾーンの時刻に変更後に、タイムゾーン情報のみを削除します。

### naiveからawareに変換

タイムゾーンが変わらない変換は、単にタイムゾーン情報のみを追加します。

naiveのJSTからawareのUTCに変換は、ローカルタイムとみなしてタイムゾーン変更します。

naiveのUTCからawareのJSTに変換は、タイムゾーン情報のみを追加後にタイムゾーン変更します。

## 実行例

```python
from datetime import datetime
from zoneinfo import ZoneInfo

jst = ZoneInfo("Asia/Tokyo")
utc = ZoneInfo("UTC")

naive_jst = datetime.now()
naive_utc = datetime.utcnow()
aware_jst = datetime.now(jst)
aware_utc = datetime.now(utc)

print(f"{naive_jst = :%X %Z}")
print(f"{naive_utc = :%X %Z}")
print(f"{aware_jst = :%X %Z}")
print(f"{aware_utc = :%X %Z}")
print()
print("From aware to naive JST")
print(f"  {aware_jst.replace(tzinfo=None):%X %Z}")
_aware_jst = aware_utc.astimezone(jst)
print(f"  {_aware_jst.replace(tzinfo=None):%X %Z}")
print("From aware to naive UTC")
_aware_utc = aware_jst.astimezone(utc)
print(f"  {_aware_utc.replace(tzinfo=None):%X %Z}")
print(f"  {aware_utc.replace(tzinfo=None):%X %Z}")
print("From naive to aware JST")
print(f"  {naive_jst.replace(tzinfo=jst):%X %Z}")
_aware_utc = naive_utc.replace(tzinfo=utc)
print(f"  {_aware_utc.astimezone(jst):%X %Z}")
print("From naive to aware UTC")
print(f"  {naive_jst.astimezone(utc):%X %Z}")
print(f"  {naive_utc.replace(tzinfo=utc):%X %Z}")
```

```text:output
naive_jst = 10:10:00 
naive_utc = 01:10:00 
aware_jst = 10:10:00 JST
aware_utc = 01:10:00 UTC

From aware to naive JST
  10:10:00 
  10:10:00 
From aware to naive UTC
  01:10:00 
  01:10:00 
From naive to aware JST
  10:10:00 JST
  10:10:00 JST
From naive to aware UTC
  01:10:00 UTC
  01:10:00 UTC
```

以上

