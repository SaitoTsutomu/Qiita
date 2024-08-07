title: Blenderの新機能：Node Toolsとは？
tags: 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/8c39e65fa2fc443d87b7
created_at: 2023-11-23 12:38:37+09:00
updated_at: 2024-07-10 20:41:11+09:00
body:

Node Tools（**ノードツール**）は、[Blender 4.0に追加された新しい機能](https://www.blender.org/download/releases/4-0/)です。この機能を使うと、メッシュやカーブを**ジオメトリーノードを使って変換**できます。
つまり、今までPythonで書かれたアドオンを使わないとできないような処理が、ジオメトリーノードでできるようになります（ただし、ジオメトリーノードでできることしかできません）。

**参考**

https://www.youtube.com/watch?v=Y8Udi1AkdGY

本記事では、簡単にノードツールを紹介します。Blender 4.1とBlender 4.2で確認しています。

## 使い方

使い方は、ノードツールを作成して、メッシュに適用するだけです。

- ジオメトリーノードのタイプをツールにし、何らかのジオメトリーノードを作成する（**ノードツール作成**）。
- メッシュの編集モードで、メニューから作成したノードツールを選ぶ（**ノードツール適用**）。

ノードツールを適用すると、ジオメトリーノードの処理にしたがって、メッシュが変換されます。

## 試してみる

Blender 4.1またはBlender 4.2を起動してください。

### ノードツール作成

まずは、ノードツールを作成してみましょう。

ノードツールは、`ジオメトリノードエディター`で作成します。
今回は、下図のように`タイムライン`が表示されているエリアに`ジオメトリノードエディター`を表示させましょう。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/17c82308-c1f0-bd43-a089-356ccc457a95.gif" width="700">


`ジオメトリノードエディター`を表示させたら、下図のように左上の`ジオメトリノードタイプ`を`モディファイアー`から`ツール`にしてください。

![pic1.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a64e8a9e-bf1e-d46c-abf5-2271c6f23a2d.gif)

続いて、`ジオメトリノードエディター`上部の「新規」ボタンを押してください。グループ入力ノードとグループ出力ノードが表示されます。

:::note info
**ノート**
ノードを見失ったときは、ビューメニューの`全てを表示`を選びましょう。
:::

今回はシンプルに、X軸方向に移動する機能を作成します。
最初はノードツールの名前が`Tool`になっています。後で、わかりやすいように、上部中央の名前を`Move`にしてください（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a8d85953-3ec8-c278-233f-3b253b92a5bd.gif" width="700">


:::note info
**ノート**
デフォルトでは、ノードツールはメッシュに対しオブジェクトモードで使えますが、`ジオメトリノードエディター`上部右で変更できます。

* タイプ：`メッシュ`と`ヘアーカーブ`のそれぞれについて指定可
* モード：`オブジェクトモード`と`編集モード`と`スカルプトモード`のそれぞれについて指定可
* オプション：`クリック待機`を指定可（Blender 4.2のみ）

また、名前の付近で右クリックして`Mark As Asset`を選ぶことでアセット化できます。アセット化すると、別ファイルからも使いやすくなります。
:::

移動処理をするノードを追加しましょう。追加メニューの`ジオメトリ`の`処理`の`ジオメトリトランスフォーム`を選んでください（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/cde0cb90-1b5c-91f5-eb27-120ab06a4f85.gif" width="600">


マウスを動かすとノードも動くので、グループ入力ノードとグループ出力ノードの間でクリックして位置を確定してください（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bfe000cc-6d22-989d-ed36-61298288c1ea.gif" width="700">


うまくできなかったら、`Ctrl + Z`を何回か押して元に戻してからやり直してみましょう。

:::note info
**ノート**
クリックした位置によっては、ノードが接続されないことがあります。その場合は、後から端子をドラッグして接続できます。また、既に接続済みの端子の終端からドラッグすると接続を切ることもできます。
:::

ジオメトリトランスフォームノードの移動のXの値を`1m`に変えてください。デフォルトの単位はメートル（m）なので、クリックして1を入力すれば、`1m`になります。

これでノードツールの作成は終了です。

### ノードツール適用

ここからは、画面上部の`3Dビューポート`で作業します。`ジオメトリノードエディター`は、小さくすると作業しやすいでしょう。
ノードツールを立方体（Cube）に適用してみましょう。立方体がなければ、追加メニューの`メッシュ`の`立方体`から作成してください。

**立方体を選択してください**。

下図のように、画面上部の「オブジェクト」の右のアイコンをクリックし、`Move`を選んでください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/7192ea96-2db7-8058-116e-62c8163f2bcf.png" width="600">

ポイントがX軸方向に1m移動します。
この処理は、モディファイアーとは違い実際に変換が行われることに注意してください。

## パラメータ入力

ノードツール適用時に、移動距離を指定できるようにしましょう。
`ジオメトリノードエディター`で、追加メニューの`ユーティリティ`の`ベクトル`の`XYZ合成`を選んでノードを追加してください。
次に、作成したXYZ合成ノードのベクトル端子をドラッグして、ジオメトリトランスフォームノードの移動の端子に接続してください。
続いて、XYZ合成ノードのXから、グループ入力ノードの右下の`◯`に接続してください。下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/6f1f3d9f-ad26-65ab-24f6-bd01d0bb079a.gif" width="700">


このようにすると、Xをパラメータとして入力できるようになります。

`3Dビューポート`でもう一度、`Move`を適用してみましょう。今度は、左下に「Move」というオペレーターパネルが表示されます。このパネルをクリックすると、下図のように開きますので、Xの値を変えることで移動距離を調整できます。

![pic8.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a3ac1715-67c9-0b5e-7976-d75723ffeeec.gif)

:::note info
**ノート**
オペレーターパネルが消えたときは、F9を押すことで再表示できます。ただし、別の処理をしてしまうと再表示はできません。
:::

## Tips

`ジオメトリノードエディター`で、追加したいジオメトリーノードをメニューから探すのは大変です。このようなときは、下記の記事のように、検索して入力するとメニューの位置を覚えなくてすみます。

https://qiita.com/SaitoTsutomu/items/39eb1f022218c647c323

以上

