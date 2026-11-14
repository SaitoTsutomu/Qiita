title: panderaなどから仕様の自動生成
tags: Python pandas documentation dataclass pandera
url: https://qiita.com/SaitoTsutomu/items/9ca3e283f711834fa4b4
created_at: 2024-06-28 22:21:59+09:00
updated_at: 2024-06-28 22:21:59+09:00
body:

# panderaなどから仕様の自動生成

panderaなどのクラスから仕様を表示する方法を紹介します。

## panderaの例

まずはpanderaを使ってみましょう。
次のようにPersonを定義すると、以下のようにバリデーションできます。

```python
import pandas as pd
import pandera as pa
import pandera.typing as pat


class Person(pa.DataFrameModel):
    """個人"""

    name: pat.Series[str] = pa.Field(description="名前")
    age: pat.Series[int] = pa.Field(description="年齢")
    email: pat.Series[str] | None = pa.Field(description="メール")


df = pd.DataFrame([["Alice", 30]], columns=["name", "age"])
Person.validate(df)
```

次にこのPersonクラスから、仕様を出力してみましょう。

```python
def show_class(cls):
    print(f"{cls.__name__}クラス：{cls.__doc__}")
    show_dataframe(cls)


def show_dataframe(cls):
    schema = cls.to_schema()
    for column in schema.columns.values():
        s = "" if column.required else "（Optional）"
        print(f"* {column.name}：{column.description}{s}")


show_class(Person)
```

**出力**

```
Personクラス：個人
* name：名前
* age：年齢
* email：メール（Optional）
```

emailは存在しなくてもよい列なので、Optionalと表示しています。

## dataclassの例

続いて、dataclassも仕様を出力できるようにしてみましょう。
まずは、クラスを定義します。

```python
from dataclasses import dataclass, field, fields


def description(s, **kwargs):
    return field(metadata={"description": s}, **kwargs)


@dataclass
class Building:
    """建物"""

    name: str = description("名称")
    address: str = description("住所")
```

次のように仕様を出力できます。関数`show_class()`は置き換えてください。

```python
def show_class(cls):
    print(f"{cls.__name__}クラス：{cls.__doc__}")
    if issubclass(cls, pa.DataFrameModel):
        show_dataframe(cls)
    else:
        show_dataclass(cls)


def show_dataclass(cls):
    for field_ in fields(cls):
        print(f'* {field_.name}：{field_.metadata.get("description")}')


show_class(Building)
```

**出力**

```
Buildingクラス：建物
* name：名称
* address：住所
```

Swagger UIのように、いつでも最新の仕様が確認できると便利になるでしょう。

以上

