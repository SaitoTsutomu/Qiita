title: Qiitaの投稿をGitHubにバックアップ
tags: Python Windows GitHub QiitaAPI
url: https://qiita.com/SaitoTsutomu/items/a2120058108593318a5b
created_at: 2013-01-07 22:59:21+09:00
updated_at: 2013-01-07 22:59:21+09:00
body:

[元記事](http://qiita.com/items/a98dffc4b1ad095898b1)を参考に、Pythonに移植
##使い方

+ [GitHub](https://github.com/)のアカウントを作成してください
+ [GitHub for Windows](http://windows.github.com/)とPythonをインストールしてください
+ GitHub for Windowsを起動して、新規リポジトリ`Qiita`作成
+ [update.py](https://github.com/Tsutomu-KKE/Qiita/blob/master/update.py)をリポジトリに追加し、中身の`user`を自分のidに書き換え
+ GitHub for WindowsでQiitaを開きtoolsメニューの`open a shell here`でGit Shellを起動し、`python update.py`を実行
