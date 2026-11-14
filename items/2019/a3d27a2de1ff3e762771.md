title: Jupyter Notebookでカーネルを増やそう
tags: Python kernel Jupyter venv
url: https://qiita.com/SaitoTsutomu/items/a3d27a2de1ff3e762771
created_at: 2019-12-07 09:16:54+09:00
updated_at: 2019-12-09 08:54:57+09:00
body:

# はじめに
Jupyter NotebookでPythonを使っているときに、複数の仮想環境を扱う方法の紹介です。
※ コマンドは、macOSのものです。Windowsなどでは、記述方法が変わるのでご注意ください。

# カーネルの仮想環境を追加する

以下では、サンプルとしてPython3.8の仮想環境を追加します。
Python3.8は、`python3.8`コマンドで実行できるとします。未インストールの場合は、 
 https://www.python.org/downloads/ などからダウンロードしてインストールしましょう。

まずは、venv38という仮想環境を作成し、有効化します。別の仮想環境名を使用する場合は、以降のvenv38を適宜読み替えてください。

```
python3.8 -m venv venv38
source venv38/bin/activate
```

`pip install ...`で必要なライブラリーを適宜インストールしてください。

カーネルに仮想環境を追加します。

```
pip install ipykernel
python -m ipykernel install --name venv38
```

# 追加したカーネルの利用

jupyterは非仮想環境下で使うことにしましょう。一旦、`deactivate`で仮想環境を抜けます。

`jupyter-notebook`でJupyter Notebookを起動します。
右上の「New」から「venv38」を選ぶと、venv38の仮想環境で新規に始められます。

# 既存ノートブックのカーネルを変更する

まず、既存のノートブックを開いてください。
Jupyter NotebookのKernelメニューのChange kernelでカーネルを変更できます。
変更できると、右上のカーネルの表示が変わります。

# 追加したカーネルの確認

以降では、追加した仮想環境上での実行とします。

`jupyter kernelspec list`でカーネルとそのパスの一覧を確認できます。

# 追加した仮想環境を削除する

`jupyter kernelspec uninstall venv38`で、追加した仮想環境を削除できます。

# ライブラリを追加する

以降では、追加した仮想環境のJupyter Notebook上での実行とします。

たとえば、venv38に、NumPyのインストールを追加したいとしましょう。
通常ですと、`!pip install numpy`でできますが、このようにするとvenv38ではなく、本体にインストールされます。
Jupyter Notebookから仮想環境にインストールしたい場合は、以下のようにします。パスは上記で確認したパスではなく、最初に作成した仮想環境のパスです。

```
!source /path/to/venv38/bin/activate; pip install numpy
```

以上

