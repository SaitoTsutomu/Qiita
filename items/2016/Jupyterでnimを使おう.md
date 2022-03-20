title: Jupyterでnimを使おう
tags: Python Docker Jupyter Nim
url: https://qiita.com/SaitoTsutomu/items/f79257430e2d8fcb9196
created_at: 2016-03-25 00:05:44+09:00
updated_at: 2016-03-25 00:05:44+09:00
body:

# <i class='fa fa-circle'> nimを使おう

[nim速いみたい](http://h-miyako.hatenablog.com/entry/2015/01/23/060000)だし、Pythonに似ているらしいので、試してみましょう。
[Jupyterのカーネル](https://github.com/ipython/ipython/wiki/IPython-kernels-for-other-languages)は、、、ない。
[dockerで作りました](https://hub.docker.com/r/tsutomu7/nim/)。

# <i class='fa fa-circle'> 実行方法

dockerのインストールは、[Install Docker Engine](https://docs.docker.com/engine/installation/)を見てください。

下記を実行すると、Jupyterが起動します。

```bash:bash
docker run -it --rm -p 8888:8888 tsutomu7/nim
```

ブラウザで「dockerホストのIPアドレス:8888」を開いてください。
右上の”New"から"nim"を選んでください。

# <i class='fa fa-circle'> 説明
セルにnimのプログラムを書いて、Shift+Enterで実行できます。

```nim:nim
echo "Hello world!"
>>>
Hello world!
```

「?」でコマンド一覧が出ます。

```nim:nim
?
>>>
?
!command
%run file
%time ...
%def ...
%inc ...
%web
```

「!」で始めるとシェルのコマンドを実行できます。

```nim:nim
!echo 'echo "OK"' >> test.nim
```

「%run [オプション] ファイル名」でファイルを実行できます。

```nim:nim
%run test
>>>
OK
```

```nim:nim
%run --opt:size test
>>>
OK
```

「%time [オプション]」で実行時間を計測できます。

```nim:nim
%time
echo "OK?"
>>>
OK?
real	0m 0.00s
user	0m 0.00s
sys 	0m 0.00s
```

「%def 名称」でプログラムファイルを作成できます。

```nim:nim
%def hello
proc Hello(): string = "Hello!"
>>>
Created hello.nim
```

```nim:nim
%def world
proc World(): string = "World!"
>>>
Created world.nim
```

「%inc 名称1 名称2 …」でファイルを取り込んで実行できます。

```nim:nim
%inc hello world
echo Hello() & World()
>>>
Hello!World!
```

「%web」でドキュメントのURLを表示します。

```nim:nim
%web
>>>
http://nim-lang.org/documentation.html
```

参考

- ドキュメント http://nim-lang.org/documentation.html
- チュートリアル等 http://nim-lang.org/learn.html
- gistサンプル https://gist.github.com/miyakogi/b1df00c8bc99927d9d0d

以上

