title: just-agentsでLM Studioのmistral-small3.2を使ってみた
tags: Python LLM LMStudio just-agents
url: https://qiita.com/SaitoTsutomu/items/111700e113819b50d7c7
created_at: 2025-06-22 22:25:41+09:00
updated_at: 2025-06-22 22:28:52+09:00
body:

## 概要

mistral-small3.2が出てたので、LM Studioでダウンロードして、just-agentsからローカルで使ってみた備忘録です。

なお、just-agentsはシンプルなAIエージェントのライブラリです。

* just-agents: https://github.com/longevity-genie/just-agents
* mistral-small3.2: https://lmstudio.ai/models/mistralai/mistral-small-3.2

## コード

```python
import base64
import urllib

from just_agents.base_agent import BaseAgent
from just_agents.data_classes import ImageContent as _ImageContent
from just_agents.data_classes import Message, Role, TextContent
from pydantic import AnyUrl


class ImageContent(_ImageContent):
    image_url: AnyUrl


def describe(url: str) -> str:
    llm_options = {
        "model": "lm_studio/mistralai/mistral-small-3.2",
        "api_base": "http://localhost:1234/v1",
        "api_key": "_",
    }
    agent = BaseAgent(llm_options=llm_options)
    with urllib.request.urlopen(url) as fp:
        b64 = base64.b64encode(fp.read()).decode("utf-8")
    message = Message(
        role=Role.user,
        content=[
            TextContent(text="画像の説明"),
            ImageContent(image_url=f"data:image/jpeg;base64,{b64}"),
        ],
    )
    return agent.query(message, remember_query=False)


print(describe("file:///path/to/some.jpg"))
print(describe("https://path/to/some.jpg"))
```

## 解説

just-agentsにはImageContentというのがあるので、これを使ってみましょう。
ローカルのLLMの場合は、画像をbase64で渡す必要があるようです。
実際に実行すると、下記のようなエラーになります。

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for ImageContent
image_url
  URL should have at most 2083 characters [type=url_too_long, \
  input_value='data:image/jpeg;base64,/...', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/url_too_long
```

調べると、[ImageContent.image_urlの型がHttpUrl](https://github.com/longevity-genie/just-agents/blob/32d53f2e4e721c096ebf6f8555e05bf34bd6b44d/core/just_agents/data_classes.py#L60-L62)で、文字列の長さが長いためPydanticでバリデーションエラーになってようです。

今回は、下記のように無理やりAnyUrlに変えて回避しました。

```python
from just_agents.data_classes import ImageContent as _ImageContent
from pydantic import AnyUrl

class ImageContent(_ImageContent):
    image_url: AnyUrl
```

軽いモデルですが、わりと良さそうな印象でした

以上

