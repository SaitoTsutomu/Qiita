title: 重み付きランダム抽出:Walker's Alias Method(Python)
tags: Python アルゴリズム
url: https://qiita.com/SaitoTsutomu/items/99d6f65fe8aaab7984f3
created_at: 2016-01-24 02:13:50+09:00
updated_at: 2016-01-24 02:13:50+09:00
body:

[重み付きランダム抽出:Walker's Alias Method](http://qiita.com/ozwk/items/6d62a0717bdc8eac8184#_reference-12387ce48c71f91280d7)のPython版

```py3:python
import numpy as np
def rand_from_prob(wgt, nn=1):
    """Walker's Alias Method"""
    if not isinstance(wgt, np.ndarray):
        wgt = np.array(wgt)
    wsm = sum(wgt)
    n = len(wgt)
    p = (wgt*n/wsm).tolist()
    a, hl = [0] * n, [0] * n
    l, h = 0, n-1
    for i in range(n):
        if p[i] < 1:
            hl[l] = i
            l += 1
        else:
            hl[h] = i
            h -= 1
    while l > 0 and h < n-1:
        j, k = hl[l-1], hl[h+1]
        a[j] = k
        p[k] += p[j] - 1
        if p[k] < 1:
            hl[l-1] = k
            h += 1
        else:
            l -= 1
    rr = np.random.rand(nn) * n
    ii = np.int32(np.floor(rr))
    rr -= ii
    return np.array([i if r < p[i] else a[i] for i, r in zip(ii, rr)])
```

O(1)なので高速。計算時間の比較。

```py3:python
w = np.random.rand(2000)
w /= sum(w)
%time x = rand_from_prob(w, 100000)
>>>
Wall time: 52 ms

%time y = np.random.multinomial(1, w, 100000)
>>>
Wall time: 6.75 s
```


