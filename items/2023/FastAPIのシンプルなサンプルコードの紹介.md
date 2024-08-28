title: FastAPIのシンプルなサンプルコードの紹介
tags: Python SQLite3 sqlalchemy REST-API FastAPI
url: https://qiita.com/SaitoTsutomu/items/6fd5cd835a4b904a5a3e
created_at: 2023-11-05 22:27:14+09:00
updated_at: 2024-07-28 23:26:24+09:00
body:

## 概要

[FastAPI](https://fastapi.tiangolo.com/ja/)の**シンプルなサンプルコード**を紹介します。

コード一式は、下記にあります。すべてを確認するためには、[Download ZIP](https://github.com/SaitoTsutomu/fastapi-book-sample/archive/refs/heads/master.zip)からZIPをダウンロードしてください。

https://github.com/SaitoTsutomu/fastapi-book-sample

最初に、テーブルと機能を説明し、続いて、環境構築や実行方法を説明します。
最後に、ファイル構成と、抜粋したコードや補足の説明をします。

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

著者が空の時にダミーの著者と書籍を追加しています。

## 対話的APIドキュメント

下記から[対話的APIドキュメント](https://fastapi.tiangolo.com/ja/tutorial/first-steps/#api)（Swagger UI）が使えます。

- http://localhost:8000/docs

## REST APIのファイル構成

APIは`src`ディレクトリにあり、下記の5つのファイルからなります。

- `main.py`：FastAPIのインスタンス（app）を作成
- `database.py`：[SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)のクラスとセッションを返す関数（get_db）を定義
- `functions.py`：データベースを操作する12機能を定義
- `schemas.py`：APIで扱うpydanticのクラスを定義
- `routers.py`：パスオペレーション関数を定義

### `main.py`（抜粋）

`main.py`は、FastAPIのインスタンス（app）を作成しています。
下記はその抜粋です（一部のimport文は省略しています）。

```python:src/main.py
from .routers import router

app = FastAPI(lifespan=lifespan)
app.include_router(router)
```

`routers.py`で定義したパスオペレーション関数を取り込むことで、`main.py`をシンプルにしています。

### `database.py`（抜粋）

`database.py`は、ORMのクラスを定義しています。SQLAlchemy2.0では、下記のように`DeclarativeBase`や`Mapped`、`mapped_column`を使います（[参考](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)）。`MappedAsDataclass`からの派生は省略できますが、派生するとdataclassのように使えて便利です。

```python:src/database.py
class Base(sqlalchemy.orm.DeclarativeBase):
    pass

class Author(sqlalchemy.orm.MappedAsDataclass, Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(16))
    ...
```

また、下記のようにAsyncSessionを返すジェネレーター`get_db`を定義しています。`get_db`は、パスオペレーション関数で使います。

```python:src/database.py
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(engine) as session:
        yield session
```

### `functions.py`（抜粋）

`functions.py`は、データベースを操作する関数を定義しています。
下記は、authorテーブルから主キーでレコードを取得する関数です。

```python:src/functions.py
async def get_author(db: AsyncSession, *, author_id: int) -> Author | None:
    return await db.get(Author, author_id)
```

### `schemas.py`（抜粋）

`schemas.py`は、パスオペレーション関数で扱う、pydanticのクラスを定義しています。

```python:src/schemas.py
class BaseModel(BaseModel_):
    model_config = ConfigDict(from_attributes=True)

class AuthorBase(BaseModel):
    name: str

class Author(AuthorBase):
    id: int | None = None
```

今回は、pydanticのクラスを下記のように定義しています。

| クラス名           | 基底クラス | 目的             |
| :----------------- | :--------- | :--------------- |
| AuthorBase         | BaseModel  | id以外のデータ   |
| Author             | AuthorBase | idを含むデータ   |
| AuthorAdd          | AuthorBase | 追加時の引数用   |
| AuthorGet          | AuthorAdd  | 取得時の戻り値用 |
| AuthorGetWithBooks | AuthorGet  | 詳細時の戻り値用 |
| AuthorUpdate       | BaseModel  | 更新時の引数用   |
| BookBase           | BaseModel  | id以外のデータ   |
| Book               | BookBase   | idを含むデータ   |
| BookAdd            | BookBase   | 追加時の引数用   |
| BookGet            | BookAdd    | 取得時の戻り値用 |
| BookGetWithAuthor  | BookGet    | 詳細時の戻り値用 |
| BookUpdate         | BaseModel  | 更新時の引数用   |

このように目的に応じたクラスを作ることで、シンプルな記述で安全に動作するようになっています。

### `routers.py`（抜粋）

`routers.py`では、パスオペレーション関数を定義しています。`Depends(get_db)`とすることで、`get_db`を差し替えられるようにしています。

```python:src/routers.py
@router.get("/authors/{author_id}", response_model=AuthorGet, tags=["/authors"])
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    author = await functions.get_author(db, author_id=author_id)
    ...
    return author
```

戻り値の型は、`response_model`で指定します。`AuthorGet`を指定することで、`database.Author`型の`author`が、`AuthorGet.model_validate()`で変換されて検証されます。

下記の`model_config = ConfigDict(from_attributes=True)`を書くことで、この変換ができるようになります。

```python:src/schemas.py
class BaseModel(BaseModel_):
    model_config = ConfigDict(from_attributes=True)
```

次のように書いても同じく変換されますが、mypyで型違いと判定されます。

```python:src/routers.py
@router.get("/authors/{author_id}", tags=["/authors"])
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)) -> AuthorGet:
    author = await functions.get_author(db, author_id=author_id)
    ...
    return author
```

## pytestの実行

下記のようにして、12の機能をテストします。

```shell
poetry run pytest
```

テストでは、別の`engine`を使うように、`get_db`を`get_test_db`で差し替えています。

```python:tests/conftest.py
@pytest_asyncio.fixture(autouse=True)
async def override_get_db(db):
    async def get_test_db():
        yield db

    app.dependency_overrides[get_db] = get_test_db
```

## リレーションのデータの取得について補足

SQLAlchemy ORMの`Book`クラスは、親の`Author`のリレーション（`author`）を持っています。

```python:src/database.py
class Book(sqlalchemy.orm.MappedAsDataclass, Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(32))
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Author] = relationship(Author)
```

`Book.author`の情報を取得するには、下記のように`options(selectinload(Book.author))`を使います。

```python:src/functions.py
async def book_details(db: AsyncSession, *, book_id: int) -> Book | None:
    return await db.scalar(
        select(Book).where(Book.id == book_id).options(selectinload(Book.author))
    )
```

## Qiitaの記事

https://qiita.com/SaitoTsutomu/items/6fd5cd835a4b904a5a3e

以上

