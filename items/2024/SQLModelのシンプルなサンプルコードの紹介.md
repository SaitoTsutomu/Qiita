title: SQLModelのシンプルなサンプルコードの紹介
tags: Python SQLite3 sqlalchemy FastAPI SQLModel
url: https://qiita.com/SaitoTsutomu/items/cf11f7b0b8b227d399d1
created_at: 2024-04-11 21:23:45+09:00
updated_at: 2024-07-28 00:16:29+09:00
body:

## 概要

[SQLModel](https://sqlmodel.tiangolo.com/)のWebAPIの**シンプルなサンプルコード**を紹介します。

コード一式は、下記にあります。すべてを確認するためには、[Download ZIP](https://github.com/SaitoTsutomu/sqlmodel-book-sample/archive/refs/heads/master.zip)からZIPをダウンロードしてください。

https://github.com/SaitoTsutomu/sqlmodel-book-sample

最初に、テーブルと機能を説明し、続いて、環境構築や実行方法を説明します。
最後に、ファイル構成と、抜粋したコードや補足の説明をします。

### 参考

- FastAPI版のサンプルコードの記事

https://qiita.com/SaitoTsutomu/items/6fd5cd835a4b904a5a3e

## テーブルとカラム

著者テーブルと書籍テーブルを操作します。データベースは、SQLiteを使います。

| テーブル         | カラム                                                              |
| :--------------- | :------------------------------------------------------------------ |
| 著者（`Author`） | ID（`id`）、名前（`name`）、書籍（`books`）                         |
| 書籍（`Book`）   | ID（`id`）、名前（`name`）、著者ID（`author_id`）、著者（`author`） |

- `Book.author_id`は、`Author.id`の外部キー
- `Author.books`と`Book.author`は、リレーション用

## 機能

2つの表を操作する12の機能があります。

| method | パスとパラメーター             | 関数               | 説明           |
| :----- | :----------------------------- | :----------------- | :------------- |
| POST   | `/authors?name=...`            | `add_author()`     | 著者の追加     |
| GET    | `/authors`                     | `get_authors()`    | 全著者の取得   |
| GET    | `/authors/<author_id>`         | `get_author()`     | 指定著者の取得 |
| GET    | `/authors/<author_id>/details` | `author_details()` | 指定著者の詳細 |
| PATCH  | `/authors?id=...`              | `update_author()`  | 指定著者の更新 |
| DELETE | `/authors?author_id=...`       | `delete_author()`  | 指定著者の削除 |
| POST   | `/books?book=...`              | `add_book()`       | 書籍の追加     |
| GET    | `/books`                       | `get_books()`      | 全書籍の取得   |
| GET    | `/books/<book_id>`             | `get_book()`       | 指定書籍の取得 |
| GET    | `/books/<book_id>/details`     | `book_details()`   | 指定書籍の詳細 |
| PATCH  | `/books?id=...`                | `update_book()`    | 指定書籍の更新 |
| DELETE | `/books?book_id=...`           | `delete_book()`    | 指定書籍の削除 |

- 著者と書籍が親子構造になっている
- 書籍を追加するには、親となる著者が必要
- 指定著者を削除すると、子供である書籍も削除される

## 環境構築

`Python 3.12`で動作します。[Poetry](https://python-poetry.org/)が必要です。
以下のようにしてFastAPIの仮想環境を作成します。

```shell
poetry install
```

## FastAPIの起動

以下のようにしてFastAPIを起動します。

```shell
poetry run uvicorn src.main:app --host 0.0.0.0 --reload
```

## 対話的APIドキュメント

下記から[対話的APIドキュメント](https://fastapi.tiangolo.com/ja/tutorial/first-steps/#api)（Swagger UI）が使えます。

- http://localhost:8000/docs

## REST APIのファイル構成

APIは`src`ディレクトリにあり、下記の3つのファイルからなります。

- `__init__.py`：パッケージ化するための空のファイル
- `main.py`：パスオペレーション関数を定義
- `models.py`：SQLModelのクラスなどを定義

### `main.py`（抜粋）

`main.py`では、主にパスオペレーション関数を定義しています。`Depends(get_db)`とすることで、`get_db`を差し替えられるようにしています。

```python:src/main.py
@app.get("/authors", tags=["/authors"])
async def get_authors(db: AsyncSession = Depends(get_db)) -> list[AuthorGet]:
    return list(map(AuthorGet.model_validate, await db.scalars(select(Author))))
```

### `models.py`（抜粋）

`models.py`は、SQLModelのクラスを定義しています。

```python:src/models.py
class Author(AuthorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list["Book"] = Relationship(
        back_populates="author", sa_relationship_kwargs={"cascade": "delete"}
    )
```

FastAPIでは、通常、「検証用のPydanticのクラス」と「ORM用のSQLAlchemyのクラス」が必要でした。しかし、SQLModelのモデルでは検証とORMでクラスを分ける必要がありません。
今回は、モデルのクラスを下記のように定義しています。AuthorとBookがDBのテーブルと対応します。

| クラス名           | 基底クラス | 目的             |
| :----------------- | :--------- | :--------------- |
| AuthorBase         | SQLModel   | id以外のデータ   |
| Author             | AuthorBase | idを含むデータ   |
| AuthorAdd          | AuthorBase | 追加時の引数用   |
| AuthorGet          | AuthorAdd  | 取得時の戻り値用 |
| AuthorGetWithBooks | AuthorGet  | 詳細時の戻り値用 |
| AuthorUpdate       | SQLModel   | 更新時の引数用   |
| BookBase           | SQLModel   | id以外のデータ   |
| Book               | BookBase   | idを含むデータ   |
| BookAdd            | BookBase   | 追加時の引数用   |
| BookGet            | BookAdd    | 取得時の戻り値用 |
| BookGetWithAuthor  | BookGet    | 詳細時の戻り値用 |
| BookUpdate         | SQLModel   | 更新時の引数用   |

SQLModelは、目的に応じたクラスを作ることで、シンプルな記述で安全に動作するようになっています。

## pytestの実行

下記のようにして、12の機能をテストします。

```shell
poetry run pytest
```

テストでは、別のDBを使うように、`get_db`を`get_test_db`で差し替えています。

```python:tests/conftest.py
@pytest_asyncio.fixture(autouse=True)
async def override_get_db(db):
    async def get_test_db():
        yield db

    app.dependency_overrides[get_db] = get_test_db
```

## リレーションのデータの取得について補足

SQLAlchemy ORMの`Book`クラスは、親の`Author`のリレーション（`author`）を持っています。

```python:src/models.py
class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author: Author | None = Relationship(back_populates="books")
```

`Book.author`の情報を取得するには、下記のように`options(selectinload(Book.author))`を使います。

```python:src/main.py
@app.get("/books/{book_id}/details", tags=["/books"])
async def book_details(book_id: int, db: AsyncSession = Depends(get_db)) -> BookGetWithAuthor:
    book = await db.scalar(
        select(Book).where(Book.id == book_id).options(selectinload(Book.author))
    )
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return BookGetWithAuthor.model_validate(book)

```

## Qiitaの記事

https://qiita.com/SaitoTsutomu/items/cf11f7b0b8b227d399d1

以上

