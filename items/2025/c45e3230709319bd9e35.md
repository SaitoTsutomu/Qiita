title: macのBlenderのPythonにパッケージをインストールする方法
tags: Python Mac インストール Blender
url: https://qiita.com/SaitoTsutomu/items/c45e3230709319bd9e35
created_at: 2025-02-23 09:39:10+09:00
updated_at: 2025-02-23 09:47:00+09:00
body:

## 概要

macOS Sequoia 15.3.1の[Blender](https://www.blender.org/)4.3に、何らかのパッケージをインストールする方法を紹介します。

## インストール

ここでは、例として`more-itertools`をインストールします。

最初にキー入力の手間を省くため、インストール先のシンボリックリンクを作成します。

```sh:zsh
cd
ln -s Library/Application\ Support/Blender/4.3/scripts/addons
```

`ls -H addons`でインストール済みのアドオンを確認できます。
今回の方法は、アドオンと同じ場所にパッケージをインストールします。

インストールは次のようにします。

```sh:zsh
pip3 install more-itertools -t addons
```

次のように確認してみましょう。

```sh:zsh
pip3 list --path addons
```

```output:出力
Package        Version
-------------- -------
more-itertools 10.6.0
```

Blenderを起動して、Scriptingワークスペースで、`import more_itertools`でインポートできることを確認してみましょう。

## アンインストール

アンインストールするには、次のようにフォルダを直接削除してください。

```sh:zsh
rm -r addons/more_itertools
rm -r addons/more_itertools-10.6.0.dist-info
```

なお、作業が終わったら、シンボリックリンクは削除してください。

```sh:zsh
rm addons
```

## pip3についての補足

`pip3`は、macOSにプリインストールされているPython3.9用のものです。
BlenderのPythonとは別物ですが、今回は問題なく使えたので利用しています。

もし、BlenderのPythonのpipを利用したい場合は、`pip3`の代わりに下記を使ってください。

```
/Applications/Blender.app/Contents/Resources/4.3/python/bin/python3.11 -m pip
```

## addonsフォルダを使う理由

BlenderのPythonでインポートできるパッケージの場所は、次のように確認できます。

```python:BlenderのScriptingワークスペース
import sys
sys.path
```

```output:出力（改行を追加）
[
    '/Applications/Blender.app/Contents/Resources/4.3/scripts/startup',
    '/Applications/Blender.app/Contents/Resources/4.3/scripts/modules',
    '/Applications/Blender.app/Contents/Resources/4.3/python/lib/python311.zip',
    '/Applications/Blender.app/Contents/Resources/4.3/python/lib/python3.11',
    '/Applications/Blender.app/Contents/Resources/4.3/python/lib/python3.11/lib-dynload',
    '/Applications/Blender.app/Contents/Resources/4.3/python/lib/python3.11/site-packages',
    '/Applications/Blender.app/Contents/Resources/4.3/scripts/freestyle/modules',
    '/Users/Your Name/Library/Application Support/Blender/4.3/scripts/addons/modules',
    '/Applications/Blender.app/Contents/Resources/4.3/scripts/addons_core',
    '/Users/Your Name/Library/Application Support/Blender/4.3/scripts/addons'
]
```

この中のどれかにインストールすれば使えることになります。
しかし、`/Applications`以下のフォルダはSIP（System Integrity Protection）で保護されているので、今回はユーザーのフォルダのaddonsを使いました。

単純に`pip3 install`すると、通常のインストール先（`/Applications`以下）にインストールできず、次の1行目のようにメッセージがでて、別の場所に正常にインストールされます。しかし、そのインストール先は`sys.path`にないので、インストールしてもBlenderで使うことはできませんので、注意してください。

```output:出力
Defaulting to user installation because normal site-packages is not writeable
Collecting more-itertools
...（中略）
Successfully installed more-itertools-10.6.0
```

以上

