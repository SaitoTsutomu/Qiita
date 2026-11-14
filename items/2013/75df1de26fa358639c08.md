title: [PSP演習] 5A 数値積分
tags: C# Practice
url: https://qiita.com/SaitoTsutomu/items/75df1de26fa358639c08
created_at: 2013-01-04 05:57:48+09:00
updated_at: 2013-01-04 05:57:48+09:00
body:

次のような形式で、シンプソン則で積分する関数を作成せよ。

```c#
public delegate double CalcFunc(double x);
public static double Simpson(CalcFunc f, double lower, double upper);
```				
シンプソン則は、n 分割した n+1 個の位置での値に 1,4,2,4,2,...,1 を掛けて和をとり、 (upper-lower) を掛けて 3*n で割ったものが積分値となる。分割数は偶数でなければいけない。 無限ループにならないようにチェックせよ。
