title: Windows の Git Shell で vim を使う
tags: Vim Windows GitHub
url: https://qiita.com/SaitoTsutomu/items/e7b441592c2f1ced4a3b
created_at: 2013-01-04 19:04:55+09:00
updated_at: 2013-01-04 19:04:55+09:00
body:

[GitHub for Windows](http://windows.github.com/)を導入すると、Git Shellが使えます。
ここで多くの Unixライクなコマンドが使えます。vim も入っていますが、単に vim しても実行できませんが、下記のように設定すると使えるようになります。

+ Git Shell は PowerShell にしておきます。(デフォルト)
+ Git Shell を起動し、下記を実行します。
+ `mkdir $(Get-ChildItem $profile).DirectoryName`
+ `echo 'function vim {sh vim $args}' > $profile`
+ いったん、終了します。

次回の起動から、vim が使えるようになります。(viでも 同様にできます)

+ 既にプロファイルを作成済みの場合は、echoの内容を追記してください。
+ Unicodeで作成されるのがいやならば、別途メモ帳などで作成してください。
