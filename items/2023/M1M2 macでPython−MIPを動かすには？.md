title: M1/M2 macでPython−MIPを動かすには？
tags: Python Mac 最適化 M1 python-mip
url: https://qiita.com/SaitoTsutomu/items/fbc33299e1906a238f53
created_at: 2023-11-15 21:13:55+09:00
updated_at: 2023-12-02 07:01:40+09:00
body:

## M1/M2でPython−MIPは動かない？

普通に実行すると、M1/M2 macでは数理最適化のライブラリである[Python−MIP](https://www.python-mip.com/)が動きません。
Python 3.12ではPython−MIPをインストールできないので、Python 3.11で動かないことを確かめてみます。

```sh
% python3.11 -V

Python 3.11.6
```

Python−MIPをインストールします。

```sh
% pip3.11 install mip

（中略）
Successfully installed cffi-1.15.1 mip-1.15.0 pycparser-2.21
```

インストールは成功します。モデルを作ってみましょう。

```sh
% python3.11 -c 'import mip; m = mip.Model()'

An error occurred while loading the CBC library:
（中略）'.../lib/python3.11/site-packages/mip/libraries/cbc-c-darwin-x86-64.dylib'
 (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64')),
（中略）
NameError: name 'cbclib' is not defined
```

エラーになりました。これは、Python−MIPと一緒にインストールされたソルバーのCBCのライブラリがx86_64のバイナリだからです。

## M1/M2でPython−MIPを動かす方法

CBCのライブラリを動かすためには、x86_64のエミュレータであるRosetta2が必要です。
Rosetta2を有効にするには、一度だけ次のようにします。

```sh
% /usr/sbin/softwareupdate --install-rosetta --agree-to-license
```

Rosetta2を有効にすると`arch`というコマンドが使えます。
`arch`を使うと、次のようにしてx86_64のzshを起動できます。

```sh
% arch --x86_64 zsh
```

これだけでは、まだ動きません。さらに仮想環境で作業する必要があります。
仮想環境を作成し、アクティベートしましょう。

```sh
% python3.11 -m venv venv
% . venv/bin/activate
```

Python−MIPをインストールします。

```sh
(venv) % pip install mip

（中略）
Successfully installed cffi-1.15.1 mip-1.15.0 pycparser-2.21
```

ここまですると、次のように動かすことができます。

```sh
(venv) % python -c 'import mip; m = mip.Model()'
```

## まとめ

M1/M2 macでPython−MIPを動かすには、次の作業が必要でした。

- Rosetta2を有効にします。
- x86_64でzshを起動します。
- 仮想環境で作業します。

## 余談

Python−MIPは、[CFFI](https://cffi.readthedocs.io/)のインターフェースを使っているため、まとめで紹介したような作業が必要でした。
似たようなライブラリである[PuLP](https://coin-or.github.io/pulp/)は、CBCを外部アプリケーションとして使っているので、Rosetta2を有効にするだけで使えます。

参考：[M1/M2でIntel用ライブラリを利用する手順 - PyQドキュメント](https://docs.pyq.jp/python/library/install_m1_mac.html)

以上




