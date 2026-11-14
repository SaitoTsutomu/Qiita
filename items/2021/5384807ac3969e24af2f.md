title: Blenderチャレンジ：星マークのボール
tags: 3DCG Blender クイズ Blenderチャレンジ
url: https://qiita.com/SaitoTsutomu/items/5384807ac3969e24af2f
created_at: 2021-12-20 21:14:16+09:00
updated_at: 2021-12-22 20:33:34+09:00
body:

3DCGソフトウェアのBlenderを使って、お題のモデルを作成してみましょう。
やり方は一通りではないと思います。あなたは、どんな方法を考えますか？

## 問題

以下のようなオブジェクトを作ってください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/228ab794-7b0a-b732-8665-4f9144242f3b.jpeg" width="480">

[完成物をSketchfabで見る](https://skfb.ly/orXxP)

…
…
…

OK？

---

## 解答例

作成する手順です。macOSのキーを書いています。Windowsの場合は、`Option`を`Alt`に読み替えてください。

- `Shift + A`（追加メニュー）の「メッシュ」の「ICO球」を選びます。
  - 画面左下の詳細設定で、「細分化」を`3`にします。
- スムーズシェードをかけます。
- `[Tab]`で編集モードに入ります。
- 面選択モードにします。
- テンキーの`3`を押し（テンキーがない場合は、ビューメニューの「視点」の「右」を選び）、下図のように中心のすぐ下の三角を選択します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/aaaf06be-ca29-cc85-c078-22e921d7dc70.png" width="300">

- `Shift + G`（類似選択メニュー）の「エリア」を選びます。
  - 画面左下の詳細設定で、「しきい値」を`0.001`にします。
- `M`（マージ）の「束ねる」を選びます。
- 下図のように2つの三角を選びます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ab72d713-6d7f-8a0e-0ea0-8b14170a63a9.png" width="300">

- `Shift + G`（類似選択メニュー）の「エリア」を選びます。
- マテリアルを2つ作り、2つ目を黒にし、「割り当て」をします。
- サブディビジョンサーフェスモディファイアーを追加し、「シンプル」にし、「ビューポートのレベル数」を`2`にします。
- キャストモディファイアーを追加し、「係数」を`1`にします。
- 完成です。`[Tab]`でオブジェクトモードに戻り確認しましょう。

以上

