title: BlenderでPythonを実行する方法
tags: Python 3DCG 初心者 Blender
url: https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377
created_at: 2022-05-06 20:02:46+09:00
updated_at: 2025-04-27 11:50:49+09:00
body:

## 概要

Blenderの機能のいくつかは、Pythonを使って実行できます。
ここでは、Pythonコードを実行する4つの方法を紹介します。

1. BlenderのPythonコンソール
1. Blenderのテキストエディター
1. シェルからBlenderのコマンド
1. アドオン

## BlenderのPythonコンソール

Pythonコンソールは、ちょっとしたコードを実行するのに向いています。
Pythonコンソールを表示するには、BlenderのエディタータイプからPythonコンソールを選びます。

![a1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/be2bb8cc-fb40-1ef8-c366-7fc9a745752c.png)

### Scriptingワークスペース

Pythonコンソールは、Scriptingワークスペースで予め表示されています。ワークスペースに切り替えはヘッダーで可能です。Scriptingは、ワークスペースの一番右にあります。ワークスペースが切れている場合は、スクロールする必要があります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0cffdad9-65d8-db8c-337f-6826ae6f8bdd.png" width="500">

Pythonコンソールでは、`>>>`のプロンプトで、Pythonのコードを実行できます。
たとえば、下記のように`1 + 2`を入力して`Enter`を押すと`3`が返ります。

![スクリーンショット 2022-05-06 19.21.27.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d3c4716f-a135-5b3c-0f7c-c1db34970ba9.jpeg)

## Blenderのテキストエディター

テキストエディターは、ある程度まとまったコードを実行するのに向いています。また、Blenderファイル（`.blend`）を保存すると、テキストも一緒に保存されるので、コードを残しておきたいときに便利です。
テキストエディターを表示するには、Blenderのエディタータイプからテキストエディターを選びます。

![a2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bf12a029-c58a-abc5-0518-083e166cb79e.png)

なお、テキストエディターは、Scriptingワークスペースで予め表示されています。ワークスペースに切り替えはヘッダーで可能です。Scriptingは、ワークスペースの一番右にあります。ワークスペースが切れている場合は、スクロールする必要があります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0cffdad9-65d8-db8c-337f-6826ae6f8bdd.png" width="500">

### 新規テキスト

ヘッダーの`新規`を押して、新規テキストを作成できます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5267b85f-bdd6-92de-b41d-0e52b3847a4f.png" width="500">

キャレット（テキストの挿入位置を表す縦棒）が表示されるので、テキストを入力できます。
作成したテキストは、テキストメニューからファイルとして保存できます。

### 既存ファイルのテキスト

ヘッダーの`開く`を押して、既存ファイルを開けます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/74fa733b-d67f-23ac-508a-6ac33f3a2635.png" width="500">

### テキストの実行（スクリプト実行）

新規テキストと既存ファイルのテキストは、どちらも、テキストメニューの`スクリプト実行`で実行できます。
また、ヘッダーの`▶`を押してもスクリプトを実行できます。

![a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f8987d75-5be6-c178-2d23-f5afd5c7acba.png)

## シェルからBlenderのコマンド

BlenderのUIを使用せずにPythonコードだけ実行したい場合は、シェル（Windowsではコマンドプロンプト）からBlenderを実行する方法が便利です。Blenderをシェルから実行する場合、Pythonファイルを指定して実行できます。

詳しくは、記事「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」を参照してください。

## アドオン

特定の作法に従って、Pythonコードを記述することで、アドオンとして登録して実行することができます。
アドオンは、主にBlenderの機能を拡張したい場合に用います。

詳しくは、[ぬっち](https://qiita.com/nutti)さんの「[はじめてのBlenderアドオン開発](https://colorful-pico.net/introduction-to-addon-development-in-blender/2.8/)」が参考になります。

