title: Pydanticの`from_attributes`とは？
tags: Python pydantic from_attributes model_validate
url: https://qiita.com/SaitoTsutomu/items/391d6f091204710e3f92
created_at: 2024-09-27 23:28:12+09:00
updated_at: 2024-09-27 23:28:12+09:00
body:

## 概要

Pydanticのオブジェクトは、キーワード引数を使ってクラスから作成できます。
また、クラスの`model_validate()`を使うと、辞書やオブジェクトから作成できます。

このとき、クラスの`model_config`に`from_attributes=True`があるかないかで、変換元に使えるオブジェクトが変わります。

## 説明

2種類のクラスを考えましょう。

| クラス | 特徴                                |
| :----- | :---------------------------------- |
| User   | from_attributes=False（デフォルト） |
| UserFA | from_attributes=True                |

これらのクラスは、次のようにオブジェクトを作成できます。

| 構築方法 ＼ 引数          | 自クラスのオブジェクト | 他クラスのオブジェクト | 辞書  | キーワード引数 |
| :------------------------ | :--------------------: | :--------------------: | :---: | :------------: |
| `User() / UserFA()`       |           x            |           x            |   x   |       ◯        |
| `User.model_validate()`   |           ◯            |           x            |   ◯   |       ×        |
| `UserFA.model_validate()` |           ◯            |           ◯            |   ◯   |       ×        |

## サンプルコード

具体的にコードで確認してみましょう。

```python
from pydantic import BaseModel, ConfigDict

class BaseModelFA(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    name: str
    age: int

class UserFA(BaseModelFA):
    name: str
    age: int

user = User(name="Alice", age=30)
user_fa = UserFA(name="Alice", age=30)
user_fa_dict = user_fa.model_dump()  # {'name': 'Alice', 'age': 30}

print(User.model_validate(user_fa_dict))  # OK
# print(User.model_validate(user_fa))  # NG
print(UserFA.model_validate(user))  # OK
```

このように、`UserFA.model_validate()`は、他クラスのオブジェクトから作成できます。
一方、`User.model_validate()`は、他クラスのオブジェクトを渡すとValidationErrorになります。

## 補足

* 変換元に余計な情報があっても無視されます
* 変換先にデフォルト値があれば、変換元になくてもOKです

以上

