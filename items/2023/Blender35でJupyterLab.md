title: Blender3.5でJupyterLab
tags: Python Blender JupyterLab
url: https://qiita.com/SaitoTsutomu/items/481f3dc6b0d4bf98b9d9
created_at: 2023-04-01 16:43:42+09:00
updated_at: 2023-04-01 21:39:10+09:00
body:

## 概要

Blender 3.5が出たので、JupyterLabが動くか確認してみました。macOSで試してますが、他のOSでもできると思います。

Blender 3.5とPython 3.10はインストール済みとします。

https://www.blender.org/

## JupyterLabの準備

Pythonは、3.10.9です。

```sh:bash
python -V
```

```test:ouput
Python 3.10.9
```

JupyterLabをインストールしておいてください。

```sh:bash
pip install jupyterlab
```

## blenderカーネルの準備

blenderカーネル用の仮想環境を作成します。

```sh:bash
python -m venv venv
```

アクティベートします。

```sh:bash
. venv/bin/activate
```

ライブラリーをインストールします。

```sh:bash
pip install blender-notebook
```

Blenderのカーネルを追加します。
```sh:bash
blender_notebook install --blender-exec /Applications/Blender.app/Contents/MacOS/Blender
```

下記のように出ましたが、気にせずに「y」とします。

```test:ouput
Current python interpreter version is not 3.7!
blender_notebook will link pip packages installed in this interpreter to the 
blender embedded python interpreter. Mismatch in python version might cause
problem launching the jupyter kernel. Are you sure to continue?
 [y/N]: y
```

これでカーネルの準備は終わりです。お手軽ですね。

### カーネルの削除（Jupyterでblenderを使わなくなったとき）

カーネルが不要になったら下記のようにして削除できます。

```sh:bash
blender_notebook remove --kernel-name blender
```

カーネルの一覧は下記で確認できます。

```sh:bash
jupyter kernelspec list
```

### 参考

https://qiita.com/odu_beyond/items/8bfb73bc24e8014e0903

## JupyterLabの実行

JupyterLabを起動します。このとき、「blenderカーネル用の仮想環境」をアクティベートしている必要はありません。

```sh:bash
jupyter lab
```

新規作成でNotebookの「Blender」を選びます。
Blenderが起動します。

Notebookのセルに下記を書くと、モンキーが作成されます。

```py:jupyterlab
import bpy

bpy.ops.mesh.primitive_monkey_add()
```

単にBlenderを終了しても、自動でBlenderが再起動します。Blenderを終了したいときは、ノートブックのカーネルをシャットダウンしてください。なお、必要ならシャットダウンの前にBlenderのファイルを保存しておいてください。


### 参考

https://qiita.com/SaitoTsutomu/items/854c826bfc65ecae31f9

以上

