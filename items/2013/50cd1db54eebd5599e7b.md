title: クラスにバインディングしてYAMLの読み書き
tags: Python C# YAML
url: https://qiita.com/SaitoTsutomu/items/50cd1db54eebd5599e7b
created_at: 2013-01-24 14:20:23+09:00
updated_at: 2013-01-24 14:49:26+09:00
body:

ツリー構造かつオブジェクト参照のあるデータ構造をYAML形式でファイルに入出力する[サンプル](https://github.com/Tsutomu-KKE/YamlTest)です。
同じ[YAMLファイル](https://github.com/Tsutomu-KKE/YamlTest/blob/master/test.yml)をC#およびPythonから読んでいます。

* Company クラスが Employee のリストと Group のリストを持っている
* Group クラスが Employee を持っている
* test.yml の Company オブジェクトは、Employees[0] と Groups[0].Employees[0] が同じデータとなっている。
