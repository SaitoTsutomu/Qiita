title: AnacondaのJupyter notebookでipywidgtesのエラーの対処法
tags: Python Jupyter Anaconda ipywidgets
url: https://qiita.com/SaitoTsutomu/items/192109ce96ac23d4db7d
created_at: 2017-09-21 16:37:16+09:00
updated_at: 2017-09-21 16:43:40+09:00
body:

# これなに

例えば、下記のように ipywidgets を使おうとしてエラーになった場合の対処方法です。

```py3:jupyter
import ipywidgets.widgets as iw
iw.Button(value='test')
```

```:エラーメッセージ
Widget Javascript not detected.  It may not be installed or enabled properly.

Error rendering Jupyter widget. Widget not found: ...
```

Anaconda で、 ipywidgets==6.0.0, widgetsnbextension==3.0.2 の環境でエラーになりました。
下記の解決方法のいずれかで直りました。

# 解決方法その1

- conda-forge を使う。→ ipywidgets が 7.0.1 でなります。

```shell-session:shell
    conda install -y -c conda-forge ipywidgets
    jupyter nbextension enable --py widgetsnbextension
```

# 解決方法その2

- pip で入れる。→ ipywidgets が 7.0.1 でなります。

```shell-session:shell
    conda uninstall -y widgetsnbextension
    pip install ipywidgets widgetsnbextension
```

# 解決方法その3

- conda で古いのを入れる。→ ipywidgets が 6.0.0 でなります。

```shell-session:shell
    conda install -y ipywidgets=6 widgetsnbextension=2
```

おそらく、現在の Anaconda の組合せが間違っているのかと思います。すぐ直ると思いますが。

ipywidgets|widgetsnbextension|可否
:--|:--|:--
7.0|3.0|OK
6.0|2.0|OK
6.0|3.0|NG ← 現在の最新状態(conda update --all)

以上

