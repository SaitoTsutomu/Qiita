title: さくらのAI EngineをLangflowから使ってみた
tags: Python さくらのクラウド AI langflow
url: https://qiita.com/SaitoTsutomu/items/03d245afb0a55ab2906f
created_at: 2025-10-05 11:02:33+09:00
updated_at: 2025-10-05 11:02:33+09:00
body:

## はじめに

さくらインターネットから新しい生成AIサービス「**さくらのAI Engine**」がリリースされました。

https://www.sakura.ad.jp/corporate/information/newsreleases/2025/09/24/1968221046/

この記事では、この「さくらのAI Engine」を**Langflowから利用する方法**を、順を追って分かりやすく解説します。

---

### 🎯 対象読者

* 「さくらのAI Engine」をLangflowで試してみたい方
* Langflowに興味がある、またはこれから使ってみたい方

---

## 💡 「さくらのAI Engine」とは？

「さくらのAI Engine」は、さくらインターネットの生成AI向けクラウド基盤「高火力」ベースの**API経由で利用できるAIサービス**です。

本記事では、チャット形式の対話が可能な「**Chat completions**」機能を利用します。

| サービス類型            | 基盤モデル                           |
| :---------------------- | :----------------------------------- |
| **Chat completions**    | `gpt-oss-120b`                       |
|                         | `llm-jp-3.1-8x13b-instruct4`         |
|                         | `Qwen3-Coder-30B-A3B-Instruct`       |
|                         | `Qwen3-Coder-480B-A35B-Instruct-FP8` |
| **Audio Transcription** | `whisper-large-v3-turbo`             |
| **Embeddings**          | `multilingual-e5-large`              |
| **ドキュメント（RAG）** | ―                                    |

利用プランには「**基盤モデル無償プラン**」と「従量課金プラン」の2種類があります。今回は、すぐに試せる「基盤モデル無償プラン」を利用します。

申し込み手順は以下をご覧ください。

https://www.sakura.ad.jp/aipf/ai-engine/

---

## 🚀 Langflowとは？

Langflowは、LLM（大規模言語モデル）を活用したアプリケーションを構築するためのGUIツールです。プログラミングの知識がなくても、チャットボットなどのプロトタイプをブロックを組み合わせて直感的に作成できます。

https://www.langflow.org/

また、UI上でPythonコードを記述して、独自のカスタムコンポーネントを作成することも可能です。既存のコンポーネントを改造したり、新しい機能を追加したりと、柔軟に拡張できます。

本記事では、「さくらのAI Engine」のLLMモデルを扱うためのコンポーネントを紹介します。

---

## 🔑 Step 1: アカウントトークンの作成

「さくらのAI Engine」のAPIを利用するには**アカウントトークンの作成**が必要です。
以下の管理画面から作成してください。

https://secure.sakura.ad.jp/ai/account-tokens

---

## 🛠️ Step 2: Langflowでの設定と実行

Langflowを起動してフローを作成します。

### Langflowの起動

ターミナルを開き、以下のコマンドを実行してLangflowを起動します。起動には少し時間がかかる場合があります。

```
uvx langflow run
```

### フローの作成

1. ターミナルに`Open Langflow`と表示されたら、ブラウザで `http://localhost:7860` を開く
2. `+ Create first flow` をクリックする
3. `Get started` の中から `Basic Prompting` を選択する

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a4db850d-ad62-4135-8bd7-091171ffbcc1.jpeg)

デフォルトでは `Language Model` というコンポーネントが配置されています。これを「さくらのAI Engine」用に変更します。

`Language Model` をクリックし、上部の `Code` を押してください。

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/4d18cfea-b362-43b0-9aee-9d74a1fd437c.png)


`Edit Code` 画面になるので、Pythonコードを下記に置き換えてください。

```python
from langchain_openai import ChatOpenAI
from langflow.base.models.model import LCModelComponent
from langflow.field_typing import LanguageModel
from langflow.inputs.inputs import BoolInput, DropdownInput, SecretStrInput, StrInput
from pydantic.v1 import SecretStr

SAKURA_AI_MODELS = [
    "gpt-oss-120b",
    "llm-jp-3.1-8x13b-instruct4",
    "Qwen3-Coder-30B-A3B-Instruct",
    "Qwen3-Coder-480B-A35B-Instruct-FP8",
]


class SakuraAIModelComponent(LCModelComponent):
    display_name = "SakuraAI"
    description = "Generate text using SakuraAI LLMs."
    icon = "cloud"
    inputs = [
        *LCModelComponent._base_inputs,
        DropdownInput(
            name="model_name",
            display_name="Model Name",
            info="Sakura AI model to use",
            options=SAKURA_AI_MODELS,
            value="gpt-oss-120b",
        ),
        StrInput(
            name="api_base",
            display_name="Sakura AI API Base",
            info="Base URL for API requests.",
            value="https://api.ai.sakura.ad.jp/v1",
            advanced=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="Sakura Account Token",
            info="The Sakura Account Token",
        ),
        BoolInput(
            name="stream",
            display_name="stream",
            info="If True, it will output stream.",
        ),
    ]

    def build_model(self) -> LanguageModel:
        api_key = SecretStr(self.api_key).get_secret_value() if self.api_key else None
        return ChatOpenAI(
            model=self.model_name,
            base_url=self.api_base,
            api_key=api_key,
            streaming=self.stream,
        )
```

`Check & Save`をクリックして保存すると、コンポーネントが`SakuraAI`に変わります。

---

### `SakuraAI`コンポーネントの設定

* `SakuraAI`コンポーネント下部の右側にある`Model Response`から、`Chat Output`コンポーネントへ線をドラッグして接続する
* `Model Name` から利用するモデルを選択する（例：`gpt-oss-120b`）
* `Sakura Account Token` の `OPENAI_API_KEY` ラベルを削除し、作成したアカウントトークンを貼る

---

### フローの実行

設定が完了したら、動作を確認してみましょう。

画面右上の`Playground`ボタンをクリックします。
チャット画面が開きます。入力欄に「Hello」と表示されていることを確認し、`Send`ボタンをクリックしてください。
AIから返答があれば、接続は成功です。

作業を終了する際は、右上の✕ボタンでチャット画面を閉じ、左上の波アイコンからダッシュボードに戻ります。このとき、作成したフローは自動的に保存されます。
最後にブラウザを閉じ、ターミナルの実行を停止してください。

---

## まとめ

本記事では「さくらのAI Engine」をLangflowから利用する方法を紹介しました。
アカウントトークンの取得とコンポーネントの置き換えだけで簡単に利用できます。慣れてきたら独自の機能やRAGの利用も試してみましょう。

