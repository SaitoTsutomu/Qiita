title: Blenderチャレンジ：平面の丸い穴
tags: 3DCG Blender クイズ Blenderチャレンジ
url: https://qiita.com/SaitoTsutomu/items/5a9fd6e48dd1fd44f93b
created_at: 2021-12-13 19:10:18+09:00
updated_at: 2021-12-22 20:19:33+09:00
body:

3DCGソフトウェアのBlenderを使って、お題のモデルを作成してみましょう。
やり方は一通りではないと思います。あなたは、どんな方法を考えますか？

## 問題

「メッシュ」の「平面」を追加してください。追加した平面に下記のように丸い穴を開けてください。

![スクリーンショット 2021-12-14 7.30.12.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/94c0de6d-503c-13af-5154-7fbfdb0f773f.jpeg)

[完成物をSketchfabで見る](https://skfb.ly/orXx8)

…
…
…

OK？

---

## 解答例

作成する手順です。macOSのキーを書いています。Windowsの場合は、`Option`を`Alt`に読み替えてください。

- 「平面」を選んで編集モードに入ります。
- `Shift + E`、`1`、`[Enter]`（辺のクリースを1に設定）。
- 2回「細分化」してください。
- 中央の`2 x 2`の四角の外側の8点を選択してください。
- `Shift + E`、`1`、`[Enter]`。
- 中央の点を追加で選び、9点を選択してください。
- `Option + Shift + S`、`1`、`[Enter]`（球状に変形）。
- `E-.5`、`[Enter]`（押し出し）。
- オブジェクトモードに戻り、サブディビジョンサーフェスモディファイアーを追加し、「ビューポートのレベル数」を2にしてください。

以上



