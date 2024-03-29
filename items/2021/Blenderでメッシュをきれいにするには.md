title: Blenderでメッシュをきれいにするには
tags: 3DCG Blender モデリング
url: https://qiita.com/SaitoTsutomu/items/5d0211d5ce4140be6b03
created_at: 2021-12-17 21:42:10+09:00
updated_at: 2022-01-11 21:26:00+09:00
body:

## メッシュをきれいにするには

Blenderで、ちょこちょこ点を動かしてると、汚くなってくることはないでしょうか？
ここでは、簡単にきれいにする方法を紹介します。

説明用に、下記のメッシュを用意しました。なるべくローポリでへこみがないものが良いです。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d8b62940-66f6-aa0f-37ac-30374ffa0dd3.png)

元は`Sphere`です。縦横に真っすぐだったのですが、ジグザグになったりしてます。

## メッシュをきれいにした後の比較

右が元のオブジェクトで、左が修正後です。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2c62b144-0fcb-f693-c603-901f0adff604.png)

## 手順

- [PolyQuilt](https://sakana3.github.io/PolyQuilt/)アドオンを使います。リンク先からダウンロードしてインストールしてください。PolyQuiltアドオンはなくてもできるのですが、あると見やすくなります。
- きれいにしたいオブジェクトを複製します。
- 複製したオブジェクトに以下の処理をします。
    - マテリアルをつけて色を緑などにします。これは、元のと複製したものとを区別するためです。
    - サブディビジョンサーフェスモディファイアーを追加します。これは、メッシュが荒いときれいになりにくいことがあるからです。あまりに形が変わるようであれば、しなくても大丈夫です。
    - `1.01`倍のように、ちょっと大きくします。これは、サブディビジョンサーフェスで、若干小さくなるためです。サイズに違和感があれば、最後に調整しても良いでしょう。

ここまでで以下のようになります。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/54ca2650-7732-da37-d418-a84a3e890a35.png)

## 手順続き

- 修正したいオブジェクトを選択して、編集モードに入ります。
- 「スナップ」をオンにして、スナップ先を面にします。

![スクリーンショット 2021-12-17 21.31.17.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3c8d3d0e-3ac7-55c5-a281-1d23ebd96eba.jpeg)

- PolyQuiltを選び、Shiftを押しながら頂点をドラッグしてスムーズを掛けていきます。へこんでいるところはうまくいかないので避けましょう。

※ PolyQuiltを使わない場合は、スカルプトモードでスムーズを掛けてください。

これだけでメッシュがきれいになっていきます。作業が終わったら複製したものは削除してください。

## 別の方法

スカルプトモードで、スライドリラックスにして、Shiftキーを押しながらドラッグしてもメッシュがきれいになるようです。こちらの方がお手軽ですね。

以上

