title: just-agentsのMCPサーバー指定方法
tags: Python MCP just-agents
url: https://qiita.com/SaitoTsutomu/items/3f2290ac8ef7fd1a25bc
created_at: 2025-09-18 22:12:40+09:00
updated_at: 2025-09-18 22:21:53+09:00
body:

## はじめに

シンプルさに定評のある`just-agents`ですが、もちろんModel Context Protocol(MCP)サーバーを指定して外部ツールを利用することができます。
しかし、公式ドキュメントにはその方法についての明確な記述が見当たらないため、備忘録として簡単な指定方法を紹介します。

https://just-agents.readthedocs.io/

### 対象読者

  * `just-agents`でMCPサーバーを指定したい方

## 概要

`just-agents`では、エージェントが利用するツールを、エージェント作成時の引数`tools`で指定します。
MCPサーバーを利用する場合、この`tools`引数に**MCPコンフィグ**を渡します。

MCPコンフィグの実体は、MCPサーバーの設定情報を引数にして作成した`JustMCPServerParameters`クラスのインスタンスです。MCPサーバーの設定にはいくつかの形式がありますが、以下の例では最もシンプルなURL形式を用います。

## 実装例

本記事では、下記のQiita記事で紹介されているMCPサーバーを題材とします。

https://qiita.com/SaitoTsutomu/items/abda9fe2c3c8aea9e5d8

### 前提条件

  * `uv`がインストールされていること
  * Gemini APIキーを取得していること

後述のMCPクライアントの実行前に、対象のMCPサーバーを起動しておいてください。

### MCPクライアント (`client.py`)

以下の内容を`client.py`として保存します。

```python
from just_agents import llm_options
from just_agents.base_agent import BaseAgent
from just_agents.data_classes import JustMCPServerParameters

# MCPサーバーのURLを指定して、MCPコンフィグを作成
mcp_config = JustMCPServerParameters(
    mcp_client_config='http://localhost:8000/mcp',
)
# BaseAgentのtools引数にMCPコンフィグをリスト形式で渡す
agent = BaseAgent(
    llm_options=llm_options.GEMINI_2_5_FLASH,
    tools=[mcp_config],
)
# エージェントに利用可能なツールを尋ねる
print(agent.query("使えるツールの一覧"))
```

### 実行

`...`の部分を実際のGemini APIキーに置き換えて、以下のコマンドを実行してください。

```bash
GOOGLE_API_KEY=... uv run --with just-agents client.py
```

**実行結果**

```
利用可能なツールは以下の通りです。

* `hello_get(user: str)`: 挨拶を返します。`user`には相手の名前を指定します。
```

期待通り、MCPサーバー上で定義されているツールの一覧が取得できました。

MCPコンフィグ（`JustMCPServerParameters`）のいろいろな作成方法については、公式リポジトリのサンプルコードも参照してください。

https://github.com/longevity-genie/just-agents/blob/main/examples/just_agents/examples/basic/just_tools_example.py

## まとめ

本記事では、`just-agents`でMCPサーバーを利用する方法を解説しました。

`BaseAgent`の`tools`引数に`JustMCPServerParameters`を渡すだけで、サーバー上のツールが利用可能になります。

