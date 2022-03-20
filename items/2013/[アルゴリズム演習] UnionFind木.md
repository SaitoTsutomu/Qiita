title: [アルゴリズム演習] UnionFind木
tags: C# アルゴリズム Practice
url: https://qiita.com/SaitoTsutomu/items/2f0c3b305beff83ac487
created_at: 2013-01-04 07:03:38+09:00
updated_at: 2013-01-04 07:03:38+09:00
body:

UnionFind木を完成させよ。

+ グループ分けを管理するデータ構造。
+ 要素aと要素bが同じグループかどうかを調べる。
+ 要素aと要素bのグループを併合する。
+ 配列(parent)で親を管理。
+ 追加（Add）：最後にユニークな値を入れる。
+ 併合(Union)：片方のグループの木の根からもう片方のグループの木の根をはる。
+ 判定(IsSame)：親をたどり各々の根が同じかどうかを見る。
+ 根を調べる(Find)：親をたどる。

```c#
public class UnionFind
{
	private List<int> parent = new List<int>();
	public void Add() { ... }
	public bool IsSame(int i, int j) { ... }
	public int Find(int i) { ... }
	public void Unite(int a, int b) { ... }
}
```
