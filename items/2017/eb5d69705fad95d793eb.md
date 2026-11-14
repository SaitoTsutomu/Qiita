title: Python more-itertools 2.5 → 2.6 を比べてみた
tags: Python
url: https://qiita.com/SaitoTsutomu/items/eb5d69705fad95d793eb
created_at: 2017-03-23 11:30:54+09:00
updated_at: 2017-04-20 09:07:11+09:00
body:

# more-itertools が 2.5 から 2.6 で変わったところ

## (変更) ilen

実装が、sum から deque に変わった。何故 deque?

```py3:python3
from collections import deque
n = 10000
%timeit sum(1 for _ in range(n))                      # 2.5
%timeit deque(enumerate(range(n), 1), maxlen=1)[0][0] # 2.6
>>>
1000 loops, best of 3: 439 µs per loop
1000 loops, best of 3: 289 µs per loop
```

確かに、速くなっている。

## (追加) divide

おおよそ同じサイズになるように、指定個数に分割する。

```py3:python3
from more_itertools import divide, always_iterable, adjacent, groupby_transform, context
[tuple(i) for i in divide(3, range(10))]
>>>
[(0, 1, 2, 3), (4, 5, 6), (7, 8, 9)]
```


## (追加) always_iterable

iterable はそのまま、iterable でないものも iterable に。

```py3:python3
always_iterable(None)
>>>
()

always_iterable(1)
>>>
(1,)

always_iterable([1,3,5])
>>>
[1, 3, 5]
```


## (追加) adjacent

条件が一致するところの前後もTrueにする。

```py3:python3
list(adjacent(lambda x: x==3, range(7)))
>>>
[(False, 0),
 (False, 1),
 (True, 2),
 (True, 3),
 (True, 4),
 (False, 5),
 (False, 6)]

list(adjacent(lambda x: x==3, range(7), distance=2)) # 前後2つ差まで
>>>
[(False, 0),
 (True, 1),
 (True, 2),
 (True, 3),
 (True, 4),
 (True, 5),
 (False, 6)]
```


## (追加) groupby_transform

グルーピング後に、キーと値を変換する。

```py3:python3
[(i,list(j)) for i,j in groupby_transform([1,1,3,2,2,2],
                                          lambda x: f'<{x}>', # キーの変換
                                          lambda x: x*10)]    # 値の変換
>>>
[('<1>', [10, 10]), ('<3>', [30]), ('<2>', [20, 20, 20])]
```


## (追加) context (3.0 で削除)

with で使えるやつをジェネレータに。

```py3:python3
with open(ファイル名) as fp:
    print(fp.read())

↓ このように書ける

print(*[fp.read() for fp in context(open(ファイル名))])
```


参考: [itertools、more-itertoolsの紹介](http://qiita.com/Tsutomu-KKE@github/items/ddb5076ef62745f03b56)

以上

