title: [PSP演習] 4A 線形回帰による予測
tags: C# Practice
url: https://qiita.com/SaitoTsutomu/items/1cf1764d11959daa46c4
created_at: 2013-01-04 05:54:11+09:00
updated_at: 2013-01-04 05:54:11+09:00
body:

n 個の実数の組(x,y)から y = β0 + β1*x となる線形回帰の係数 β0、β1 を求め算出せよ。
計算式は![計算式](http://plaza.harmonix.ne.jp/~fakira/turedure/pic2.GIF)を用いよ。
ゼロ割しないようにすること。

```c#
public static void CalcB0B1(double[][] l, out double b0, out double b1)
```
