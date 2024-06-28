title: Litestarのシンプルなサンプルコードの紹介
tags: Python SQLite3 sqlalchemy REST-API litestar
url: https://qiita.com/SaitoTsutomu/items/db7605ff0869d82e828b
created_at: 2024-01-27 20:02:28+09:00
updated_at: 2024-01-27 20:02:28+09:00
body:

## 概要

Litestarの**シンプルなサンプルコード**を紹介します。

https://litestar.dev/

コード一式は、下記にあります。すべてを確認するためには、下記のZIPをダウンロードしてください。

https://github.com/SaitoTsutomu/litestar-book-sample/archive/refs/heads/master.zip

最初に、テーブルと機能を説明し、続いて、環境構築や実行方法を説明します。
最後に、ファイル構成と、抜粋したコードや補足の説明をします。

### 参考

- FastAPI版のサンプルコードの記事もあります。

https://qiita.com/SaitoTsutomu/items/6fd5cd835a4b904a5a3e

- 参考にしたチュートリアル

https://docs.litestar.dev/latest/tutorials/repository-tutorial/01-modeling-and-features.html

## テーブルとカラム

著者テーブルと書籍テーブルを操作します。データベースは、SQLiteを使います。

| テーブル         | カラム                                                              |
| :--------------- | :------------------------------------------------------------------ |
| 著者（`Author`） | ID（`id`）、名前（`name`）、書籍（`books`）                         |
| 書籍（`Book`）   | ID（`id`）、名前（`name`）、著者ID（`author_id`）、著者（`author`） |

- `Book.author_id`は、`Author.id`の外部キーです。
- `Author.books`と`Book.author`は、リレーション用です。

## 機能

2つの表を操作する10の機能があります。

| method | パスとパラメーター            | 関数              | 説明           |
| :----- | :---------------------------- | :---------------- | :------------- |
| POST   | `/authors?name=*`             | `add_author()`    | 著者の追加     |
| GET    | `/authors`                    | `get_authors()`   | 全著者の取得   |
| GET    | `/authors/<author_id>`        | `get_author()`    | 指定著者の取得 |
| PUT    | `/authors?author_id=*&name=*` | `update_author()` | 指定著者の更新 |
| DELETE | `/authors?author_id=*`        | `delete_author()` | 指定著者の削除 |
| POST   | `/books?title=*`              | `add_book()`      | 書籍の追加     |
| GET    | `/books`                      | `get_books()`     | 全書籍の取得   |
| GET    | `/books/<book_id>`            | `get_books()`     | 指定書籍の取得 |
| PUT    | `/books?book_id=*&title=*`    | `update_book()`   | 指定書籍の更新 |
| DELETE | `/books?book_id=*`            | `delete_book()`   | 指定書籍の削除 |

- 著者と書籍が親子構造になっています
- 書籍を追加するには、親となる著者が必要です
- 指定著者を削除すると、子供である書籍も削除されます

## 環境構築

`Python 3.11`で動作します。[Poetry](https://python-poetry.org/)が必要です。
以下のようにしてLitestarの仮想環境を作成します。

```shell
poetry install
```

## Litestarの起動

以下のようにしてLitestarを起動します。

```shell
poetry run litestar run --reload
```

## 対話的APIドキュメント

下記からSwagger UIが使えます。

- http://localhost:8000/schema/swagger/

## REST APIのファイル構成

シンプルなので、ソースファイルを1ファイル（`app.py`）にまとめています。。

## `app.py`の解説

ポイントごとに簡単に紹介します。なお、異常系の処理では処理不足の部分が残っています。

### plugins

`SQLAlchemyInitPlugin`を使うと、DBの初期化を設定できます。
また、`SQLAlchemySerializationPlugin`を使うと、DBのレコードからPydanticのオブジェクトにシリアライズ可能になります。このため、このサンプルではPydanticのクラス定義は不要になっています。

```python
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///db.sqlite3",
    session_config=AsyncSessionConfig(expire_on_commit=False),
)

app = Litestar(..., 
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config), SQLAlchemySerializationPlugin()],
)
```

Pydanticのクラスを定義する場合は、下記が参考になります。

https://docs.litestar.dev/2/tutorials/repository-tutorial/03-repository-controller.html

### on_startup

`on_startup`で、起動時の処理を指定できます。ここでは、テーブルを作成しています。

```python
async def on_startup() -> None:
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)

app = Litestar(on_startup=[on_startup], ...)
```

### DBのクラス定義

UUIDBaseから派生すると、`id`を主キーとして自動的に追加します。また、サンプルでは使用していませんが、UUIDAuditBaseから派生すると、`id`、`created_at`、`updated_at`を追加します。
なお、テーブル名はクラス名をスネークケースにしたものになります。

```python
class Author(UUIDBase):
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(...)
```

### パスオペレーション関数

SQLAlchemyInitPluginを使っているので、パスオペレーション関数の引数に、セッションとして`db_session`が使えます。
また、SQLAlchemySerializationPluginを使っているので、クエリ結果から自動的にPydanticのオブジェクトに変換されます。

```python
@get(path="/author", tags=["/authors"])
async def get_author(author_id: str, db_session: AsyncSession) -> Author | None:
    return await db_session.get(Author, author_id)
```

以上

