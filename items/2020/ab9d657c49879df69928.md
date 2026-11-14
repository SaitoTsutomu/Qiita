title: OR-Toolsで巡回セールスマン問題を解く
tags: Python 数学 最適化 組合せ最適化 ortools
url: https://qiita.com/SaitoTsutomu/items/ab9d657c49879df69928
created_at: 2020-05-04 21:40:41+09:00
updated_at: 2020-11-11 16:54:31+09:00
body:

## これなに

「[Watsonで巡回セールスマン問題を解く](https://qiita.com/makaishi2/items/78570f9283c0bc6c7e6c)」をOR-Toolsを使って解いてみました。

### OR-Toolsとは

Googleが作成した無料のOperations Research関連のライブラリーです。
OR-Toolsを使うと、[配送最適化問題](https://qiita.com/SaitoTsutomu/items/1126e1493ff601a858c9)や[巡回セールスマン問題](https://qiita.com/SaitoTsutomu/items/def581796ef079e85d02)を解くことができます。

参考：https://developers.google.com/optimization/routing

## 解いてみる

そのままだと、ちょっと面倒なので、ortoolpyのラッパーを使います。

```py
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance
from ortoolpy import ortools_vrp

url = 'https://raw.githubusercontent.com/makaishi2/sample-data/master/data/att48.csv'
df = pd.read_csv(url)[:30]  # 元記事に揃えて30都市にする
dist = distance.cdist(df.values, df.values).astype(int)
route = ortools_vrp(len(df), dist, limit_time=1)[0]
plt.figure(figsize=(6, 6))
plt.plot(df.x[route], df.y[route], 'bo-');
```

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9bfdb62e-878b-61c4-c730-c79c7390961e.png)

計算時間1秒で、元記事と同じ結果が出ました（元記事の計算時間は、226秒）。

### 補足

OR-Toolsのアルゴリズムは近似解法です。`limit_time=1`をつけないと一瞬で解がでますが、若干精度が悪いです。
そこで、計算時間を1秒にすることで、元記事と同じ厳密解が得られています。

※ `dist`を整数にしていますが、OR-Toolsは距離を整数にしないといけません。

