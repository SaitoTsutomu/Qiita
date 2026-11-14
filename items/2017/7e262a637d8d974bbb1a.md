title: Bash in Jupyter
tags: Python Bash Jupyter
url: https://qiita.com/SaitoTsutomu/items/7e262a637d8d974bbb1a
created_at: 2017-02-28 10:44:03+09:00
updated_at: 2017-02-28 10:44:03+09:00
body:

# WindowsでLinuxのコマンドを使う方法
[Bash on Ubuntu on Windows](https://msdn.microsoft.com/ja-jp/commandline/wsl/about) や [Mingw](https://ja.wikipedia.org/wiki/MinGW) や [Cygwin](https://ja.wikipedia.org/wiki/Cygwin) や [Git](https://ja.wikipedia.org/wiki/Git)をインストールすれば、Windowsでも Linux のコマンドの一部を使えるようになります。

[Jupyter](http://jupyter.org/)からも、シェルのコマンドを簡単に使えるようです。例えば、Gitをインストールしていると、下記のように表示されます。

```py3:jupyter_notebook
%%bash
ls /
>>>
ReleaseNotes.html
bin
cmd
dev
etc
git-bash.exe
git-cmd.exe
mingw64
proc
tmp
unins000.dat
unins000.exe
usr
```

使えるコマンドは、"C:\Program Files\Git\usr\bin"などにありました。

Pythonを書きながら、ちょっと grep や sed や xargs などを使いたいときには、便利かもしれません。

以上

