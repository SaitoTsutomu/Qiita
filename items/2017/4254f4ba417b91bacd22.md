title: NumPyでしきい値以上の位置を求める
tags: Python numpy
url: https://qiita.com/SaitoTsutomu/items/4254f4ba417b91bacd22
created_at: 2017-04-20 11:12:18+09:00
updated_at: 2017-09-12 00:08:48+09:00
body:

# NumPyで 昇順のデータに対して value >= threshold となる index を求める
## 方法
1. 「np.array < th」の argmin
- 「np.array >= th」の searchsorted
- 「np.array < th」の長さ
- 「np.array < th」の sum
- 「np.array >= th」の where
- for ループで探す
- 「takewhile」 の長さ

7通りの方法で、結果が正しいことを確認

```py3:python
import numpy as np
from more_itertools import ilen
from itertools import takewhile

def find_index(a, ths):
    for i,v in enumerate(a):
        if v >= th:
            break
    return i

n = 10000000
x = np.arange(n)
th = n / 10
print((x < th).argmin())
print(np.searchsorted(x, th))
print(len(x[x < th]))
print((x < th).sum())
print(np.where(x>=th)[0][0])
print(find_index(x, th))
print(ilen(takewhile(lambda i: i < th, x)))
>>>
1000000
1000000
1000000
1000000
1000000
1000000
1000000
```

## 計測
```py3:python
%timeit np.searchsorted(x, th)
%timeit (x < th).argmin()
%timeit len(x[x < th])
%timeit (x < th).sum()
%timeit np.where(x >= th)[0][0]
%timeit find_index(x, th)
%timeit ilen(takewhile(lambda i: i < th, x))
>>>
3.84 µs ± 347 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
10.2 ms ± 215 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
12.5 ms ± 62.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
21.2 ms ± 411 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
43.1 ms ± 635 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
3.36 µs ± 19.3 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
5.74 µs ± 75.5 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```

```py3:python
th = 10
%timeit np.searchsorted(x, th)
%timeit (x < th).argmin()
%timeit len(x[x < th])
%timeit (x < th).sum()
%timeit np.where(x >= th)[0][0]
%timeit find_index(x, th)
%timeit ilen(takewhile(lambda i: i < th, x))
>>>
3.31 µs ± 24.8 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
9.86 ms ± 28.5 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
13.1 ms ± 530 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
21.7 ms ± 761 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
46.9 ms ± 1.8 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
3.76 µs ± 310 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
6.01 µs ± 231 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```

## 考察
- searchsortedがよい
- argmin と forループ ならば、ソートされている必要はない

以上

