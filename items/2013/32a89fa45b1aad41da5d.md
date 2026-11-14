title: ブラウザでPython：Brythonのすすめ
tags: Python Brython
url: https://qiita.com/SaitoTsutomu/items/32a89fa45b1aad41da5d
created_at: 2013-03-01 18:37:22+09:00
updated_at: 2013-03-01 19:58:24+09:00
body:

まずは、[Brythonのサイト](http://www.brython.info/index_en.html)を見てください。
時計が動いていますが、これは Python で書かれています。「ソースの表示」で確認してください。

つまり、javascriptの代わりにPythonが使えます。
実際に自分のサイトで動かすのに必要な作業は、以下の通りです。ファイルの置き場所は、IISを例にしています。

* [ダウンロード先](https://code.google.com/p/brython/downloads/list)からファイルをダウンロードしてください。
* ダウンロードしたファイルを C:\inetpub\wwwroot\libs フォルダに解凍して配置してください。ただし、brython.js は、C:\inetpub\wwwroot フォルダに配置してください。
* HTMLで、head タグ内に下記のように scriptタグを入れます。
* HTMLで、body タグ内に下記のように onloadを記述します。
* HTMLで、script タグ内で type を text/python にして、Pythonを記述します。

以上です。Let's try Brython!

```html:hello.html
<html><head><script src="/brython.js"></script></head>
<body onload="brython()">
<script type="text/python">
def echo():
    alert("hello %s !" % doc["zone"].value)
</script>
<p>Your name is : <input id="zone"><button onclick="echo()">clic !</button>
</p></body></html>
```
[hello.html](http://www.brython.info/gallery/hello.html)
