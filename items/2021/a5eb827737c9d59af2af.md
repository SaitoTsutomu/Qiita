title: Python-Fireについて
tags: Python Fire python-fire
url: https://qiita.com/SaitoTsutomu/items/a5eb827737c9d59af2af
created_at: 2021-06-09 12:05:18+09:00
updated_at: 2021-12-30 10:26:37+09:00
body:

# Pythonのコマンドラインツール作成方法

Pythonでは、標準ライブラリーのargparseを使って、コマンドラインツールを作ることができます。

また、サードパーティのライブラリーが、[Awesome Python - Command-line Interface Development](https://github.com/vinta/awesome-python#command-line-interface-development) に紹介されています。

この中でGitHub上でStar数が最も多いのはPython Fireです。

# Python Fireについて

Python Fireは、Google製のライブラリーです。`pip install fire`でインストールすると使えます。

Python Fireを使うと、「**コマンドラインからオブジェクトを自由に操作**」できるようになります。
そのために必要なことは、**オブジェクトをFireに登録することだけ**です。簡単に使い始められるというのがメリットです。

オブジェクトには、関数やクラスも含めて任意のオブジェクトが扱えます。
ドキュメントは、[The Python Fire Guide](https://github.com/google/python-fire/blob/master/docs/guide.md) です。

以下に主な使用方法を紹介します。

## 関数のコマンドライン化

Python Fireを使うには、`from fire import Fire`して、`Fire(コマンドラインで使用したい関数)`とします。つまり「使用したい関数を`Fire`に登録」だけです。

下記を`sample.py`というファイル名で作成してください（以降も同名のファイルを扱います）。

```python
from random import choice
from fire import Fire

Fire(choice)
```

`python sample.py [1,2,3]`を実行すると、`1, 2, 3`のいずれかが出力されます。これは、Pythonで`print(choice([1, 2, 3]))`を実行するのと同じになります。

また、`python sample.py [大吉,吉,小吉]`を実行すると、`大吉, 吉, 小吉`のいずれかが出力されます。

- `python sample.py ["大吉","吉","小吉"]`としなくても「大吉」などを文字列と認識します。
- `python sample.py [大吉, 吉, 小吉]`のようにスペースを入れるとエラーになるので注意してください。

`Fire(choice)`とするだけで、簡単に、おみくじとして使うことができます。

## ヘルプの表示

以下のいずれの方法でもヘルプを表示できます。

- `python sample.py --help`
- `python sample.py -- --help`
- `python sample.py -h`
- `python sample.py -- -h`

このように、Python Fireでは、自動的に「ヘルプを表示する機能」が使えます。

- `--help`あるいは`-h`をつけることでヘルプが表示されます。
  - 「Choose a random element from a non-empty sequence.」という説明が出てきます。
- `--`を書くことによって、以降の引数が、`sample.py`に対してはなく`Fire`に対するものになります。今回は、「`--help`や`-h`」が`sample.py`の引数でないことが自明なので、`--`は不要になっています。

また、自作の関数を登録して、詳しいヘルプを出したい場合は、その関数にdocstringを記述してください。

## 複数の関数のコマンドライン化

複数の関数を使えるようにするには、`Fire`に辞書を渡します。
辞書のキーに**コマンド名**を、値に**関数**を指定します。

たとえば、`Fire({"min": min, "max": max})`とすることで、`min`と`max`の2つのコマンドが使えます。

`python sample.py -h`または`python sample.py`でヘルプを表示します。
ヘルプを見ると、`python sample.py コマンド`のように使えて、コマンドとして`min`と`max`が選べることがわかります。

- `python sample.py min 1 -2 3`を実行すると、`min(1, -2, 3)`を計算して`-2`と表示されます。
- `python sample.py max 1 -2 3`を実行すると、`max(1, -2, 3)`を計算して`3`と表示されます。

引数にリストを指定できます。
`python sample.py min [1,-2,3]`を実行すると、`min([1, -2, 3])`を計算して`-2`と表示されます。

引数に文字列を指定できます。
`python sample.py min cat`を実行すると、`min("cat")`を計算して`a`と表示されます。`min("cat")`は、`min(["c", "a", "t"])`と同じです。

辞書のキーがコマンドになります。
もし、`Fire({"MIN": min, "MAX": max})`としていれば、`python sample.py MIN 1 -2 3`のように使います。

辞書の要素数は、3つ以上でも可能です。
もし、`Fire({"min": min, "max": max, "sum": sum})`としていれば、`python sample.py sum [1,-2,3]`を実行すると、`sum([1, -2, 3])`を計算して2と表示されます。

引数の文字列はPythonのコードのように評価され、適切な型のオブジェクトになって実行されます。
`python sample.py min [1,-2,3]`を実行すると、min関数の引数は**リスト**になります。
`python sample.py min cat`を実行すると、min関数の引数は**文字列**になります。

## Fire()のように空にした場合

`Fire()`のように引数を指定しないと、そのモジュールに出てくる変数をすべて登録します。

```python
from builtins import min, max
from fire import Fire as _Fire

_Fire()
```

上記のようにすると、`Fire({"min": min, "max": max})`と同じになります。なお、`_Fire`は、アンダースコアで始まっているため無視されます。

## クラスのコマンドライン化

クラスを指定することもできます。
下記を`sample.py`とします。

```python
from fire import Fire

class Command:
    min = min
    max = max

Fire(Command)
```

Commandクラスは、`min`と`max`のスタティックなメソッドを持っています。
このとき、`Fire(Command)`とすることで、下記と同じように動作します。

```python
c = Command()
Fire({"min": c.min, "max": c.max})
```

クラスを登録した場合でも、使い方は複数の関数の場合と変わりません。

|実行例|結果|
|:--|:--|
|`python sample.py min cat`|`a`|
|`python sample.py max cat`|`t`|
|`python sample.py`|ヘルプを表示|
|`python sample.py min -- --help`|minのヘルプを表示|

`python sample.py min cat`を実行すると、`Command().min('cat')`を実行し結果を表示します。

## メソッドを定義したクラスのコマンドライン化

スタティックでないメソッドを定義したクラスでは、以下のようになります。

```python
from fire import Fire

class Command:
    def min(self, *args):
        """return smallest args"""
        return min(args)

    def max(self, *args):
        """return largest args"""
        return max(args)

Fire(Command)
```

Commandクラスのメソッドは、スタティックでないので、第1引数は自分自身（`self`）にします。

実行例は以下のようになります。

|実行例|結果|
|:--|:--|
|`python sample.py min 3 -2 1`|`-2`|
|`python sample.py max 3 -2 1`|`3`|

※ `python sample.py min 3 -2 1`は、`Command().min(3, -2, 1)`に対応し、`min((3, -2, 1))`を計算し、`-2`と出力されます。

※ `python sample.py min cat`は、`Command().min("cat")`に対応し、`min(("cat", ))`を計算し、`cat`と出力されることに注意してください。

## `__init__`メソッドを定義したクラスのコマンドライン化

前節では、`python sample.py min`を実行すると、`Command().min()`が呼ばれ、`min(())`を実行しようとしてエラーになります。

一般に、`min((), default=0)`のように`default`を指定すると、エラーにならずに`0`を返すようになります。

ここでは、`__init__`メソッドを作成し、`min`の`default`引数を指定できるようにします。

以下のように、Commandクラスの`__init__`メソッドで`default`を受け取れるようにし、それを`min`や`max`で使うようにします。

```python
from fire import Fire

class Command:
    def __init__(self, default=0):
        self.default = default

    def min(self, *args):
        """return smallest args"""
        return min(args, default=self.default)

    def max(self, *args):
        """return largest args"""
        return max(args, default=self.default)

Fire(Command)
```

このようにすることで、引数が空でもエラーにならずに、`0`を返します。
引数`default`に値を指定するには、下記のように`--default 値`というオプションをつけます。

|実行例|結果|
|:--|:--|
|`python sample.py min`|`0`|
|`python sample.py max --default -1`|`-1`|

## 別々の引数があるクラスのコマンドライン化

`__init__`メソッドと、通常のメソッド（`some`）の両方に引数がある場合は以下のようになります。

```python
from fire import Fire

class Command:
    def __init__(self, arg1=1):
        self.arg1 = arg1
    def some(self, arg2=2):
        return self.arg1, arg2

Fire(Command)
```

|実行例|結果|
|:--|:--|
|`python sample.py some`|`[1, 2]`|
|`python sample.py some --arg1 10`|`[10, 2]`|
|`python sample.py some 20`|`[1, 20]`|
|`python sample.py some --arg2 20`|`[1, 20]`|
|`python sample.py some --arg1 10 20`|`[10, 20]`|
|`python sample.py some --arg1 10 --arg2 20`|`[10, 20]`|

- メソッドの引数にデフォルト値があれば、コマンドラインで省略できます。

- `__init__`メソッドと通常のメソッドのどちらの引数も、同じように指定できます。同名の引数の場合、`__init__`メソッドが優先されます。

- `--引数名`をつけない場合、通常のメソッドの引数と解釈されます。
- Python Fireへのオプションを指定したい場合は、`python sample.py -- --help` のように`--`の後に書きます。

**補足**

もし、`def some(self, arg2):`のように定義していれば、下記は`arg2`が指定されていないのでエラーになります。

- `python sample.py some`
- `python sample.py some --arg1 10`

## サブコマンドについて

Python Fireでは、サブコマンドを持つツールも簡単に作成できます。

```python
from fire import Fire

class Bin:
    """Convert binary number from/to decimal number."""
    def from_dec(self, n):
        """Convert binary number from decimal number."""
        return bin(n)
    def to_dec(self, n):
        """Convert binary number to decimal number."""
        return int(str(n), 2)

class Oct:
    """Convert octal number from/to decimal number."""
    def from_dec(self, n):
        """Convert octal number from decimal number."""
        return oct(n)
    def to_dec(self, n):
        """Convert octal number to decimal number."""
        return int(str(n), 8)

class Command:
    bin = Bin
    oct = Oct

Fire(Command)
```

- 上記のように記述することで、binコマンドとoctコマンドが使えます。
- binコマンドの値は、Binなので、Binクラスのメソッドをサブコマンドとして使えます。
- octコマンドの値は、Octなので、Octクラスのメソッドをサブコマンドとして使えます。

|実行例|結果|意味|
|:--|:--|:--|
|`python sample.py`|（略）|コマンドのヘルプ表示|
|`python sample.py bin`|（略）|binコマンドのサブコマンドのヘルプ表示|
|`python sample.py bin from_dec 3`|`0b11`|10進数の数字3を2進数の数字に変換|
|`python sample.py bin to_dec 11`|`3`|2進数の数字11を10進数の数字に変換|
|`python sample.py oct from_dec 9`|`0o11`|10進数の数字9を8進数の数字に変換|
|`python sample.py oct to_dec 11`|`9`|8進数の数字11を10進数の数字に変換|

**補足その1**

```python
class Command:
    bin = Bin
    oct = Oct

Fire(Command)
```

上記の代わりに、`Fire({"bin": Bin, "oct": Oct})`のように辞書で書いても同じ機能になります。
ただし、Commandクラスにはdocstringを書けますが、辞書では書けません。

**補足その2**

```python
class Command:
    bin = Bin()
    oct = Oct()

Fire(Command)
```

上記のように、「クラスではなくオブジェクトを指定」しても同じように使えます。

## コマンドチェーンについて

Python Fireでは、コマンドをつなげていくことができます。

`python sample.py xxx`が返すオブジェクトがyyyという（メソッドなどの）属性を持っていれば、`python sample.py xxx yyy`を実行できます。
また、それが返すオブジェクトがzzzという属性を持っていれば、`python sample.py xxx yyy zzz`を実行できます。
これは、いくつでもつなげることができます。

下記を`sample.py`とします。

```python
import calendar
from fire import Fire

Fire(calendar)
```

`python sample.py TextCalendar prmonth 2021 2`を実行すると下記のように、2021年2月のカレンダーが表示されます。

```
   February 2021
Mo Tu We Th Fr Sa Su
 1  2  3  4  5  6  7
 8  9 10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
```

- `Fire`では、`calendar`モジュールを登録しています。
- `calendar`モジュールでは、`TextCalendar`クラスが使えます。
- `TextCalendar`クラスでは、`prmonth`というカレンダーを表示するメソッドが使えます。
- `prmonth`メソッドの引数は、年と月です。

以上から、`python sample.py TextCalendar prmonth 2021 2`を実行すると、`calendar.TextCalendar().prmonth(2021, 2)`に対応し、カレンダーが表示されます。

**補足**

Fireは、オプションで実行状態のトレースを出力できます。デバッグ時に役立ちます。

`python sample.py TextCalendar prmonth 2021 2 -- --trace`とすると下記のように出力されます。

```
Fire trace:

1. Initial component
2. Accessed property "TextCalendar" (中略/calendar.py:293)
3. Instantiated class "TextCalendar" (中略/calendar.py:293)
4. Accessed property "prmonth" (中略/calendar.py:346)
5. Called routine "prmonth" (中略/calendar.py:346)
```

## クラス指定、オブジェクト指定の違い

**クラスを指定する例**

```python
class Command:
    def __init__(self, hello='Hello'):
        self.hello = hello
    def say(self)
        return self.hello

Fire(Command)  # クラスを指定
```

`python sample.py --hello Hi say`で`Hi`と出力されます。このように、実行時に`__init__`メソッドの引数を指定できます。

**オブジェクトを指定する例**

```python
class Command:
    def __init__(self, hello='Hello'):
        self.hello = hello
    def say(self):
        return self.hello

Fire(Command('Hi'))  # オブジェクトを指定
```

`python sample.py say`で`Hi`と出力されます。このように、実行時に指定していない`__init__`メソッドの引数が使われます。`__init__`メソッドの引数は変更できません。

**クラス指定、オブジェクト指定の違いのまとめ**

| クラスを指定                      | オブジェクトを指定                 |
| --------------------------- | ------------------------- |
| ヘルプ中の文言「`sample.py COMMAND`」 | ヘルプ中の文言「`sample.py GROUP`」 |
| オブジェクトを自動で生成                | オブジェクトを明示的に生成             |
| `__init__`メソッドの引数を指定可能      | `__init__`メソッドの引数は指定不可    |

## 副作用のあるメソッドのコマンドチェーン

ここでは、`print()`で結果を出力するメソッドをつなげる例を紹介します。

```python
import random
from fire import Fire

class Command:
    def __init__(self, *words):
        self._words = list(words)

    def s(self):
        """shuffle"""
        random.shuffle(self._words)
        print(" ".join(self._words))
        return self

    def r(self):
        """reverse"""
        self._words.reverse()
        print(" ".join(self._words))
        return self

    def __str__(self):
        return ""

Fire(Command)
```

**実行例**

- `python sample.py A B C D E - s`：A〜Eをシャッフルして出力
- `python sample.py A B C D E - s s`：A〜Eをシャッフルして出力を繰り返す
- `python sample.py A B C D E - s s r`：A〜Eをシャッフルして出力を繰り返し、反転し出力

**コードの説明**

- `-`引数は、現在のメソッド（`__init__`メソッド）の引数の終わりを指示します。
- `s()`は、`self._words`をシャッフルして出力します。
- `r()`は、`self._words`を反転して出力します。
- `s()`や`r()`は`self`を返すので、最後に`__str__`メソッドが呼ばれて空文字列を出力します。
- `_words`という代わりに`words`という名前のデータ属性にすると、`words`というコマンドがヘルプに表示されます。
- `_words`のようにアンダースコアで始まる名前にすると、ヘルプには表示されませんが、利用はできます。

## ブール型の引数

ブール型の引数は値を省略できます。

```python
def show_args(args):
    print(args)

Fire(show_args)
```

**実行例**

| コマンド                           | 出力    |
| ------------------------------ | ----- |
| `python sample.py --args`       | True  |
| `python sample.py --noargs`     | False |
| `python sample.py --args True`  | True  |
| `python sample.py --args False` | False |

- 引数の値を省略すると、Trueを指定したとみなされます。
- 引数の名前に`no`をつけて、値を省略すると、Falseを指定したとみなされます。

以上

