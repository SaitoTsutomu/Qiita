title: FastAPI と Tortoise ORMで作る、シンプルなCRUD APIハンズオン
tags: Python ハンズオン FastAPI tortoise-orm Polars
url: https://qiita.com/SaitoTsutomu/items/9572da099c632f249d4f
created_at: 2025-08-27 00:06:32+09:00
updated_at: 2025-08-27 05:31:29+09:00
body:

## はじめに

本記事では、モダンなPythonのWebフレームワーク **FastAPI** と、非同期処理に対応したORM（Object-Relational Mapper）である **Tortoise ORM** を組み合わせた、シンプルなAPI開発のハンズオンを紹介します。

このハンズオンを通じて、データベースと連携する基本的なCRUD（作成・読み取り・更新・削除）APIを効率的に実装する方法を学びます。

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9182a70e-27ca-41bd-97b0-b453d03bc290.jpeg)

- **OS**: macOSを想定していますが、LinuxやWindows (WSL2) でも同様の手順で進められます。
- **データベース**: Docker上でPostgreSQLを起動して使用します。
- **ORM**: Tortoise ORMを利用して、Pythonのコードで直感的にデータベースを操作します。
- **動作確認**: APIの動作確認はSwagger UIで行い、データの操作や分析の例としてJupyterとPolarsを利用します。

## 対象読者

- FastAPIを使ったデータベース連携アプリケーションの実装方法を学びたい方
- ORMを使って、シンプルかつ効率的にCRUD APIを開発したい方
- FastAPIとデータ分析ツール（Polars）の連携に興味がある方

## 前提条件

以下のツールがインストールされ、利用できる状態であることを前提とします。

- Docker
- uv

また、Jupyterとターミナル操作の基本的な知識が必要です。

---

## 1. 環境構築

まずは、プロジェクトのディレクトリを作成し、必要なパッケージをインストールします。

### プロジェクト作成

ターミナルを開き、以下のコマンドを実行してプロジェクト用のディレクトリを作成し、そこに移動します。

```bash
uv init my_fastapi_proj
cd my_fastapi_proj
```

### パッケージの追加

APIサーバーの実行に必要なパッケージと、開発・データ確認に使うパッケージをそれぞれインストールします。

```bash
# APIサーバーに必要なパッケージを追加します
# - fastapi[all]: FastAPI本体と、サーバー実行(uvicorn)など必要なものが全て含まれます
# - tortoise-orm: 非同期対応のORM
# - asyncpg: PostgreSQLと非同期で通信するためのドライバ
uv add "fastapi[all]==0.116.1" tortoise-orm==0.25.1 asyncpg==0.30.0

# 開発時に使用するパッケージを--devフラグ付きで追加します
# - jupyter: インタラクティブなデータ操作に使用します
# - polars: 高速なデータフレーム操作ライブラリ
uv add --dev jupyter==1.1.1 polars==1.32.3
```

### PostgreSQLの起動

Dockerを使って、APIが接続するPostgreSQLデータベースを起動します。

```bash
docker run -it --rm \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -v fastapi-data:/var/lib/postgresql/data \
  postgres
```

**【重要】**
このコマンドはターミナルのフォアグラウンドで実行され、ログが出続けます。**以降の作業は、別の新しいターミナルウィンドウ（またはタブ）を開いて行ってください。**

-----

## 2. APIの実装と起動

次に、APIのメインロジックを記述し、サーバーを起動します。

### `main.py` の更新

`main.py`に次のように置き換えてください。

```python
from fastapi import FastAPI, HTTPException
from tortoise import Tortoise, fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

# --- FastAPIアプリケーションの初期化 ---
app = FastAPI()


# --- Tortoise-ORM モデル定義 ---
class User(Model):
    """データベースのユーザーテーブルを表すモデル"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)


# --- Pydantic スキーマ定義 ---
# TortoiseモデルからPydanticモデルを自動生成
User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)


# --- APIエンドポイント ---
@app.post("/users", response_model=User_Pydantic, status_code=201)
async def create_user(user: UserIn_Pydantic):
    """新しいユーザーの作成"""
    user_obj = await User.create(**user.model_dump(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get("/users", response_model=list[User_Pydantic])
async def get_users():
    """すべてのユーザーの取得"""
    return await User_Pydantic.from_queryset(User.all())


@app.get("/users/{user_id}", response_model=User_Pydantic)
async def get_user(user_id: int):
    """指定されたIDのユーザーの取得"""
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return await User_Pydantic.from_tortoise_orm(user)


@app.put("/users/{user_id}", response_model=User_Pydantic)
async def update_user(user_id: int, user: UserIn_Pydantic):
    """指定されたIDのユーザー情報の更新"""
    await User.filter(id=user_id).update(**user.model_dump(exclude_unset=True))
    updated_user = await User.get_or_none(id=user_id)
    if updated_user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return await User_Pydantic.from_tortoise_orm(updated_user)


@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    """指定されたIDのユーザーの削除"""
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return {"message": f"User {user_id} deleted successfully"}


# --- Tortoise-ORMのDB設定 ---
db_url = "postgres://postgres:password@localhost:5432/postgres"
db_args = {"db_url": db_url, "modules": {"models": ["main"]}}


async def init_db() -> None:
    """Jupyter用のDB設定"""
    await Tortoise.init(**db_args)
    await Tortoise.generate_schemas()


# FastAPI用のDB設定
register_tortoise(app, **db_args, generate_schemas=True, add_exception_handlers=True)
```

### FastAPIの起動

以下のコマンドで、FastAPIアプリケーションサーバーを起動します。`dev`をつけることで、コードの変更を検知して自動でリロードする開発モードになります。

```bash
uv run fastapi dev main.py
```

サーバーが起動したら、**さらに別のターミナルを開いて**、次の動作確認に進みます。

-----

## 3. 動作確認

APIが正しく動作するか、いくつかの方法で確認しましょう。

### Swagger UIでの確認

Webブラウザで以下のURLにアクセスすると、自動生成されたAPIドキュメント（Swagger UI）が表示されます。

  - `http://localhost:8000/docs`

1.  `GET /users` のエンドポイントをクリックして開きます。
2.  `Try it out` ボタンをクリックします。
3.  `Execute` ボタンをクリックします。

初めはデータベースにユーザーがいないため、レスポンスボディには空のリスト `[]` が表示されるはずです。

### Jupyterでのインタラクティブな操作

次に、Jupyterを使ってより対話的にデータベースを操作してみます。

#### 起動

（FastAPIサーバーとは別の）新しいターミナルで、以下のコマンドを実行してJupyter Labを起動します。

```bash
uv run jupyter lab
```

ブラウザでJupyter Labが開いたら、新しいノートブックを作成し、以下のセルを順番に実行していきましょう。

#### データベース接続の初期化

`main.py`で定義したモデルをインポートし、データベースへの接続を確立します。

```python
import polars as pl
from main import User, init_db

# データベースに接続し、テーブルを作成します
await init_db()
```

*注意: トップレベルでの`await`は、Jupyter NotebookやIPythonの最近のバージョンでサポートされている機能です。*

#### Userモデルの確認

まずはユーザーが存在しないことを確認します。

```python
await User.all()
```

**実行結果:** `[]`

#### Userの作成

新しいユーザーを2件作成し、再度全件取得して確認します。

```python
await User.create(id=1, name="Alice")
await User.create(id=2, name="Bob")

await User.all()
```

**実行結果:** `[<User: 1>, <User: 2>]`

この時点で、先ほどの **Swagger UI** (`http://localhost:8000/docs`) に戻って `GET /users` を再度実行すると、2件のユーザーがJSON形式で返ってくることを確認できます。

#### Userの取得と更新

IDを指定して特定のユーザーを取得し、名前を更新します。

```python
# ID=1のユーザーを取得
user = await User.get(id=1)
print(user.name)

# 名前を更新して保存
user.name = "Carol"
await user.save()
```

**実行結果:** `Alice`

更新がAPIに反映されているか、`curl`コマンドで確認してみましょう。（Jupyter Notebook内から`!`を付けてシェルコマンドを実行できます）

```bash
!curl http://127.0.0.1:8000/users/1
```

**実行結果:** `{"id":1,"name":"Carol","is_active":true,"created_at":"..."}`

#### DataFrameへの変換

`Polars`を使い、データベースから取得した全ユーザーをデータフレームに変換します。これはデータ分析などを行う際の一般的な入り口となります。

```python
# .values()でモデルオブジェクトのリストを辞書のリストに変換します
users_data = await User.all().values()
df = pl.DataFrame(users_data)
df
```

#### DataFrameからデータベースへの登録

逆に、データフレームの内容をデータベースに一括で登録することも可能です。

```python
# まず、既存のレコードを全て削除します
await User.all().delete()

# データフレームの各行をUserオブジェクトに変換し、bulk_createで一括登録します
await User.bulk_create(User(**row) for row in df.to_dicts())

# 登録結果を確認します
await User.all()
```

**実行結果:** `[<User: 2>, <User: 1>]`

-----

## 4. 後片付け

ハンズオンが終わったら、起動したサーバーとデータベースを停止し、作成したリソースを削除してクリーンな状態に戻しましょう。

1.  **FastAPIサーバーの停止**:
    `uv run fastapi ...` を実行したターミナルで `Ctrl + C` を押します。

2.  **Jupyterの停止**:
    `uv run jupyter ...` を実行したターミナルで `Ctrl + C` を押し、確認メッセージに `y` で答えます。

3.  **Dockerコンテナの停止**:
    `docker run ...` を実行したターミナルで `Ctrl + C` を押します。（`--rm`オプションを付けて起動したため、コンテナは自動的に削除されます。）

4.  **Dockerボリュームの削除**:
    データベースのデータを保存していたボリュームを、以下のコマンドで削除します。

    ```bash
    docker volume rm fastapi-data
    ```

これで、ハンズオン開始前の状態に戻りました。

-----

## まとめ

このハンズオンでは、以下の内容を実践しました。

  - `uv`を使ったPythonプロジェクトの初期化とパッケージ管理
  - DockerによるPostgreSQLデータベースの準備
  - `Tortoise ORM`を使ったデータベースモデルの定義とテーブル操作
  - `FastAPI`による基本的なCRUD API（作成・取得・更新・削除）の実装
  - Swagger UIを使ったAPIの動作確認
  - JupyterとPolarsを連携させた、インタラクティブなデータ操作とDataFrameへの変換

