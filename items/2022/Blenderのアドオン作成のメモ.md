title: Blenderのアドオン作成のメモ
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/6b8e6e734c99be6eeb5e
created_at: 2022-05-28 18:04:26+09:00
updated_at: 2022-07-23 19:54:50+09:00
body:

## 概要

Blenderのアドオンを作るときのメモです。

### 前提

- 作成するアドオンは、GitHubで管理します。
- Pythonコードは、Visual Studio Code（以降VSCode）で編集します。
- [WatchAddon](https://github.com/SaitoTsutomu/WatchAddon)アドオンを使って、アドオンファイルを保存すると機能が自動で有効になるようにします。

## 手順

### WatchAddonをBlenderにインストールする

[WatchAddon](https://github.com/SaitoTsutomu/WatchAddon)アドオンをインストールしておきます。アドオンを有効化するには、**テスト中**を選ぶ必要があります。
このアドオンをインストールすると、インストール済みの特定のアドオンを直積編集して保存すると自動で有効化されます。
これにより、開発中のアドオンのコードを変更し保存するだけで、開発中のアドオンの機能を確認できるようになります。

https://github.com/SaitoTsutomu/WatchAddon

### 作りたいものを決める

作成したいものを考えます。ここでは、「Blenderで開いている外部テキストを、VSCodeで開く機能」とします。コードで書くと以下になります。

```py
        for text in bpy.data.texts:
            if text.filepath:
                pth = Path(text.filepath)
                Popen(f"code {pth.name}", shell=True, cwd=pth.parent)
```

実行方法は、Scriptingワークスペースのテキストメニューとします。
アドオンの名前は、**OpenTextFile**にします。

### 元にするものを決める

作成済みのリポジトリーから機能が似ているものを探し、コピー元にします。なければ、空で作ります。
今回作成するものはメニューなので、メニューのアドオンの[**OpenURL**](https://github.com/SaitoTsutomu/OpenURL)を元にします。

- [OpenURL](https://github.com/SaitoTsutomu/OpenURL)のCodeから、クローン用のURLをコピーします。
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3cb8ecc8-f359-0752-59ae-59e8bdbe3dff.png" width="400">

- GitHubのページの右上の`+`の[**Import repository**](https://github.com/new/import)を選びます。[リンク]
- コピーしたURLを下記のように貼り付け、新しいリポジトリ名をOpenTextFileにし、**Begin import**を押します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d0be4399-2237-d26c-22a5-e9f9f1f87182.png" width="800">

- 下記のようになったら、OpenTextFileのリンクをクリックします。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5901d631-39fd-069e-fc46-023dbf881049.png" width="500">

### コピーしたアドオンを簡単に修正しインストールする

作成したOpenTextFileリポジトリのクローン用のURLをコピーします。
ここからコンソールで作業をします。

```sh
git clone コピーしたURL
cd OpenTextFile
code .
```

アドオン名、クラス名などは、はじめに正しいものに変えておきます。そこで、VSCoodeで下記を修正します。

- 全ファイルの`OpenURL`を`OpenTextFile`に一括変換します。
- `__init__.py`の`COU_OT_open_url`を`COT_OT_open_text_file`に一括変換します。
- 同ファイルの`bpy.types.VIEW3D_MT_object`を`bpy.types.TEXT_MT_text`に一括変換します。
- 同ファイルの`bl_idname`の行は、下記のように修正します。

```py
    bl_idname = "object.open_text_file"
```

- 修正箇所を確認してからコミットし、変更の同期をします。
- GitHubのOpenTextFileリポジトリに戻り、README.mdのInstallationのDownloadのリンクをクリックし、アドオンをダウンロードします。
- ダウンロードしたzipファイルは解凍せずに、そのままBlenderでアドオンとしてインストールします。今回、アドオンを`TESTING`で作成しているので、下記のように、**テスト中**を選択してチェックします。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/178620b9-9122-fd8b-f7bc-e29ac05b4d9f.png" width="600">

- Scriptingワークスペースのテキストメニューに、下記のように`Open URL`が追加されます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f17b81b9-ab22-15dd-8934-3a07b8d512e2.png" width="400">

### アドオンを完成させる

３Dビューポートのサイドバーの編集タブで下記のようにWatchAddonのaddonに`OpenTextFile`を指定します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a3b2b3e7-dbfe-bd4a-1415-34272ef61a6a.png" width="300">


上図の`Start`を押します。**インストールされたアドオンの__init__.py**が開きます。
下記のようにアドオンを完成させます。

```py
from pathlib import Path
from subprocess import Popen

import bpy

bl_info = {
    "name": "OpenTextFile",
    "author": "tsutomu",
    "version": (0, 1),
    "blender": (3, 1, 0),
    "support": "TESTING",
    "category": "Object",
    "description": "",
    "location": "View3D > Object",
    "warning": "",
    "doc_url": "https://github.com/SaitoTsutomu/OpenTextFile",
}


class COT_OT_open_text_file(bpy.types.Operator):
    bl_idname = "object.open_text_file"
    bl_label = "Open Text File"
    bl_description = "Open Text File"

    def execute(self, context):
        for text in bpy.data.texts:
            if text.filepath:
                pth = Path(text.filepath)
                Popen(f"code {pth.name}", shell=True, cwd=pth.parent)
        return {"FINISHED"}


def draw_item(self, context):
    self.layout.operator(COT_OT_open_text_file.bl_idname)


def register():
    bpy.utils.register_class(COT_OT_open_text_file)
    bpy.types.TEXT_MT_text.append(draw_item)


def unregister():
    bpy.utils.unregister_class(COT_OT_open_text_file)
    bpy.types.TEXT_MT_text.remove(draw_item)
```

ファイルを保存すると、インストール済みのアドオンに反映されます。
Scriptingワークスペースのテキストエディターでファイルを適当に開き、`Open Text File`でVSCodeが起動するのを確認します。

### アドオンをGitHubに反映する

機能確認できたら、**完成したコードをGitHubで管理しているコードにコピー**してGitHubにコミットして完成です。

なお、今回作成したOpenTextFileアドオンは説明用なので、記事投稿時にリポジトリは削除しています。

以上



