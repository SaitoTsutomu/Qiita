title: Python-MIPのLinExprTensor.astype()をDataFrameの列に追加したときの考察
tags: Python 最適化 python-mip
url: https://qiita.com/SaitoTsutomu/items/4f409507b04ddda4fb7c
created_at: 2022-06-14 12:50:38+09:00
updated_at: 2022-06-14 14:02:10+09:00
body:

## 概要

Python-MIPの`LinExpr`を要素に持つ多次元配列の`LinExprTensor`を考えます。
この`LinExprTensor`は、`astype(float)`により要素を`LinExpr`からfloatに変換してくれます。
ただし、型自体は`LinExprTensor`のままです。
これをDataFrameの列に追加すると、**一見floatの多次元配列に見えて実は異なる型になる**ので、その説明をします。

## 説明

まずは、実際のコードを実行して確認してみましょう。
下記の数理モデルは、非負の連続変数が1つで制約条件なしの最小化問題なので自明の最適解（値は0）を持ちますが、解に意味はないです。
型が興味の対象です。

```py
import pandas as pd
from mip import Model

m = Model()
df = pd.DataFrame()
df["Var"] = m.add_var_tensor((1,), "Var")
m.optimize()
df["Val"] = df.Var.astype(float)
print(f"{df.Val.dtype = }")
print(f"{repr(df.Val[0]) = }")
print(f"{repr(df.Val.max()) = }")
```

出力

```
df.Val.dtype = dtype('float64')
repr(df.Val[0]) = '0.0'
repr(df.Val.max()) = 'LinExprTensor(0.)'
```

`df.Val`は要素が`np.float64`のSeriesです[^1]。
`df.Val[0]`を確認すると`0.0`と出力されます。
しかし、`df.Val.max()`は、`0.0`にならずに`LinExprTensor(0.)`と出力されます。
これは、Seriesの内部構造で持つ多次元配列が`np.ndarray`ではなく`LinExprTensor`だからです。`type(df.Val.values)`とすることで確認できます。
多くの場合、このままでも特に問題になりませんが、ときとして警告が出ることがあります。具体的には下記を実行すると警告がでます。

[^1]: `import numpy as np`を想定しています。

```py
df.Val.max() == 0
```

出力

```
（中略）
FutureWarning: using `dtype=object` (or equivalent signature) will return object arrays in the future also when the inputs do not already have `object` dtype.
  return np.equal(self, other, dtype=object)
LinExprTensor(True)
```

これを解決するには、下記のように`LinExprTensor`を`np.ndarray`に変換すればOKです。

```py
df["Val"] = df.Var.astype(float).to_numpy()
# 下記も同じ
df["Val"] = df.Var.to_numpy().astype(float)
```

ちなみに、`df.Var.astype(float).to_numpy()`は`np.ndarray`ですが、`df.Var.astype(float).values`は`LinExprTensor`なので注意しましょう。

以上

