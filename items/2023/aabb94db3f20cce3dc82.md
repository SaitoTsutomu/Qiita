title: M1/M2 macのarm64シェルでPython−MIPを動かすには？
tags: Python Mac 最適化 M1 Poetry
url: https://qiita.com/SaitoTsutomu/items/aabb94db3f20cce3dc82
created_at: 2023-12-12 20:03:53+09:00
updated_at: 2023-12-12 20:22:39+09:00
body:

## 概要

この記事は、下記の続編です。「arm64のシェルでx86_64のPythonを動かす方法」を説明します。

https://qiita.com/SaitoTsutomu/items/fbc33299e1906a238f53

上記の記事では、**x86_64のzsh**上で、x86_64でしか動かないPython−MIPを稼働させました。
しかし、ときには**arm64のzsh**上で、x86_64のPythonを動かしたい場合もあるでしょう。たとえば、PoetryでPython−MIPを動かしたい場合があたります。

## 前提条件

Rosetteを有効化してください。

Python 3.11を使います。
Python 3.11は、[公式サイト](https://www.python.org/downloads/macos/)の`macOS 64-bit universal2 installer`版をインストールされている必要があります。

また、下記のようにPoetryをインストールしているとします（`%`はシェルのプロンプトです）。
```zsh:zsh
% curl -sSL https://install.python-poetry.org | python3 -
```

さらに、プロジェクト内に仮想環境を作成するように設定します。

```zsh:zsh
% poetry config --local virtualenvs.in-project true
```

## PoetryでPython−MIPを動かすには

ここからは、実際に実行しながら説明します。前提のようにPoetryをインストールすると、下記のようにx86_64上ではPoetryが動きません。

```zsh:zsh
% arch --x86_64 poetry
Traceback (most recent call last):
（中略）
(mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64'))
```

本記事では、arm64上のシェルで、Poetryを使ってPython−MIPを動かすことがゴールになります。まずは、Poetryの新規プロジェクトを作成します。

```zsh:zsh
# arm64の確認
% uname -m
arm64
# Poetryの新規プロジェクト作成
% poetry new sample
Created package sample in sample
% cd sample
```

Poetryで仮想環境を作成するには`poetry install`としますが、この方法ではうまくいきません。次のように、仮想環境を作成する必要があります。

```zsh:zsh
% python3.11-intel64 -m venv venv .venv
```

`python3.11-intel64`は、x86_64版のPythonです。これで、x86_64版のPythonの仮想環境が作成されればいいのですが、作成されません。そこで、次のように自前で修正します。

```zsh:zsh
% cd .venv/bin
% rm python*
% ln -s python3.11-intel64 python
% ln -s python3.11-intel64 python3
% ln -s python3.11-intel64 python3.11
% ln -s /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11-intel64
% cd ../..
```

これで、Poetryの仮想環境がx86_64になります。

続いて、pyproject.tomlを次のように修正してください。

```toml:pyproject.toml
[tool.poetry.dependencies]
python = "^3.11"

↓

[tool.poetry.dependencies]
python = "~3.11"
```

`^3.11`は、`>=3.11.0 <4.0.0`を意味してますが、この範囲に対応するPython−MIPのバージョンは存在しません。
`~3.11`とするとことで、`>=3.11.0 <3.12.0`の範囲になり、Python−MIPの`1.15.0`が対応します。

下記のようにPython−MIPをインストールしましょう。

```zsh:zsh
% poetry add mip
```

ここまでくると、PoetryでPython−MIPを実行できます。

```zsh:zsh
% poetry run python -c 'import mip; m = mip.Model()'
```

## x86_64の仮想環境を作成するには（まとめに変えて）

arm64シェルでx86_64のPythonを動かす仮想環境（`.venv`）を作成するには、次のようにします。

```zsh:zsh
% python3.11-intel64 -m venv venv .venv
% cd .venv/bin
% rm python*
% ln -s python3.11-intel64 python
% ln -s python3.11-intel64 python3
% ln -s python3.11-intel64 python3.11
% ln -s /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11-intel64
% cd ../..
```

アクティベートは、通常通りにできます。

```zsh:zsh
% source .venv/bin/activate
```

なお、`.venv`は、`venv`などの他の名前に変更できます。

以上

