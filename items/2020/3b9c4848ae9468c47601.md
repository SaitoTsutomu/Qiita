title: japanese-addressesを使ったジオコーディング
tags: Python GeoCoding geometry
url: https://qiita.com/SaitoTsutomu/items/3b9c4848ae9468c47601
created_at: 2020-08-24 22:00:14+09:00
updated_at: 2020-08-24 22:18:48+09:00
body:

## はじめに

「[Geolonia 住所データ | japanese-addresses](https://geolonia.github.io/japanese-addresses/)」で住所データと代表点の緯度経度が公開されました。

参考： [無料で使える「住所マスターデータ」公開、表記統一や緯度経度への変換に活用可能 - INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/1271/298/index.html)

このデータを使って、住所⇔緯度経度変換のコマンドを作ったので紹介します。
Python3.8が必要です。

## インストール＆設定

まず、上記サイトで「ダウンロード」からCSV（latest.csv）をダウンロードしてください。ダウンロードしたパスを「`/path/to/latest.csv`」とします。
下記コマンドを実行してください。

```
pip install simple-geocoding
python -c '__import__("simple_geocoding").Geocoding("/path/to/latest.csv")'
```

2つ目のコマンドでCSVから「住所リスト、KDTree、住所をキーとした緯度経度の辞書」を作成してインストール先にpickleで保存しています。

## 使い方

### 住所→緯度経度

```
simple-geocoding 東京都千代田区丸の内一丁目
>>>
(35.68156, 139.767201)
```

引数が1つのときは、住所とみなして、緯度経度に変換します。
これは、単純に住所をキーにした緯度経度を返しています。
なお、単純化のため同一の住所に対して複数の緯度経度が存在しても1つだけ返しています。

### 緯度経度→住所

```
simple-geocoding 35.68156 139.7672
>>>
東京都千代田区丸の内一丁目
```

引数が2つのときは、緯度と経度とみなして、住所に変換します。
これは、[KD-Tree](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html)で最寄りの登録地点を求めています。

## 補足

KD-Treeというデータ構造を使うことで、不均一に存在する地点を効率よく管理できます。
また、PythonではKD-Treeがscipyに含まれているので、簡単に利用できます。

参考
- [Kd木 - Wikipedia](https://ja.wikipedia.org/wiki/Kd木)
- [simple_geocoding/\_\_init__.py](https://github.com/SaitoTsutomu/simple-geocoding/blob/master/simple_geocoding/__init__.py)


