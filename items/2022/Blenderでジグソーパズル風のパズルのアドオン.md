title: Blenderでジグソーパズル風のパズルのアドオン
tags: Python 3DCG Blender パズル
url: https://qiita.com/SaitoTsutomu/items/f71b9dfb4c68a71f848a
created_at: 2022-03-28 07:35:19+09:00
updated_at: 2022-03-28 09:25:51+09:00
body:

## Blenderでジグソーパズル風のパズル

Blender3.1で、ジグソーパズル風のパズルを遊べるアドオンをPythonで作成したので紹介します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0567dc42-2a5b-343f-5944-3c8b45db5a35.png" width="300">


## やり方

- [Blender Add-on: Jigsaw](https://github.com/SaitoTsutomu/Jigsaw)の画面にしたがってインストールしてください。
    - アドオンのチェックでは「テスト中」を選んでください。
- サイドバーの編集タブの「Puzzle」を開いてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d3ab43df-16d4-0e3a-6684-509645ec1274.png" width="300">

- 横と縦の分割数を`num_x`、`num_y`に設定してください。
- パズルを作成するには、「Make Puzzle」を押してください。
    - 画像の選択画面が出るので、画像を選んでください。
- 下図のように、選んだ画像を分割したブロックと枠が作成されます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ee3d867d-1e1e-5218-e7e7-d316278eb385.png" width="300">

- パズルを遊ぶには「Start」を押してください。ブロックがバラバラになります。
    - ブロックを枠内に収めると、枠が黄色になって終了です。
- 途中でやめるときは、「Finish」を押してください。「Finish」を押すと、完成したかどうかの判定を行いません。

## しくみ

ブロックのUVを適切に作成するのは、手間がかかります。
そこで、1つのグリッドに画像のマテリアルを設定し、そのグリッドを辺分離モディファイアーでバラバラにします。
さらに、ブロックにするために、編集モードで押し出しをします。これをオブジェクトとしてバラバラにするために、構造的に分離したパーツで分離します。
このままだと、ブロックの原点で正解位置がばれるので原点をジオメトリに変えます。
「Start」を押すと、開始位置を覚えて、バラバラにし、タイマーで定期的に位置をチェックし、位置が正しければ終了します。

### Pythonのコード

https://github.com/SaitoTsutomu/Jigsaw/blob/main/__init__.py

以上


