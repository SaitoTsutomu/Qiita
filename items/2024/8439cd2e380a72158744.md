title: Polarsの速度比較（vstack vs concat）
tags: Python concat vstack Polars
url: https://qiita.com/SaitoTsutomu/items/8439cd2e380a72158744
created_at: 2024-11-04 09:19:44+09:00
updated_at: 2024-11-04 09:19:44+09:00
body:

Polarsでは、concatはメモリコピーをして、vstackはメモリコピーをしないようです。

https://qiita.com/hkzm/items/8427829f6aa7853e6ad8#4-vstack-concat-%E3%81%A9%E3%81%A1%E3%82%89%E3%82%92%E4%BD%BF%E3%81%86%E3%81%8B%E3%81%AF%E5%BE%8C%E7%B6%9A%E3%81%A7%E3%81%AE%E3%82%AF%E3%82%A8%E3%83%AA%E6%AC%A1%E7%AC%AC

バージョン1.12.0で確かめてみました。

## 比較

16 x 16の`df1`を`n`回結合してみます。
メモリコピーしていれば、結合回数の自乗で計算時間が増えていくはずです。

```python
import numpy as np
import polars as pl
from timeit import timeit

df1 = pl.DataFrame(
    np.arange(256).reshape(16, -1),
    [f"col{i:02}" for i in range(16)],
)

concat_code = """\
df = df1
for _ in range(n):
    df = pl.concat([df, df1])
"""

vstack_code = """\
df = df1
for _ in range(n):
    df = df.vstack(df1)
"""

times = [1, 100, 200, 300, 400]

vstack_times = [
    timeit(vstack_code, number=100, globals=locals())
    for n in times
]

concat_times = [
    timeit(concat_code, number=100, globals=locals())
    for n in times
]
```

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0921a78d-1bc9-fc19-018d-b9afed965918.png)

図からはわかりにくいですが、どちらも自乗で増えています。
また、vstackの方が速いですが、2倍くらいしか違いません。思ったほど違いません。

なお、結合だけならvstackの方が速いですが、このあと加工したときにvstackの方が遅いかもしれません。

## 私の結論

* （シビアな状況でなければ）どちらでも良さそう
* 気になるなら、計測してみればよい

以上

