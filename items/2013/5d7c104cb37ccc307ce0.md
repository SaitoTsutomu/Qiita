title: [PSP演習] 8A ソート
tags: C# Practice
url: https://qiita.com/SaitoTsutomu/items/5d7c104cb37ccc307ce0
created_at: 2013-01-04 06:16:04+09:00
updated_at: 2013-01-04 06:16:04+09:00
body:

マージソートで安定ソートせよ。

```c#
public static void Sort<T>(IList<T> a, Comparison<T> f) { Sort<T>(a, f, 0, a.Count); }
public static void Sort<T>(IList<T> a, Comparison<T> f, int i, int j);
```
