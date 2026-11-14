title: NiceGUIのフィクスチャを使ったGUIのテスト方法
tags: Python Webアプリケーション pytest nicegui
url: https://qiita.com/SaitoTsutomu/items/9800bfe7d2b31b9f2c59
created_at: 2025-03-04 23:06:05+09:00
updated_at: 2025-03-04 23:09:55+09:00
body:

## 概要

NiceGUIベースの書籍管理システムを通して、pytestによるGUIのテスト方法を紹介します。

**紹介すること**

* `user`フィクスチャによる軽量テスト
* `screen`フィクスチャによるブラウザベースのテスト

**実行に必要なもの**

* uv
* Python 3.12以上

https://docs.astral.sh/uv/

## NiceGUIについて

NiceGUIは、PythonでWebアプリケーションやWebAPIを作成するためのフレームワークです。

https://nicegui.io/

## 書籍管理システムについて

書籍管理システムは、著者の追加・削除、書籍の追加・削除ができるシステムです。
実行するには、次のリポジトリを`git clone`してください。

https://github.com/SaitoTsutomu/nicegui-pytest

`git clone`後に、次のようにして実行できます。

```
uv run book-list
```

著者リストと書籍リストの2つのページがあります。

![](https://raw.githubusercontent.com/SaitoTsutomu/nicegui-pytest/refs/heads/master/images/main.jpg)

## pytestについて

pytestは、Pythonで人気のテストフレームワークです。

https://pytest.org/

紹介するリポジトリのテストは次のようにして実行します。

```
uv run pytest
```

次の6つをテストします。

* `user`フィクスチャを使ったテスト
  * `test_label`: 表示項目のテスト
  * `test_add_author`: 著者追加のテスト
  * `test_show_book`: 書籍表示のテスト
* `screen`フィクスチャを使ったテスト
  * `test_label`: 表示項目のテスト
  * `test_add_author`: 著者追加のテスト
  * `test_show_book`: 書籍表示のテスト

### `user`フィクスチャと`screen`フィクスチャについて

`user`フィクスチャと`screen`フィクスチャは、NiceGUIで用意されているGUIのテスト用のフィクスチャです。
GUIのテストをシンプルに記述できます。

`screen`フィクスチャを使ったテスト関数を実行すると関数終了時の画面のスナップショットが自動で`screenshots`フォルダーに保存されます。

https://nicegui.io/documentation/section_testing

## テストに必要なもの

**パッケージ**

* `pytest`: テストフレームワーク
* `pytest-asyncio`: pytestの非同期用
* `pytest-selenium`: pytestのヘッドレスブラウザ用

**ファイル**

* `conftest.py`: `pytest_plugins`を指定する
* `src/tests/__init__.py`: 空ファイル
* `src/tests/conftest.py`: フィクスチャなどの作成
* `src/tests/test_views.py`: テストコードの記述

### `conftest.py`

`user`フィクスチャと`screen`フィクスチャを使用するには、次の記述が必要です。

```python
pytest_plugins = ["nicegui.testing.plugin"]
```

`pytest_plugins`は、ルートの`conftest.py`に書く必要があります。

### `src/tests/conftest.py`

**テスト用DBのフィクスチャ**

DBは`sqlite3`です。テストではインメモリで使います。
ORMは`tortoise-orm`を使います。

https://tortoise.github.io/

次のフィクスチャを用意することで、テストの関数ごとに空のDBを利用できます。

```python
@pytest.fixture(autouse=True)
def db() -> Iterable[None]:
    """DBの開始と終了"""
    asyncio.run(Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["nicegui_book_list.models"]}))
    asyncio.run(Tortoise.generate_schemas())
    yield
    asyncio.run(Tortoise.close_connections())
```

**`user`フィクスチャと`screen`フィクスチャ**

テストの関数で`user`フィクスチャを使えますが、ここでは次のようにページの登録（ルーティング）もしています。`screen`フィクスチャも同様です。

```python
@pytest.fixture
def user(user: User) -> User:
    """ページを登録してuserフィクスチャを返す"""
    importlib.reload(nicegui_pytest.views)
    return user
```

## テストの実装

次は、`user`フィクスチャの使用例です。`user`フィクスチャは軽量に動作します。

* `user.open("/")`で、トップページを開く
* `user.should_see()`で、画面の内容を検証する

```python
async def test_label(user: User) -> None:
    """表示項目のテスト"""
    await user.open("/")  # 著者リストのページを開く

    # 画面に「書籍管理システム」が表示されていることの確認
    await user.should_see("書籍管理システム")
```

次は、`screen`フィクスチャの使用例です。`screen`フィクスチャは、ブラウザを操作するので少し重いです。

* `screen.open("/")`で、トップページを開く
* `screen.should_contain()`で、画面の内容を検証する

```python
def test_label(screen: Screen) -> None:
    """表示項目のテスト"""
    screen.open("/")
    # 画面に「書籍管理システム」が表示されていることの確認
    screen.should_contain("書籍管理システム")
```

より詳しいテストの書き方については、次も参考にしてください。

https://github.com/zauberzeug/nicegui/tree/main/examples/pytests/

https://qiita.com/SaitoTsutomu/items/9800bfe7d2b31b9f2c59

以上

