title: 数理最適化RPG
tags: Python 最適化 pulp RPG 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/031ed3bc406abfb663d7
created_at: 2017-04-11 20:18:37+09:00
updated_at: 2020-05-07 13:03:44+09:00
body:

# 数理最適化RPG

数理最適化の問題を Role Playing Game (RPG)風に解いていく問題です。
[Code Puzzle - 任天堂](http://cp1.nintendo.co.jp/python.html)みたいなやつです。

# 内容

あなたは、『数理最適化の世界(The World of Mathematical Optimization)』にある『組合せ最適化の迷宮』の冒険者です。
迷宮は5階層からなり、各階層のボスが出す問題を解かないと先に進めません。さぁ、最下層にある秘宝を見つけに行きましょう。

- Python の数理最適化パッケージ PuLP を使って、全5問の 組合せ最適化問題 を解いてください。
- 問題は、簡単なものばかりです。(プログラムで8行以内。手計算だと大変ですが)
- [PuLPチートシート](c0bbf6cf8873ccd7edf3)(PuLP cheat sheet)

![pulp.png](https://qiita-image-store.s3.amazonaws.com/0/13955/b855aea1-70b5-0d12-c488-86e059d7367f.png)

# 追記

herokuで動くようにしました。

- https://github.com/SaitoTsutomu/OptRPG/blob/master/heroku.md

# お試し公開版の結果発表

ボス1|数名
:--|:--
ボス2|0名
ボス3|0名
ボス4|0名
ボス5|0名

全然でした。。。

---

# 今後の実行方法（古いです）
Dockerで下記のようにして、ブラウザで localhost:5000 を開いてください。

```bash:docker
docker run -it --rm -p 5000:5000 tsutomu7/optrpg
```

<a href="http://seaof-153-125-231-145.jp-tokyo-01.arukascloud.io:31779/"><img src="https://qiita-image-store.s3.amazonaws.com/0/13955/3ddfc810-e97c-9006-cb59-a8754c218aab.png"></a>

以上


