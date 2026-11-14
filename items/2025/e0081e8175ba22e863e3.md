title: Pythonの循環import：なぜこのコードは動作するのか？
tags: Python Import モジュール 循環参照
url: https://qiita.com/SaitoTsutomu/items/e0081e8175ba22e863e3
created_at: 2025-10-23 19:50:04+09:00
updated_at: 2025-10-24 09:22:43+09:00
body:

Pythonでモジュールを分割して開発していると、「循環import（循環インポート）」という問題に遭遇することがあります。
これは、2つ以上のモジュールが互いをインポートし合うことで発生します。

---

## 基本的なエラー例

まず、典型的なエラーが発生するケースを見てみましょう。

```python
# main.py
from sub import print_add

def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    print_add(1, 2)
```

```python
# sub.py
from main import add

def print_add(a: int, b: int) -> None:
    print(add(a, b))
```

この状態で `python3 main.py` を実行すると、`ImportError` が発生します。

### エラーの原因

1. `main.py` が `sub` モジュールから `print_add` をインポートしようとする
2. Pythonが `sub.py` の読み込みを開始する
3. `sub.py` が `main` モジュールから `add` をインポートしようとする
4. ここで循環が発生。Pythonは再び `main.py` を読み込もうとするが、`main.py` は `sub.py` の完了待ちのため、まだ完全に初期化されていない
5. 結果として、`sub.py` は未完成の `main` モジュールから `add` を見つけられず、`ImportError` が発生する

### 一般的な回避策

関数内でインポートを行うことで、循環のタイミングをずらす方法があります。

```python
# sub.py
def print_add(a: int, b: int) -> None:
    from main import add
    print(add(a, b))
```

---

## 発展例：これらのパターンはどう動作する？

次に、`import` と `from ... import` の違いによって挙動が変わる例を見てみましょう。
一見どれも循環インポートに見えますが、実際には挙動が異なります。

### パターン1

```python
# main.py
from sub import print_add

def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    print_add(1, 2)
```

```python
# sub.py
import main

def print_add(a: int, b: int) -> None:
    print(main.add(a, b))
```

**結果： ❌ `ImportError` 発生**

---

### パターン2

```python
# main.py
import sub

def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    sub.print_add(1, 2)
```

```python
# sub.py
from main import add

def print_add(a: int, b: int) -> None:
    print(add(a, b))
```

**結果： ✅ 正常に実行される**

---

### パターン3

```python
# main.py
import sub

def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    sub.print_add(1, 2)
```

```python
# sub.py
import main

def print_add(a: int, b: int) -> None:
    print(main.add(a, b))
```

**結果： ✅ 正常に実行される**

---

### パターン4

```python
# main.py
import sub

def add(a: int, b: int) -> int:
    return a + b

sub.print_add(1, 2)
```

```python
# sub.py
import main

def print_add(a: int, b: int) -> None:
    print(main.add(a, b))
```

**結果： ❌ `AttributeError` 発生**

---

## なぜこうなるのか？：詳細解説

これらの違いは、Pythonの「モジュール初期化のタイミング」と「名前解決の仕組み」に起因します。

### 成功と失敗の分岐点

* **`import <モジュール>` の場合（例：パターン2の `main.py`）**  
  `import sub` により、`sub` というモジュールオブジェクトへの参照が確保されます。
  この時点では `sub` の中身（関数など）は未定義でも、オブジェクト自体は存在します。
  実際に `sub.print_add()` が呼ばれるのは `main` の初期化完了後なので、問題なく動作します。

* **`from <モジュール> import <名前>` の場合（例：パターン1の `main.py`）**  
  `from sub import print_add` の実行時点で `sub.print_add` を直接参照する必要があるため、
  `sub` の初期化が終わっていないと `ImportError` になります。

---

### パターン4で `AttributeError` になる理由

`if __name__ == "__main__":` がないため、モジュール初期化の途中で `sub.print_add(1, 2)` が実行されてしまいます。

1. `main.py` が `import sub` を実行し、`sub.py` の読み込みを開始  
2. `sub.py` が `import main` を実行し、再び `main` の初期化を試みる  
3. この時点で `sub` は空のモジュールオブジェクトとして登録済み  
4. `add()` が定義される  
5. 直後に `sub.print_add(1, 2)` が呼ばれるが、`sub` 内の関数はまだ定義途中  
6. よって `AttributeError` が発生する

---

## まとめ

- 循環インポートのエラーは、**モジュールの初期化が終わる前に未定義の属性へアクセス**することで起きる  
- `import ...` はモジュール全体を遅延的に参照できるため、エラーを回避できる場合がある  
- `from ... import ...` は属性を即時に解決するため、循環関係では失敗しやすい  
- `if __name__ == "__main__":` の利用は、循環インポートによる実行タイミング問題の回避にも有効  

循環インポートを根本的に避けるには、モジュールの依存関係を整理し、共通部分を別モジュールへ切り出す設計が推奨されます。

