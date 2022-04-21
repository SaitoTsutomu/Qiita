title: Blenderで平面を本のページのように動かす
tags: 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/150d553f6b2154d3b611
created_at: 2022-04-16 09:46:19+09:00
updated_at: 2022-04-16 19:22:35+09:00
body:


## 概要

下図のような動きをするアーマチュアを作成する方法の紹介です。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/44bde698-9363-76cc-56c0-3779b34f4dd0.gif" width="300">


- 平面は4分割しています。
- 分割と直角に、縦にボーンが4つあります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/26f70ef2-d439-3d64-36b1-4909bae6a8d6.jpeg" width="160">

- 4つのボーンは、全て親です（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2e5f1970-f097-07f9-5ec1-6815d52193a9.jpeg" width="180">

- `Bone4`、`Bone3`、`Bone2`、`Bone1`の長さの比は、`4:3:2:1`です。
- `Bone4`を`x`度回転すると、`Bone3`を`0.8 * x`度回転させます。
- `Bone3`を`x`度回転すると、`Bone2`を`0.8 * x`度回転させます。
- `Bone2`を`x`度回転すると、`Bone1`を`0.8 * x`度回転させます。

## 手順

- ページの元になる平面（`Plane`）を作成
  - `Shift + A`（追加）→メッシュ→平面
- `Tab`で編集モードに
- サイズを2倍に
  - `S2`、`Enter`
- クリースの設定（サブディビジョンサーフェスで変わらないように）
  - `Shift + E`、`1`、`Enter`
- 立てる
  - `RX90`、`Enter`
- 上に移動
  - `GZ2`、`Enter`
- 下図のようにループカット
  - マウスを縦の辺のところで、`Ctrl + R`、`3`、`Enter`、`Enter`

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3caacccd-b85b-a127-b322-62b6f0c3ec00.jpeg" width="180">


- `Tab`でオブジェクトモードに
- 右クリックでスムーズシェード
- 下図のようにモディファイアープロパティでサブディビジョンサーフェスを追加し、ビューポートのレベル数を2に

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0cc2830f-11b6-c214-a459-65f5e013e37a.jpeg" width="300">

- `テンキーの1`（ビューメニュー→視点→前）
- アーマチュア（`Armature`）の追加
  - `Shift + A`（追加）→アーマチュア
- `Tab`で編集モードに
- ボーンの長さを4に
  - ボーンの上を選択し、`GZ3`、`Enter`
- ボーンプロパティで、ボーンの名前を`Bone4`に

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/27d2a5a3-d07b-dad1-cef7-e6f47e1065f1.jpeg" width="300">

- 透過表示に
  - `Shift + Z`
- ボーン追加
  - `Bone4`の下を選択し、`EZ3`、`Enter`
  - ボーンプロパティで、ボーンの名前を`Bone3`に
- ボーン追加
  - `Bone4`の下を選択し、`EZ2`、`Enter`
  - ボーンプロパティで、ボーンの名前を`Bone2`に
- ボーン追加
  - `Bone4`の下を選択し、`EZ1`、`Enter`
  - ボーンプロパティで、ボーンの名前を`Bone1`に
- 透過表示オフ
  - `Shift + Z`

- アウトライナーは下図のように

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3c83f90b-0a56-8bd4-9b6a-8e11ea262f1f.jpeg" width="180">

- `Tab`でオブジェクトモードに
- 親子づけ
  - Armatureを選択し、`A`（すべて選択）、`Ctrl + P`（ペアレント）→空のグループで
- 以降からウェイトづけ
- Planeを選択し、ウェイトペイントモードに
- オブジェクトデータプロパティの頂点グループで`Bone4`を選択し、下図のように1番上の辺のウェイトを1に

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/580cf6d9-a3b1-f91e-58d7-2ca1c0313b83.jpeg" width="500">

- 同様に`Bone3`を選択し、上から2番目の辺のウェイトを1に
- 同様に`Bone2`を選択し、上から3番目の辺のウェイトを1に
- 同様に`Bone1`を選択し、上から4番目の辺のウェイトを1に
- オブジェクトモードに
- Armatureを選択し、`Ctrl + Tab`でポーズモードに
- `N`（サイドバー）で、サイドバーを表示
- 以降からボーンにドライバを設定
- アウトライナーで、下図のように`Bone4`を選択

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3c83f90b-0a56-8bd4-9b6a-8e11ea262f1f.jpeg" width="180">

- サイドバーを下図のように
  - XYZオイラー角
  - 回転のYとZをロック

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/b5fbd489-7e5e-69be-5d4d-c75bab37df3f.jpeg" width="240">

- 回転のXで右クリックし「新規ドライバーとしてコピー」
- アウトライナーで、`Bone3`を選択
- XYZオイラー角
- 回転のXで右クリックし「ドライバーを貼り付け」
- 回転のXで右クリックし「ドライバーを編集」
- 下図のように編集
  - タイプをスクリプト型の式に
  - 式を`rotation_euler * 0.8`に

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/41cf81dd-5356-cd0f-234b-b8b99b4b9a6a.jpeg" width="240">

- 回転のXで右クリックし「新規ドライバーとしてコピー」
- アウトライナーで、`Bone2`を選択
- XYZオイラー角
- `Bone3`と同様に、回転のXで「ドライバーを貼り付け」て「ドライバーを編集」
  - タイプをスクリプト型の式に
  - 式を`rotation_euler * 0.8`に
- 回転のXで右クリックし「新規ドライバーとしてコピー」
- アウトライナーで、`Bone1`を選択
- XYZオイラー角
- `Bone3`と同様に、回転のXで「ドライバーを貼り付け」て「ドライバーを編集」
  - タイプをスクリプト型の式に
  - 式を`rotation_euler * 0.8`に
- 確認
  - `Bone4`を選択し、`R`（回転）で回転してみましょう。曲面になって曲がります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/16493977-b34e-d666-8afe-5cc11477cc55.jpeg" width="240">

以上

