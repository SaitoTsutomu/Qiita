title: FastAPI-MCPサーバーからツール情報を取得する方法
tags: Python MCP FastAPI FastAPI-MCP
url: https://qiita.com/SaitoTsutomu/items/abda9fe2c3c8aea9e5d8
created_at: 2025-09-13 21:53:45+09:00
updated_at: 2025-09-13 21:53:45+09:00
body:

## はじめに

この記事では、FastAPIで構築したサーバーを**MCP (Model Context Protocol) サーバー**化し、クライアントから**ツールの情報を取得**する具体的な手順を紹介します。

💡 **MCPとは？**
MCPは、生成AIモデルが外部のデータソースやツールと連携するための標準プロトコルです。これにより、AIモデルは文脈情報を効率的に管理し、その能力を拡張できます。いわば、AIと外部機能をつなぐための「共通言語」のようなものです。

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a74f9707-080b-4e2d-a05a-c2a062971c52.jpeg)

### ✅ 対象読者

* FastAPIを使ったことがあり、アプリケーションをMCPサーバー化したい方
* MCPクライアントがサーバーから情報を取得する具体的な通信フローを知りたい方

### ✅ 前提知識

* FastAPIの基礎的な知識
* MCPの基本的な概念に関する知識

---

## 🚀 MCPサーバーの構築

MCPサーバーは、`FastAPI-MCP`ライブラリを使って驚くほど簡単に構築できます。
既存のFastAPIアプリケーションに`FastApiMCP(app).mount_http()`の1行を追加するだけで、MCPサーバーとして機能させることが可能です。

🔗 **公式ドキュメント**

https://fastapi-mcp.tadata.com/

以下の内容で`server.py`を作成してください。

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

@app.get("/hello", operation_id="hello_get", status_code=201)
def hello(user: str) -> str:
    """挨拶を返す

    :param user: 相手
    :return: 挨拶
    """
    return f"Hi {user}!"

FastApiMCP(app).mount_http()
```

:::note info
**ワンポイントアドバイス**
`operation_id="hello_get"`を指定することで、MCPにおけるツール名が`hello_get`のように意図した名前になります。これを指定しない場合、FastAPIが自動生成する名前（この例では`hello_hello_get`）が使われます。デバッグや管理のしやすさから、[明示的に指定することをおすすめします](https://fastapi-mcp.tadata.com/configurations/tool-naming)。
:::

### サーバーの起動

ターミナルで以下のコマンドを実行し、MCPサーバーを起動します。

```
uv run --with fastapi-mcp uvicorn server:app
```

:::note info
**補足: `uv` と `uvicorn` について**

  * `uv`: Ruffプロジェクトが開発した、高速なPythonパッケージインストーラー兼仮想環境マネージャーです。
  * `uvicorn`: FastAPIなどのASGIアプリケーションを動作させるための、軽量で高速なサーバーです。
    このコマンドは「`uv`を使って`fastapi-mcp`を含む依存関係を解決し、`uvicorn`で`server.py`内の`app`を起動する」という意味になります。
:::

:::note warn
**ポートの競合に注意！**
デフォルトではポート`8000`を使用します。もし`address already in use`といったエラーが表示された場合は、他のプロセスがそのポートをすでに使用しています。
その際は、`--port 8100`のように空いているポート番号を指定してください。後述するクライアント側の`MCP_URL`も忘れずに変更しましょう。
:::

-----

## 🔧 クライアントからツール情報を取得する

サーバーからツール情報を取得するには、**JSON-RPC 2.0** というプロトコルに則って通信を行います。

💡 **JSON-RPC 2.0とは？**
軽量なリモートプロシージャコール（RPC）プロトコルの1つです。HTTPリクエストのボディにJSON形式で「どのメソッドを (`method`)」「どんな引数で (`params`)」呼び出したいかを記述して送信します。サーバーからの応答もJSONで返され、成功時には`result`、失敗時には`error`キーが含まれます。

情報の取得は、以下の3ステップの通信を順番に行うのが基本です。

1.  **セッションの初期化 (`initialize`)**
      * **目的:** クライアントとサーバー間で「握手」を交わし、通信を開始します。このリクエストにより、この後の一連の通信で使う**セッションID**が発行されます。
2.  **初期化完了の通知 (`notifications/initialized`)**
      * **目的:** クライアント側の準備が整ったことをサーバーに伝えます。これにより、サーバーはクライアントから次のリクエストを受け付ける準備ができたと認識します。
3.  **ツール一覧の取得 (`tools/list`)**
      * **目的:** サーバーが提供している利用可能なツールの一覧を問い合わせます。

以下の内容で`client.py`を作成してください。

```python
from pprint import pprint
import httpx

MCP_URL = "http://127.0.0.1:8000/mcp"

# 各リクエストのペイロードを定義
init_params = {
    "protocolVersion": "1.0",
    "capabilities": {},
    "clientInfo": {"name": "init client", "version": "1.0"},
}
headers = {"Accept": "application/json, text/event-stream"}
payload1 = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": init_params}
payload2 = {"jsonrpc": "2.0", "method": "notifications/initialized"}
payload3 = {"jsonrpc": "2.0", "id": 3, "method": "tools/list"}

with httpx.Client() as client:
    # 1. セッションIDの取得
    init_resp = client.post(MCP_URL, headers=headers, json=payload1)
    session_id = init_resp.headers.get("Mcp-Session-Id")
    print("セッションID:", session_id)
    pprint(init_resp.json())

    # セッションIDを付与したヘッダ
    headers_with_id = headers | {"Mcp-Session-Id": session_id}

    # 2. 完了通知
    client.post(MCP_URL, headers=headers_with_id, json=payload2)

    # 3. ツール一覧の取得
    tools_resp = client.post(MCP_URL, headers=headers_with_id, json=payload3)
    tools_json = tools_resp.json()

# 結果を見やすく整形して表示
# descriptionは長いため、変数に保持して別途表示する
description = tools_json["result"]["tools"][0]["description"]
tools_json["result"]["tools"][0]["description"] = "..."
pprint(tools_json)
print("DESCRIPTION")
print(description)
```

### プログラムの実行

サーバーを起動したまま、別のターミナルで以下のコマンドを実行します。

```
uv run --with httpx client.py
```

**実行結果の例**

````
セッションID: 01234567890123456789012345678901
{'id': 1,
 'jsonrpc': '2.0',
 'result': {'capabilities': {'experimental': {},
                             'tools': {'listChanged': False}},
            'protocolVersion': '2025-06-18',
            'serverInfo': {'name': 'FastAPI', 'version': '1.14.0'}}}
{'id': 3,
 'jsonrpc': '2.0',
 'result': {'tools': [{'description': '...',
                       'inputSchema': {'properties': {'user': {'title': 'user',
                                                               'type': 'string'}},
                                       'required': ['user'],
                                       'title': 'hello_getArguments',
                                       'type': 'object'},
                       'name': 'hello_get'}]}}
DESCRIPTION
Hello

挨拶を返す

:param user: 相手
:return: 挨拶

### Responses:

**201**: Successful Response (Success Response)
Content-Type: application/json

**Example Response:**
```json
"Response Hello Get"
```
````

実行結果から、FastAPIのエンドポイント（`hello`関数）の**docstring**が、ツールの`description`として正しく取得できていることが確認できます。これにより、クライアント（やAIモデル）はツールの機能や使い方を理解できます。

---

## 📚 補足情報

### HTTP Transport と SSE Transport

FastAPI-MCPには、MCPの通信方式（Transport）として`HTTP Transport`と`SSE (Server-Sent Events) Transport`の2種類が用意されています。

🔗 **詳細:**

https://fastapi-mcp.tadata.com/advanced/transport

今回はリクエストごとに応答が返ってくるシンプルな`HTTP Transport`（`mount_http()`）を使用しました。サーバーからのプッシュ通知など、より双方向な通信が必要な場合は`SSE Transport`（`mount_sse()`）を検討しますが、その場合クライアント側の情報の取得方法も異なるため注意が必要です。

### よくあるハマりポイント

* **セッションIDの付け忘れ**
    * `initialize`後の`notifications/initialized`や`tools/list`といったリクエストでは、**必ずHTTPヘッダーに取得したセッションID (`Mcp-Session-Id`) を含める**必要があります。忘れるとサーバー側でセッションを特定できずエラーになります。
* **ポートの競合**
    * 前述の通り、`uvicorn`起動時にポートが使用済みの場合があります。`--port`オプションで空いているポートを指定しましょう。
* **`Accept`ヘッダーの指定**
    * クライアントからリクエストを送る際、ヘッダーに`"Accept": "application/json, text/event-stream"`を指定しないと、サーバーが応答形式を決定できず`406 Not Acceptable`エラーが発生することがあります。

---

## 🎉 まとめ

本記事では、FastAPI-MCPを使ってMCPサーバーを構築し、クライアントからツール情報を取得するまでの一連の流れを解説しました。

* **サーバー構築は簡単:** `FastAPI-MCP`を使えば、既存のFastAPIアプリに1行追加するだけでMCPサーバー化できます。
* **通信プロトコル:** クライアントとの通信には、軽量な**JSON-RPC 2.0**プロトコルが使われます。
* **通信の順序が重要:** **`initialize` → `notifications/initialized` → `tools/list`** の順番でリクエストを送るのが基本フローです。

この手順を理解することで、生成AIと連携可能なカスタムツールを効率的に開発する第一歩となります。

