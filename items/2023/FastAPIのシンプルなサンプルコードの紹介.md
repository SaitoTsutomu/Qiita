title: FastAPIのシンプルなサンプルコードの紹介
tags: Python SQLite3 sqlalchemy REST-API FastAPI
url: https://qiita.com/SaitoTsutomu/items/6fd5cd835a4b904a5a3e
created_at: 2023-11-05 22:27:14+09:00
updated_at: 2023-12-01 07:01:05+09:00
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

- `Book.author_id`は、`Author.id`の外部キーです。
- `Author.books`と`Book.author`は、リレーション用です。

## 機能

2つの表を操作する11の機能があります。

| method | パスとパラメーター            | 関数              | 説明           |
| :----- | :---------------------------- | :---------------- | :------------- |
| POST   | `/authors?name=*`             | `add_author()`    | 著者の追加     |
| GET    | `/authors`                    | `get_authors()`   | 全著者の取得   |
| GET    | `/authors/<author_id>`        | `get_author()`    | 指定著者の取得 |
| PUT    | `/authors?author_id=*&name=*` | `update_author()` | 指定著者の更新 |
| DELETE | `/authors?author_id=*`        | `delete_author()` | 指定著者の削除 |
| POST   | `/books?name=*`               | `add_book()`      | 書籍の追加     |
| GET    | `/books`                      | `get_books()`     | 全書籍の取得   |
| GET    | `/books/<book_id>`            | `get_books()`     | 指定書籍の取得 |
| GET    | `/books/<book_id>/details`    | `book_details()`  | 指定書籍の情報 |
| PUT    | `/books?book_id=*&name=*`     | `update_book()`   | 指定書籍の更新 |
| DELETE | `/books?book_id=*`            | `delete_book()`   | 指定書籍の削除 |

- 著者と書籍が親子構造になっています
- 書籍を追加するには、親となる著者が必要です
- 指定著者を削除すると、子供である書籍も削除されます

## 環境構築

`Python 3.11`で動作します。[Poetry](https://python-poetry.org/)が必要です。
以下のようにしてFastAPIの仮想環境を作成します。

```shell
poetry install
```

## データベース初期化

以下のようにしてデータベースを初期化します。
ダミーの著者と書籍を追加しています。

```shell
poetry run python create_table.py
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

APIは`src`ディレクトリにあり、下記の5つのファイルからなります。

- `main.py`：FastAPIのインスタンス（app）を作成しています。
- `database.py`：[SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)のクラスとセッションを返す関数（get_db）を定義しています。
- `functions.py`：データベースを操作する11機能を定義しています。
- `schemas.py`：APIで扱うpydanticのクラスを定義しています。
- `routers.py`：パスオペレーション関数を定義しています。

### `main.py`（抜粋）

`main.py`は、FastAPIのインスタンス（app）を作成しています。
下記はその抜粋です（一部のimport文は省略しています）。

```python:src/main.py
from .routers import router

app = FastAPI()
app.include_router(router)
```

`routers.py`で定義したパスオペレーション関数を取り込むことで、`main.py`をシンプルにしています。

### `database.py`（抜粋）

`database.py`は、ORMのクラスを定義しています。SQLAlchemy2.0では、下記のように`DeclarativeBase`や`Mapped`、`mapped_column`を使います（[参考](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)）。`MappedAsDataclass`からの派生は省略できますが、派生するとdataclassのように使えて便利です。

```python:src/database.py
class Base(DeclarativeBase):
    pass

class Author(MappedAsDataclass, Base):
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
async def get_author(author_id: int, db: AsyncSession) -> Author | None:
    return await db.get(Author, author_id)
```

### `schemas.py`（抜粋）

`schemas.py`は、パスオペレーション関数で扱う、pydanticのクラスを定義しています。

```python:src/schemas.py
class Author(BaseModel):
    id: int
    name: str
    ...
```

`database.Author`のオブジェクトから`schemas.Author`のオブジェクトへの変換については、後述の「ORMクラスからpydanticクラスへの変換の補足」を参照してください。

### `routers.py`（抜粋）

`routers.py`では、パスオペレーション関数を定義しています。`Depends(get_db)`とすることで、`get_db`を差し替えられるようにしています。

```python:src/routers.py
@router.get("/authors/{author_id}", tags=["/authors"])
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)) -> Author:
    author = await functions.get_author(author_id, db)
    ...
```

## pytestの実行

下記のようにして、11の機能をテストします。

```shell
poetry run pytest
```

テストでは、別の`engine`を使うように、`get_db`を`get_test_db`で差し替えています。

```python:tests/conftest.py
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    ...
    async def get_test_db():
        async with AsyncSession(engine) as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db
```

## リレーションのデータの取得について補足

SQLAlchemy ORMの`Book`クラスは、親の`Author`のリレーション（`author`）を持っています。

```python:src/database.py
class Book(MappedAsDataclass, Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(32))
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Author] = relationship(Author)
```

`Book.author`の情報を取得するには、下記のように`options(selectinload(Book.author))`を使います。

```python:src/functions.py
async def book_details(book_id: int, db: AsyncSession) -> Book | None:
    return await db.scalar(
        select(Book).where(Book.id == book_id).options(selectinload(Book.author))
    )
```

## ORMクラスからpydanticクラスへの変換の補足

下記は、指定した著者を取得するパスオペレーション関数です。

```python:src/routers.py
@router.get("/authors/{author_id}", tags=["/authors"])
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)) -> Author:
    author = await functions.get_author(author_id, db)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return Author.model_validate(author)
```

上記の`Author.model_validate(author)`では、ORMクラス（`database.Author`）から、下記のpydanticのクラス（`schemas.Author`）に変換しています。下記の`model_config = ConfigDict(from_attributes=True)`を書くことで、この変換ができるようになります。

```python:src/schemas.py
class Author(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
```

以上

