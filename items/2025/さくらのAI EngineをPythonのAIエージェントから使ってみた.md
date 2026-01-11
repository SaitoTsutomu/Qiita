title: さくらのAI EngineをPythonのAIエージェントから使ってみた
tags: Pyhton さくらのクラウド AI MCP just-agents
url: https://qiita.com/SaitoTsutomu/items/5c3b9058b02a6f02dec5
created_at: 2025-09-26 07:50:49+09:00
updated_at: 2025-09-26 07:50:49+09:00
body:

## はじめに

さくらインターネットから新しい生成AIサービス「**さくらのAI Engine**」がリリースされました。

https://www.sakura.ad.jp/corporate/information/newsreleases/2025/09/24/1968221046/

この記事では、この「さくらのAI Engine」を**PythonでAIエージェントから利用する方法**を、実践的なコード例とともにわかりやすく解説します。

---

### 🎯 対象読者

- PythonでAIエージェントを使ったことがある方
- 「さくらのAI Engine」をAIエージェントから利用してみたい方
- `LiteLLM` や `just-agents` に興味がある、あるいはこれから使ってみたい方

---

### 💡 「さくらのAI Engine」とは？

「さくらのAI Engine」は、さくらインターネットの生成AI向けクラウド基盤「高火力」をベースとした、**API経由で簡単に利用できるAIサービス**です。  
国内外の複数のLLM（大規模言語モデル）やRAG（検索拡張生成）機能が提供されています。

本記事では、チャット形式で対話が可能な「**Chat completions**」機能を利用します。とくに `Qwen3-Coder-480B-A35B-Instruct-FP8` のような高性能モデルを使える点が魅力です。

| サービス類型            | 基盤モデル                           |
| :---------------------- | :----------------------------------- |
| **Chat completions**    | `gpt-oss-120b`                       |
|                         | `llm-jp-3.1-8x13b-instruct4`         |
|                         | `Qwen3-Coder-30B-A3B-Instruct`       |
|                         | `Qwen3-Coder-480B-A35B-Instruct-FP8` |
| **Audio Transcription** | `whisper-large-v3-turbo`             |
| **Embeddings**          | `multilingual-e5-large`              |
| **ドキュメント（RAG）** | ―                                    |

利用プランは「**基盤モデル無償プラン**」と「従量課金プラン」の2種類。今回は手軽に試せる「基盤モデル無償プラン」に申し込みました。

申し込み手順は以下の公式サイトをご覧ください。

https://www.sakura.ad.jp/aipf/ai-engine/

---

## 🔑 Step 1: アカウントトークンの作成

APIを利用するには、まず**アカウントトークンの作成**が必要です。  
以下の管理画面から最大20個まで作成できます。

https://secure.sakura.ad.jp/ai/account-tokens

---

## 💻 Step 2: PythonからAPIを呼び出す

**公式ドキュメント**  

https://manual.sakura.ad.jp/cloud/ai-engine/03-operation-guide.html#id6  

https://manual.sakura.ad.jp/api/cloud/ai-engine/inference.html

ドキュメントのChat completionsのところはシンプルすぎてちょっとわかりにくいです。

### 1. `requests` を使った基本的な呼び出し

まずは標準ライブラリ `requests` を使って、直接APIを叩いてみましょう。

※ `just-agents`をインストールしておきます。

```python
import requests

token = "＜ここに作成したトークンを入力＞"
api_base = "https://api.ai.sakura.ad.jp/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
}
model = "gpt-oss-120b"  # モデル
query = "hello"  # LLMに送る内容
messages = [{"role": "user", "content": query}]
data = {"model": model, "messages": messages}

response = requests.post(api_base, headers=headers, json=data)
print(response.json()["choices"][0]["message"]["content"])
````

**実行結果**

```
Hello! How can I help you today?
```

無事にレスポンスが返ってきました！

### 2. `LiteLLM` を使った呼び出し

次に、複数のLLMを統一的なインターフェイスで扱えるライブラリ `LiteLLM` を使ってみましょう。

https://docs.litellm.ai/docs/

以下のように設定すれば、`LiteLLM` からも問題なく呼び出せます：

```python
import litellm

llm_options = {
    "model": model,
    "api_base": api_base,
    "api_key": token,
    "custom_llm_provider": "deepseek",  # ← これがポイント
}

response = litellm.completion(**llm_options, messages=messages)
print(response.choices[0].message.content)
```

ここでの重要なポイントは、`custom_llm_provider` に `"deepseek"` を指定することです。これにより、`LiteLLM`がほぼ素のAPIとして解釈し動作します。

### 3. `just-agents` を使った呼び出し

`LiteLLM` が動けば、内部的にそれを利用しているAIエージェントフレームワーク `just-agents` でも同様に利用可能です。

https://github.com/longevity-genie/just-agents

```python
from just_agents.base_agent import BaseAgent

agent = BaseAgent(llm_options=llm_options)
print(agent.query(query))
```

こちらも問題なく動作します。これで、Function Calling（ツール連携）やMCPサーバーも利用できるでしょう。

https://qiita.com/SaitoTsutomu/items/3f2290ac8ef7fd1a25bc

---

## まとめ

この記事では、さくらインターネットの新サービス「**さくらのAI Engine**」をPythonから利用する方法を解説しました。

- `requests` を使ったシンプルなAPI呼び出し
- `LiteLLM` を使った統一的な利用
- `just-agents` を通じたエージェント利用

とくに `LiteLLM` を介することで、多くのエージェントフレームワークへの組み込みが容易になります。これにより、開発の幅が大きく広がるでしょう。ぜひ一度試してみてください！

