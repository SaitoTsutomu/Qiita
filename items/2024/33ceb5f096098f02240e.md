title: CSVのデータをDjangoのORMでさくっと扱う方法
tags: Python Django SQLite3 ORM
url: https://qiita.com/SaitoTsutomu/items/33ceb5f096098f02240e
created_at: 2024-05-30 20:43:05+09:00
updated_at: 2024-05-30 20:43:05+09:00
body:

試したらできたので、メモとして記事にしました。

## やること

下記のCSV（person.csv）のデータをDjangoのORMで使ってみましょう。

```csv:person.csv
name,age,city
Alice,30,New York
Bob,25,Los Angeles
Charlie,35,Chicago
```

## 実装

今回はプロジェクトを作らず、1ファイルで実行できるようにします。
以下のファイル（main.py）を作ります。

```python:main.py
import csv
import pathlib

import django
from django.conf import settings
from django.db import connection, models

db_file = "db.sqlite3"
settings.configure(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": db_file}},
    INSTALLED_APPS=["__main__"],
)
django.setup()


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)


if not pathlib.Path(db_file).exists():
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Person)
    with open("person.csv") as fp:
        for row in csv.DictReader(fp):
            Person.objects.create(**row)

for person in Person.objects.filter(age__gte=30):
    print("{0.name} {0.age} {0.city}".format(person))
```

## 実行

下記のように実行します。

```
python main.py
```

**実行結果**

```
Alice 30 New York
Charlie 35 Chicago
```

## 簡単な説明

### 設定

Djangoの設定はこれだけです。ほぼDB（SQLite）の指定だけです。

```python
# インポートは省略
db_file = "db.sqlite3"
settings.configure(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": db_file}},
    INSTALLED_APPS=["__main__"],
)
django.setup()
```

### モデル定義

CSVの内容に合わせてモデルを作ります。

```python
class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
```

### DBの作成

DBのファイルがなければ、テーブルを初期化してCSVデータを取り込みます。

```python
if not pathlib.Path(db_file).exists():
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Person)
    with open("person.csv") as fp:
        for row in csv.DictReader(fp):
            Person.objects.create(**row)
```

### ORMの処理

ここでは、サンプルとして`age >= 30`のデータを抽出して表示します。

```python
for person in Person.objects.filter(age__gte=30):
    print("{0.name} {0.age} {0.city}".format(person))
```

## まとめ

DjangoのDB操作だけする場合の最低限の処理を紹介しました。
実用性は、ないかもしれません。

以上

