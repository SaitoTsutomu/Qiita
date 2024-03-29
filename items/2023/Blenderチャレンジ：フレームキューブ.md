title: Blenderチャレンジ：フレームキューブ
tags: 3DCG Blender クイズ Blenderチャレンジ
url: https://qiita.com/SaitoTsutomu/items/b4fa5ed4cdf2f59a372d
created_at: 2023-01-01 11:48:15+09:00
updated_at: 2023-08-12 23:31:18+09:00
body:

3DCGソフトウェアのBlenderを使って、お題のモデルを作成してみましょう。
やり方は一通りではないと思います。あなたは、どんな方法を考えますか？

## 問題

以下のようなオブジェクトを作ってください。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2cf49c57-7cba-1ce9-189e-50be504f341a.png)

※わかりやすいようにワイヤーフレーム表示にしています。

[完成物をSketchfabで見る](https://skfb.ly/oC6XI)

…
…
…

OK？

---

## 解答例

作成する手順です。macOSのキーを書いています。Windowsの場合は、`Option`を`Alt`に読み替えてください。

- 下記のアドオンを有効化。
    - Auto Mirror
    - Bool Tool

- `Shift + A`（追加メニュー）の「メッシュ」の「立方体」を選びます（以下Cube）。
- 編集モードで面だけ削除。
- 奥の1点を選択し、選択を拡大し頂点を削除。→4頂点が残る。
- 全選択し、`V + Space`で頂点をリップ。
- オブジェクトモードで変換のカーブ。
- カーブのジオメトリのベベルで深度を`0.2`、解像度を`10`。
- 変換のメッシュ。
- 編集モードで`AFP + Enter`。
- オブジェクトモードで`AN`
- サイドバーの編集タブのBool ToolのAuto BooleanのUnion。
    - うまく統合されなかったら2つずつ統合。
    - 編集モードで余計な頂点がないか確認。
- 別のCubeを追加。
- 編集モードで細分化（分割数を`5`、スムーズを`1`）。
- `S.1155`。
- 下図のように1/8の象限だけ残して他頂点を消す。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/89de6179-63ff-5e2f-c4b1-9bc4eed29e35.png)

- はまるように移動（各軸の移動距離は`1`）。
- オブジェクトモードで2つのオブジェクトを`Ctrl + J`で統合。
- 編集モードで不要な面を削除し、頂点をいい感じにマージ。
- オブジェクトモードでXYZでAutoMirror。
    - うまくいかなかったら、座標系を逆に。
- 変換のメッシュ化。
- 編集モードで不要な辺を溶解。

## 別解（完全に同じではない方法）

サブディビジョンサーフェスを使うと似たような感じになります。ただし、角付近が若干盛り上がります。

- 立方体（Cube）を追加。
- 編集モードで細分化し、細分化で追加された24辺を選択。
- `Ctrl + B`、`.75S2`、`[Enter]`
- 面モードにし、一番面積の大きい面を選択し、`Shift + G`の面積で、24面を選択。
- `Option + E`の法線に沿って面を押し出しを選び、`-.25`、`[Space]`。
- `X`で面を削除。
- `AM`で「距離で」。
- 点モードにし、XYZのいずれかが0の48頂点を選択。
- `Ctrl + B`、`.75S1`、`[Enter]`
- オブジェクトモードで、サブディビジョンサーフェスモディファイアーを追加し、ビューポートのレベル数を2に。

## ジオメトリーノードの例

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bd33cd95-a478-3ae8-e7d9-c9baa0731814.png)

角が`UV Sphere`なので、ちょっと違います。

## 参考

https://www.youtube.com/watch?v=rYUGd6UQwkY

以上

