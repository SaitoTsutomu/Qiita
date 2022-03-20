title: enumの項目数
tags: C#
url: https://qiita.com/SaitoTsutomu/items/776b36c52a503eb06882
created_at: 2013-01-06 21:59:27+09:00
updated_at: 2013-03-15 08:27:43+09:00
body:

以下のようにすれば、`(int)Some.CountOfSome`で項目数(=3)として使えます。
最初の要素はデフォルトで0なので、`=0`は不要ですが、数字に意味があるのを明示しています。

```c#:C#
enum Some
{
	A = 0,
	B,
	C,
	CountOfSome
}
```

下記のようなFuhdukiさんのコメントの方法もあります。

```c#:C#
var count = Enum.GetValues(typeof(Some)).Length;
```
