title: [PSP演習] 1A リンクリスト作成
tags: C# Practice
url: https://qiita.com/SaitoTsutomu/items/28de17005ac2bdfb91cb
created_at: 2013-01-04 05:24:48+09:00
updated_at: 2013-01-04 05:24:48+09:00
body:

下記の「TODO」を埋めて、リンクリストを完成させよ。

``` c#
public class MyLinkedList<T> : IEnumerable<T>
{
	internal class Item
	{
		internal T Value;
		internal Item Next;
		public Item(T t){ Value = t; }
	}
	public int Length { get; private set; }
	private Item Top;
	public MyLinkedList()
	{
		// TODO:初期化
	}
	public void AddLast(T t)
	{
		// TODO:追加
	}
	public IEnumerator<T> GetEnumerator()
	{
		// TODO:反復子
	}
	System.Collections.IEnumerator
		System.Collections.IEnumerable.GetEnumerator()
	{
		return GetEnumerator();
	}
}
```

