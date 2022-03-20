title: Jupyterの小技5
tags: Python Jupyter
url: https://qiita.com/SaitoTsutomu/items/5be28c10f6f30d1df6ec
created_at: 2017-05-18 09:31:20+09:00
updated_at: 2017-05-18 09:31:32+09:00
body:

# Jupyterの(マイナーな)マジックコマンド紹介
[Jupyterの小技4 - Qiita](http://qiita.com/SaitoTsutomu/items/34847c066880ebfdebf7)の続き

## %precision : 表示桁数設定

- 使用法1 `%precision` : デフォルトの設定を表示
- 使用法2 `%precision 3` : 小数点以下3桁表示に設定
- 使用法3 `%precision %08.3f` : 小数点以下3桁、全体で8桁、頭を0で埋めるように設定

## %bookmark, %cd, %pwd: ディレクトリ操作

### 使用例
c:\temp を workingdir(名称は任意可) ディレクトリとして登録

```py3:jupyter
%bookmark workingdir c:\temp
```

登録済み一覧表示

```py3:jupyter
%bookmark -l
>>>
Current bookmarks:
workingdir -> c:\temp
```

カレントディレクトリ表示

```py3:jupyter
%pwd
>>>
'C:\\Users\\tsutomu\\Documents'
```

登録したディレクトリに移動

```py3:jupyter
%cd workingdir
>>>
(bookmark:workingdir) -> c:\temp
c:\temp
```

元のディレクトリに戻る

```py3:jupyter
%cd -
>>>
C:\Users\tsutomu\Documents
```

ブックマーク削除

```py3:jupyter
%bookmark -d workingdir
```

全ブックマーク削除

```py3:jupyter
%bookmark -r
```

## 参考
[Built-in magic commands — IPython 3.2.1 documentation](https://ipython.org/ipython-doc/3/interactive/magics.html)

以上

