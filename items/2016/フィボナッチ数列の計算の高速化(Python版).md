title: フィボナッチ数列の計算の高速化(Python版)
tags: Python 数学
url: https://qiita.com/SaitoTsutomu/items/be069ea89c85191799fa
created_at: 2016-02-16 14:49:20+09:00
updated_at: 2016-02-16 14:59:37+09:00
body:

[フィボナッチ数列の計算の高速化(Ruby版)](http://qiita.com/mathhun/items/4c117d33028a888f6fcf)をPythonでもやってみました。

定義は、一緒です。

```py3:python
# 通常版
def fib1(n):
    if n <= 1:
        return n
    n0, n1 = 0, 1
    for _ in range(n):
        n0, n1 = n1, n0+n1
    return n0

# 高速版
def fib2(n):
    if n <= 1:
        return n
    result = [1, 0, 0, 1]
    matrix = [1, 1, 1, 0]
    while n > 0:
        if n % 2:
            result = mul(matrix, result)
        matrix = mul(matrix, matrix)
        n //= 2
    return result[2]

def mul(a, b):
    return [a[0]*b[0] + a[1]*b[2],
            a[0]*b[1] + a[1]*b[3],
            a[2]*b[0] + a[3]*b[2],
            a[2]*b[1] + a[3]*b[3]]
```

ちゃんとできてます。

```py3:python
print([fib1(i) for i in range(11)])
print([fib2(i) for i in range(11)])
>>>
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

時間計測。

```py3:python
%timeit fib1(100000)
%timeit fib2(100000)
%timeit fib1(1000000)
%timeit fib2(1000000)
>>>
10 loops, best of 3: 75.7 ms per loop
100 loops, best of 3: 10.6 ms per loop
1 loops, best of 3: 6.9 s per loop
1 loops, best of 3: 374 ms per loop
```

Rubyより10倍以上、速い！

ちなみに、numpy使うと、1476項(≒1.3e309)までしか計算できませんでした。

以上

