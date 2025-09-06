title: uvとtaskipyを使った環境変数の管理
tags: Python UV 環境変数 taskipy
url: https://qiita.com/SaitoTsutomu/items/ff10a21ab9a6bacce5d2
created_at: 2025-07-29 18:05:09+09:00
updated_at: 2025-08-04 09:12:29+09:00
body:

## はじめに

AIを使ったアプリケーション開発で、APIキーを環境変数に保存することを考えます。

環境変数を特定のプロジェクトのみ有効にする方法として、`dotenv`や`direnv`、`autoenv`などがあります。

この記事では、`uv`と`taskipy`で環境変数を設定する方法を紹介します。

※ `taskipy`は、`pyproject.toml`で管理するタスクランナーです。

https://github.com/taskipy/taskipy

## 前提

* `uv`がインストールされている
* `taskipy`がインストールされている
* プロジェクトを`pyproject.toml`で管理する
* アプリケーションは、`uv run`で動かす

`taskipy`は、`uv tool install taskipy`でインストールできます。

## 構築手順

それでは、実際にプロジェクトを構築していきましょう。

### 1. ファイルの準備

まず、環境変数を定義する`.env`ファイルと、それを読み込む`main.py`ファイルを作成します。

```text:.env
API_KEY="your_secret_api_key_here"
```

```python:main.py
import os

api_key = os.getenv("API_KEY")

if api_key:
    # 成功！キーの一部を隠して表示
    print(f"✅ API Key loaded successfully: {api_key[:11]}...")
else:
    # 失敗
    print("❌ Error: API_KEY not found.")
```

### 2. タスクの設定
次に、`pyproject.toml`に`taskipy`のタスクを定義します。これにより、`.env`ファイルを読み込むコマンドを簡単に実行できるようになります。

コード スニペット

```toml:pyproject.toml
[project]
name = "my-uv-project"
requires-python = ">=3.11"
version = "0.1.0"

# 以下を追加する
[tool.taskipy.tasks]
run = "uv run --env-file .env"
```

### しくみの説明

`pyproject.toml`に下記を追加すると、`task new_command`とすることで右辺のコマンドを実行できます。また、`task new_command`の後ろに付けた引数は、定義したコマンドの末尾にそのまま追加されます。

```toml
[tool.taskipy.tasks]
new_command = (コマンド)
```

このことから、「プロジェクトの設定」の記述により、`task run main.py`とすると`uv run --env-file .env main.py`を実行します。
この`--env-file .env`を付けることで、ファイル`.env`の環境変数を反映してコードを実行できます。

## 実行と確認

すべてのファイルが準備できたら、以下のコマンドを実行します。

**コマンド**

```shell
task run main.py
```

**実行結果**

```
✅ API Key loaded successfully: your_secret...
```

このように表示されれば、`main.py`が`.env`ファイルから環境変数を正しく読み込めたことになります。

## おわりに

ポイントは「`uv run --env-file .env`を使えば、`.env`ファイルで環境変数を簡単に管理できる」ということです。

このコマンドを毎回入力するのは手間ですが、`taskipy`を使うことで`task run`のように短いコマンドで実行でき、管理も楽になります。

また、`alias`を使う方法もありますが、`alias`は個人のPCのシェル設定に依存するため、チームメンバーとの共有が困難です。一方、`taskipy`の設定は`pyproject.toml`に記述されるため、**Gitで管理でき、チーム全体で同じ開発体験を簡単に共有できる**という大きなメリットがあります。

以上

