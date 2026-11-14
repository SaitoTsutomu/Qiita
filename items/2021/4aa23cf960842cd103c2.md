title: Blenderチャレンジ：網目
tags: 3DCG Blender クイズ Blenderチャレンジ
url: https://qiita.com/SaitoTsutomu/items/4aa23cf960842cd103c2
created_at: 2021-12-19 06:08:53+09:00
updated_at: 2021-12-22 20:28:25+09:00
body:

3DCGソフトウェアのBlenderを使って、お題のモデルを作成してみましょう。
やり方は一通りではないと思います。あなたは、どんな方法を考えますか？

## 問題

下記のような2m×2mの平面状のメッシュを作成してください。なお、頂点数は`６４`です。

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/445bcd6f-2191-66c4-737e-004d55b6ea2c.jpeg)

[完成物をSketchfabで見る](https://skfb.ly/orXxI)

…
…
…

OK？

---

作成する手順です。

## 解答例1

- `Shift + A`の追加で「メッシュ」→「グリッド」でグリッドを追加します。
- 編集モードに入ります。
- 「辺」メニューの「分割の復元」を選び、詳細設定で下記のように、「反復」を`1`にしてください。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/cdf79e83-9d72-9d85-010f-e9f39da6f867.png)

## 解答例2

- `Shift + A`の追加で「メッシュ」→「グリッド」でグリッドを追加します。
- デシメートモディファイアーを追加し、「分割の復元」にし、「反復」を`1`にし、適用してください。

「分割の復元」は、縦横のメッシュを斜めにするのに、よく使われますね。

以上

