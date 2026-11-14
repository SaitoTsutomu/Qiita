title: OfTypeの使い方
tags: Windows C# LINQ
url: https://qiita.com/SaitoTsutomu/items/513e7d473fe5a8bd970f
created_at: 2013-01-06 11:01:59+09:00
updated_at: 2013-01-06 11:01:59+09:00
body:

WindowsのFormの画面にCheckBoxがたくさんあるとします。
プログラムで、すべてチェック済みにしたいとき、

```c#:C#
foreach (var cntr in Controls)
{
	var cb = cntr as CheckBox;
	if (cb != null) cb.Checked = true;
}
```

このように書くと思いますが、OfTypeを使うと以下のようにかけます。

```c#:C#
foreach (var cb in Controls.OfType<CheckBox>()) cb.Checked = true;
```

似たようなものに Castがありますが、Castでは、型が異なると例外になります。

