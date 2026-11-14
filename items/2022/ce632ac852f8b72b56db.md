title: panderaメモ
tags: Python pandas pandera
url: https://qiita.com/SaitoTsutomu/items/ce632ac852f8b72b56db
created_at: 2022-08-24 21:32:37+09:00
updated_at: 2022-08-26 11:19:35+09:00
body:

# 概要

[pandera](https://pandera.readthedocs.io/)には多くの機能がありますが、ここでは**型定義、検証、型強制**のシンプルな実装方法を紹介します。

- 型定義：DataFrameの構成や列の型を一元的に管理できる。内容を把握しやすく管理しやすい
- 検証：関数の入出力のDataFrameを自動的に検証できる。データ不整合を早期に発見できる
- 型強制：DataFrame作成時などに型を簡易に強制できる。検証が容易になる。

### 紹介方法の特徴

- **スキーマーの型は作らない**：検証や型強制でスキーマの型を使わないようにし、型が増えて混乱するのを防ぐ
- **アノテーションで検証する**：アノテーションさえ書けば検証できるようにする（戻り値が複数でも検証できる）
- **型強制をわかりやすくする**：型強制は検証で行わずタイミングは明示する

# 準備

下記を`pandera_tool.py`として用意しておきます[^1]。このファイルは共通で使えます。

[^1]: あるいは、`pip install -U pandera-tool`としてください。

```python
from pandera import SchemaModel, check_io, check_types
from pandera.typing import DataFrame


def to_dataframe(schema):
    return DataFrame[schema]


def to_schema(df_type):
    return df_type.__args__[0]


def check_annotations(func):
    anr = func.__annotations__.get("return")
    if anr and getattr(anr, "__origin__") == tuple:
        out = []
        for i, typ in enumerate(anr.__args__):
            tydf = getattr(typ, "__args__", (type,))[0]
            if issubclass(tydf, SchemaModel):
                out.append((i, to_schema(typ)))
        if out:
            return check_io(out=out)(check_types(func))
    return check_types(func)


def dtype(df_type, use_nullable=True):
    dc = {}
    schema = to_schema(df_type).to_schema()
    for name, column in schema.columns.items():
        typ = column.dtype.type
        if use_nullable and column.nullable and column.dtype.type == int:
            typ = "Int64"
        dc[name] = typ
    return dc
```

# 型定義

単なるDataFrameでは、どのような列で構成されているかわかりません。
そこで、panderaを使って、構成を確認できたり検証や型強制に使えるDataFrameで使えるカスタムの型を作成します。

panderaでは、いろいろな方法がありますが、ここでは下記のように作成します。

1. SchemaModelから派生した**スキーマの型**
1. 上のスキーマの型をスキーマとする**DataFrameの型**

型がいろいろあると紛らわしいので、**直接作るのはDataFrameの型だけ**とします。
スキーマの型が必要な場合は`to_schema()`で取得します。

## 型定義 - 実装方法

```py
from io import StringIO
from typing import Tuple
import pandas as pd
from pandera import Field, SchemaModel
from pandera.errors import SchemaError
from pandera.typing import Series
from pandera_tool import check_annotations, dtype, to_dataframe, to_schema

@to_dataframe
class DataFrameIn(SchemaModel):
    Name: Series[str] = Field()

    class Config:
        strict = True

@to_dataframe
class DataFrameOut(to_schema(DataFrameIn)):
    Age: Series[int] = Field()

    class Config:
        strict = True
```

`@to_dataframe`を使うことで、スキーマの型を見ることなく、DataFrameの型を作ります。
上記の例では、DataFrameInに文字列のName列があり、DataFrameOutにName列と整数のAge列があります。
また、`strict = True`とし、省略できる列は明示的に記述します（例：`Age: Optional[Series[int]]`）。

# 検証

検証は、`@check_annotations`をつけることで、関数の引数と戻り値に対し暗黙的にvalidateすることにします。戻り値はタプルも可能です。

## 検証 - 実装方法

```py

@check_annotations
def func_ok(df: DataFrameIn) -> DataFrameOut:
    return df.assign(Age=2)

@check_annotations
def func_err(df: DataFrameIn) -> DataFrameOut:
    return df.assign(Age="")

@check_annotations
def func_err_output_tuple(df: DataFrameIn) -> Tuple[DataFrameOut]:
    return (df.assign(Age=""),)

df_ok = pd.DataFrame({"Name": ["1"]})
df_ng = pd.DataFrame({"Name": [1]})

func_ok(df_ok)  # OK

try:
    func_ok(df_ng)  # Input error
except SchemaError as e:
    print(e)

try:
    func_err(df_ok)  # Output error
except SchemaError as e:
    print(e)

try:
    func_err_output_tuple(df_ok)  # Output error
except SchemaError as e:
    print(e)
```

# 型強制

`pd.read_csv()`では、データによっては意図しない型になることがあります。`dtype()`を指定することで型を強制できます。
作成済みのDataFrameに対しては、`astype(dtype(...))`で型を強制できます。

```python
df1 = pd.read_csv(StringIO("Name\n1"))
try:
    func_ok(df1)  # Input error
except SchemaError as e:
    print(e)

df2 = pd.read_csv(StringIO("Name\n1"), dtype=dtype(DataFrameIn))
func_ok(df2)  # OK

df3 = df_ng.astype(dtype(DataFrameIn))
func_ok(df3)  # OK
```

以上

