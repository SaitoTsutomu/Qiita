title: Blenderでメッシュの3つの重心を確認する
tags: 3DCG Blender 数学
url: https://qiita.com/SaitoTsutomu/items/8db78f28033ccd8f44c2
created_at: 2022-09-14 23:39:40+09:00
updated_at: 2022-09-15 08:03:22+09:00
body:

## 概要

メッシュには、3つの重心があります。

- **ジオメトリ**：頂点に質点があると仮定したときの重心。頂点座標の平均。
- **重心（サーフェス）**：面に質量があると仮定したときの重心。
- **重心（ボリューム）**：密度が一定と仮定したときの重心。いわゆる重心。

実際にメッシュを作って、確認してみます。

## 重心の求め方

Blenderでは、以下のようにしてメッシュの重心を確認できます。
まず最初に、オブジェクトメニューの適用の**全トランスフォーム**で、回転とスケールをリセットしておいてください。
それぞれの重心は、下記操作後に、サイドバーのアイテムのトランスフォームの**位置**で確認できます。

- ジオメトリ：オブジェクトメニューの原点を設定の**原点をジオメトリに移動**
- 重心（サーフェス）：オブジェクトメニューの原点を設定の**原点を重心に移動（サーフェス）**
- 重心（ボリューム）：オブジェクトメニューの原点を設定の**原点を重心に移動（ボリューム）**


## 三角錐の場合

三角錐では、ジオメトリと重心（ボリューム）が同じになります。
適当な三角錐を作って確認します。

| ジオメトリ | 重心（ボリューム） |
|--:|--|
|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a1050e82-5d73-afff-ac37-dacc2d5b7254.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/740e354d-2ef3-4c3f-8c34-18b197cb3ef1.png)|

## 四角錐の場合

四角錐では、重心（ボリューム）は、高さの1/4のところにあります。
頂点を4にして円錐を作って確認します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/7e93bf2b-08ce-b239-911d-4b34c6a4c8a7.png" width="400">

各頂点は下記の通りです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5248ea88-89db-ba57-9997-ff3192c6fb0e.png" width="400">

ジオメトリは下記の通りです。平均になっています。
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0abe09ae-84b0-3229-6801-2aae606e9233.png" width="400">

重心（ボリューム）は下記の通りです。Zが高さの1/4になっています。
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/7e00806c-f321-f0c3-a5a9-69f609449f89.png" width="400">

## 三角形の場合

三角形では、ジオメトリと重心（サーフェス）は同じです。
平面を作り、頂点を1つ削って確認します。

各頂点は下記の通りです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/86f7ce11-2a6d-c697-e024-b312aa1b9ab7.png" width="400">

ジオメトリは、平均になります。重心（サーフェス）も同じです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/cacbdf50-d320-2620-7fc8-89a063d915db.png" width="400">

### 1辺の頂点を増やした場合

三角形の下辺を100個に細分化し、頂点を増やしてみましょう。見た目は三角形ですが、101角形になっています。
ジオメトリは、下辺の中心に近くなります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ff550d94-1b01-2f00-841b-edc651d61a7d.png" width="400">

101角形になっても面の形状は三角形と同じなので、重心（サーフェス）は変わりません。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/cacbdf50-d320-2620-7fc8-89a063d915db.png" width="400">

### 1つの頂点にベベルをかけた場合

三角形の左下の頂点にベベルを書けてみましょう。形状は三角形に近いですが、原点付近に頂点が99個あります。

ジオメトリは、原点付近になります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/69c3fdc2-2e8b-0f54-15b8-bd0ea3bf3ace.png" width="400">

形状は三角形に近いので、重心（サーフェス）は三角形のときに近いです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/535b6873-c78b-0a4d-1d54-db2b0ef56fe6.png" width="400">

以上






