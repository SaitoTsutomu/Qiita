title: macOSのBlenderでシステムコンソールを出す方法
tags: Mac tips Blender
url: https://qiita.com/SaitoTsutomu/items/38ac3077713cf10ce385
created_at: 2023-08-27 20:10:32+09:00
updated_at: 2025-02-22 00:20:22+09:00
body:

## 背景

Windowsであれば、Blenderの`ウィンドウ`メニューの`システムコンソール切替え`でBlenderのコンソール画面を出せますが、macOSのBlenderにはこのメニューがありません。

macOSでは、先にターミナル画面を開いておいて次のようにコマンドを実行すると、そのターミナル画面がコンソール画面の代わりになります。

```sh
/Applications/Blender.app/Contents/MacOS/Blender
```

## やりたいこと

- macOSでターミナル画面が開くBlenderアプリケーション（以降ではBlenderConsole.app）の作成

## アプリケーションの構成

背景で説明したコマンドをアプリケーションにするには、下記の構成でファイルを作成します（括弧内は内容です）。BlenderConsoleがアプリケーション名です。

* BlenderConsole.app
    * Contents
        * Info.plist（設定ファイル）
        * MacOS
            * blender.sh（コマンドのスクリプト）
        * Resources
            * blender icon.icns（アイコン）

`BlenderConsole.app`は、どこに置いてもよいですが、今回は、`/Applications`に置きます。

## BlenderConsole.appの作成

Blender本体がインストールされている状態で、管理者権限のあるユーザのシェルで次を実行してください。

```sh
mkdir -p /Applications/BlenderConsole.app/Contents/{MacOS,Resources}
cp /Applications/Blender.app/Contents/Resources/blender_icon.icns \
   /Applications/BlenderConsole.app/Contents/Resources/

cat << EOF >> /Applications/BlenderConsole.app/Contents/Info.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>blender.sh</string>
    <key>CFBundleIconFile</key>
    <string>blender_icon</string>
</dict>
</plist>
EOF

cat << EOF >> /Applications/BlenderConsole.app/Contents/MacOS/blender.sh
#!/bin/bash
open /Applications/Blender.app/Contents/MacOS/Blender
EOF

chmod +x /Applications/BlenderConsole.app/Contents/MacOS/blender.sh
```

アプリケーションフォルダのBlenderConsoleでターミナル画面が開くBlenderを実行できます。

※　実行は自己責任でお願いします。

## ターミナル画面を自動で消すための設定

BlenderConsoleを実行すると、ターミナル画面と一緒にBlenderが起動します。しかし、Blender終了時にターミナル画面が残ってしまいます。手動で消してもよいですが、次のようにすると自動で消えるようになります。

- ターミナルを起動している状態で、ターミナルメニューの設定（⌘＋，）で設定画面を開く
- プロファイルタブの`シェルの終了時`を`シェルが正常に終了した場合は閉じる`にする

## Dockに追加

アプリケーションフォルダのBlenderConsoleをDockにドラッグしてください。

## BlenderConsole.appの内容の確認

アプリケーションフォルダのBlenderConsoleを右クリックして`パッケージの内容を表示`を選んでください。

## BlenderConsole.appの削除

アプリケーションフォルダのBlenderConsoleを削除してください。

以上


