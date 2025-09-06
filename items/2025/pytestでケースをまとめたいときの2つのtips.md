title: pytestでケースをまとめたいときの2つのtips
tags: Python tips pytest
url: https://qiita.com/SaitoTsutomu/items/25dffa0c7bb2471a227b
created_at: 2025-06-18 17:08:32+09:00
updated_at: 2025-06-18 17:12:26+09:00
body:

pytestでテスト関数をまとめたいときの2つのtipsを紹介します。

テスト対象の関数は、割り算をする関数（`operator.truediv`）とします。

## 正常処理と異常処理をまとめる

次がテストコードです。

```python:test1_before.py
import operator

import pytest


def test_ok():
    """正常終了するテスト"""
    numerator, denominator = 1, 2
    actual = operator.truediv(numerator, denominator)
    assert actual == 0.5


def test_error():
    """異常終了するテスト"""
    numerator, denominator = 1, 0
    with pytest.raises(ZeroDivisionError):
        operator.truediv(numerator, denominator)
```

正常処理のテスト関数と、例外を確認する異常処理のテスト関数があります。
この2つの関数を1つの関数にしましょう。

一般に、1つの関数で複数のケースを実行するのはわかりにくくなるので避けるべきですが、`parametrize`を使えばわかりやすくまとめることができます。

次が修正したテストコードです。

```python:test1_after.py
import operator
from contextlib import nullcontext

import pytest


@pytest.mark.parametrize(
    ("numerator", "denominator", "context"),
    [
        (1, 2, nullcontext(0.5)),
        (1, 0, pytest.raises(ZeroDivisionError)),
    ],
)
def test(numerator, denominator, context):
    """正常終了と異常終了のテスト"""
    with context as expected:
        actual = operator.truediv(numerator, denominator)
        assert actual == expected
```

`nullcontext`によりwithで統一して使えるようになります。
正常処理の場合は、そのままassertで確認がされます。
異常処理の場合は、例外が発生することが`pytest.raises`で確認され、assertは実行されません。

この方法は、pytestの公式ドキュメントに載っている方法です。

https://docs.pytest.org/en/stable/example/parametrize.html#parametrizing-conditional-raising

## 複数のフィクスチャをまとめる

次がテストコードです。
テスト対象の関数の引数がJSONのファイルに定義されているという想定です。
2つのフィクスチャがそれぞれPathオブジェクトを返します。

```python:test2_before.py
import json
import operator
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def file1():
    with tempfile.NamedTemporaryFile(mode="w+") as tf:
        tf.write('{"numerator": 1, "denominator": 2, "expected": 0.5}')
        tf.flush()
        yield Path(tf.name)


@pytest.fixture
def file2():
    with tempfile.NamedTemporaryFile(mode="w+") as tf:
        tf.write('{"numerator": 3, "denominator": 4, "expected": 0.75}')
        tf.flush()
        yield Path(tf.name)


def test1(file1):
    c = json.loads(file1.read_text())
    actual = operator.truediv(c["numerator"], c["denominator"])
    assert actual == c["expected"]


def test2(file2):
    c = json.loads(file2.read_text())
    actual = operator.truediv(c["numerator"], c["denominator"])
    assert actual == c["expected"]

```

フィクスチャが違うだけなのでテスト関数をまとめたいですが、`parametrize`ではフィクスチャを扱えません。
このようなときは、`request.param`が便利です。

次が修正したテストコードです。

```python:test2_after.py
import json
import operator
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(
    params=[
        '{"numerator": 1, "denominator": 2, "expected": 0.5}',
        '{"numerator": 3, "denominator": 4, "expected": 0.75}',
    ]
)
def file(request):
    with tempfile.NamedTemporaryFile(mode="w+") as tf:
        tf.write(request.param)
        tf.flush()
        yield Path(tf.name)


def test(file):
    c = json.loads(file.read_text())
    actual = operator.truediv(c["numerator"], c["denominator"])
    assert actual == c["expected"]
```

`params`の要素が2つなので、`file`フィクスチャを使ったテスト関数は2回実行されます。

以上

