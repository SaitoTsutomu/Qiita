title: Wiki.jsにSQLAlchemyで記事を作成してみた
tags: Python PostgreSQL sqlalchemy Docker Wiki.js
url: https://qiita.com/SaitoTsutomu/items/fec573224567a614930c
created_at: 2020-10-04 11:12:08+09:00
updated_at: 2020-10-04 11:12:08+09:00
body:

## やってみたこと

多機能な[Wiki.js](https://wiki.js.org/)ですが、既存データの一括インポート方法がわからなかったので、無理やりデータベースを更新できるかやってみました。正式な方法ではないので、自己責任でお試しください。

※ データベースは、いろいろ選べますが、PostgreSQLを選びました。

### 手順

- 準備
- docker-composeでWiki.jsの起動
- ローカルにSQLAlchemyの環境構築
- データベースからクラス作成
- SQLAlchemyで記事を作成

[GIGAZINEの記事](https://gigazine.net/news/20201003-wiki-js/)も参考にしてください。

## 準備

作業はmacOSのbashで確認しています。
docker-composeとPython3.8をインストールしておいてください。

## docker-composeでWiki.jsの起動

「[Wiki.js - Docs](https://docs.requarks.io/)」に起動方法がいろいろ書いてありますが、docker-composeを使います。
まずは、docker-compose.yamlを作成します。

```bash:bash
mkdir wikijs
cd wikijs
cat << EOF > docker-compose.yaml
version: "3"
services:

  db:
    image: postgres:11-alpine
    environment:
      POSTGRES_DB: wiki
      POSTGRES_PASSWORD: wikijsrocks
      POSTGRES_USER: wikijs
    ports:
      - "5432:5432"
    logging:
      driver: "none"
    restart: unless-stopped
    volumes:
      - db-data:/var/lib/postgresql/data

  wiki:
    image: requarks/wiki:2
    depends_on:
      - db
    environment:
      DB_TYPE: postgres
      DB_HOST: db
      DB_PORT: 5432
      DB_USER: wikijs
      DB_PASS: wikijsrocks
      DB_NAME: wiki
    restart: unless-stopped
    ports:
      - "80:3000"

volumes:
  db-data:
EOF
```

ローカル側のポート5432を変えた場合は、"5432:5432"を"15432:5432"のように変えて、以降の5432も変えてください。

### 起動＆ログイン

`docker-compose up -d`でWiki.jsが起動します。なお、停止は`docker-compose down`です。
`http://localhost/`でWiki.jsが利用できます。

ADMINISTRATOR ACCOUNTを適当に作成してください。そして作成したアカウントでログインしてください。

### トップページ作成

ログイン直後は何もページがありません。まずは、トップページを作成します。
トップページのパスは、`/<言語>/home`です。最初は、言語として英語（`en`）だけ使えます。

ここでは、言語として日本語（`ja`）を使うことにします。
まずは、英語のトップページを作成後、日本語の言語をインストールし、英語のトップページを削除して日本語のトップページを作成します。

「`+ CREATE HOME PAGE`」を押してください。
「Markdown」を押して、「`✓OK`」を押して、「`✓CREATE`」を押してください。

トップページ（`http://localhost/en/home`）が開きます。Administratorでログインしているので、右上の「`⚙`」で管理画面（`http://localhost/a/dashboard`）を開きます。

左側から「`Locale`」を選んでください。「`Download Locale`」から「Japanese」を選んで「雲に下矢印のマーク」の「Download」を押してください。そして、上に戻って「`Locale Settings`」を「Japanese」にし右上の「`✓ APPLY`」を押します。

アクティブな名前空間を日本語にしたので、トップページを日本語で作成し直しす必要があります。
左側から「`ページ`」を選んでください。Pathが「en/home」の項目を選び、「`ACTIONS v`」の「`Delete`」で削除します。

右上の「`閉じる`」で最初の画面に戻るので日本語のトップページを作成してください。

## ローカルにSQLAlchemyの環境構築

Wiki.jsではブラウザで記事を作成できますが、ここではPythonからデータベースを直接編集して記事の作成を試みます。
まずは、Pythonの仮想環境を作成します。

```bash:bash
python3.8 -m venv venv
source venv/bin/activate
pip install psycopg2-binary SQLAlchemy
```

## データベースからクラス作成

SQLAlchemyで使うクラスをデータベースから作成します。下記を実行すると`db_class.py`が作成されます。

```bash:bash
cat << EOF | python
import re

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql+psycopg2://wikijs:wikijsrocks@localhost:5432/wiki")

metadata = MetaData()
metadata.reflect(engine)

Base = declarative_base(metadata=metadata)


def _subfunc(m):
    s = ".".join(m.group(1).split(".")[-2:])
    return rf"ForeignKey('{s}')"


def make_class(cls):
    lst = [f"class {str(cls).split('.')[-1][:-2]}(Base):"]
    lst.append(f'    __tablename__ = "{cls.__tablename__}"\n')
    for column in cls.__table__.columns:
        s = repr(column)
        nam = s.split("'")[1]
        s = re.sub(r", table=[^>]+>", "", s)
        s = re.sub(r", server_default=[^)]+\)", "", s)
        s = re.sub(r"ForeignKey\('([^']+)'\)", _subfunc, s)
        lst.append(f"    {nam} = {s}")
    res = "\n".join(lst) + "\n"
    res = res.replace("metadata = Column", "metadata_ = Column")
    return res


def make_classes():
    lst = [
        """\
# made by make_classes
from typing import Any
from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import (
    BOOLEAN, BYTEA, INTEGER, JSON, TEXT, TIMESTAMP, VARCHAR
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # type: Any
"""
    ]
    dc = {"__table_args__": {"autoload": True}}
    for tbl in sorted(metadata.tables):
        if tbl in {"brute"}:
            continue
        typ = type(tbl.title(), (Base,), dict(__tablename__=tbl, **dc))
        lst.append(make_class(typ))
    with open("db_class.py", "w") as fp:
        fp.write("\n".join(lst))


make_classes()
EOF
```

## SQLAlchemyで記事を作成

まずは、ファイルを作成します。

```bash:bash
cat << EOF > main.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_class import *

engine = create_engine("postgresql+psycopg2://wikijs:wikijsrocks@localhost:5432/wiki")
Session = sessionmaker(bind=engine)
session = Session()
pgid = max(i.id for i in session.query(Pages).all()) + 1
ptid = max(i.id for i in session.query(Pagetree).all()) + 1
pg = Pages(
    id=pgid,
    path=f"test{pgid}",
    hash="0123456789001234567890abcdefghijklmnopqr",
    title=f"テストページ{pgid}",
    isPrivate=False,
    isPublished=True,
    content="",
    contentType="markdown",
    createdAt="2020-10-04T09:00:00.000Z",
    updatedAt="2020-10-04T09:00:00.000Z",
    editorKey="markdown",
    localeCode="ja",
    description="",
    authorId=1,
    creatorId=1,
    render="<div></div>",
    toc=[{"title": "", "anchor": "", "children": []}],
    extra={"js": "", "css": ""},
    publishStartDate="",
    publishEndDate="",
)
pt = Pagetree(
    id=ptid,
    path=pg.path,
    localeCode="ja",
    pageId=pgid,
    title=pg.title,
    depth=1,
    isPrivate=False,
    isFolder=False,
    ancestors=[],
)
session.add(pg)
session.add(pt)
session.commit()
session.close()
EOF
```

上記で、`main.py`を作成します。
`python main.py`で、`テストページ...`という空のページが作成されます。

内容は、`Pages.content`と`Pages.render`に記述します。contentに記述しただけだと表示されませんが、編集して保存すると表示されます。

### バックアップ

`pg_dump -h localhost -p 5432 -U wikijs wiki -f data.sql`でデータベースの内容をダンプできます。

`psql -h ホスト -p 5432 -U ユーザ データベース -f data.sql`で空のPostgreSQLにデータを戻せます。

