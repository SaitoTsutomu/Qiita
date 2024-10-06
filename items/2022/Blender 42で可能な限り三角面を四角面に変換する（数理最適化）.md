title: Blender 4.2で可能な限り三角面を四角面に変換する（数理最適化）
tags: Python 3DCG addon Blender 最適化
url: https://qiita.com/SaitoTsutomu/items/b608c80d70a54718ec78
created_at: 2022-03-21 17:05:44+09:00
updated_at: 2024-10-05 13:52:46+09:00
body:

## メッシュの四角面化

Blenderには、三角面を四角面にする機能があります。これは、辺の長さを考慮して溶解する辺を選んでいます。
これはこれで便利なのですが、**可能な限り三角面を四角面に変えたい**ことがあります。
ここでは、それを**数理最適化**で実現するアドオンを紹介します。

## 具体例

下記のメッシュで試してみます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/26141131-8915-b923-87f3-78e115397f85.png" width="300">

通常の「三角面を四角面に」を実行すると下記のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/21a01f16-46d2-1765-239a-17c19d654514.png" width="300">

隅の方に三角面ができています。

一方で、今回紹介するアドオンを実行すると下記のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/928d6e87-6d11-b922-2452-980fb8eeb984.png" width="300">

すべての三角面が四角面になっています。

## インストール方法

### PuLPのインストール

本アドオンは、Pythonの[PuLP](https://github.com/coin-or/pulp)モジュールを利用しています。
そのため、下記のように、コマンドラインでBlenderにPuLPをインストールする必要があります。コマンドラインからBlenderを操作する方法については、「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」も参考にしてください。

※ バージョンは適宜変えてください。

- macOSの場合
```
/Applications/Blender.app/Contents/Resources/4.2/python/bin/python3.11 -m pip install pulp
```

- Windowsの場合
```
"C:\Program Files\Blender Foundation\Blender 4.2\4.2\python\bin\python" -m pip install pulp
または
"C:\Program Files\Blender Foundation\Blender 4.2\4.2\python\Scripts\pip" install pulp
```

※ Windowsで、インストールできるのに`import`で**エラーになる場合**は、一旦アンインストールしてから、**管理者権限のコマンドプロンプトでインストール**し直すとうまくいくかもしれません。

※ 実は、[Python-MIP](https://www.python-mip.com/)ライブラリーを使いたかったのですが、Blenderでは動かないためPuLPを用いています。

### アドオンのインストール

- GitHubの[Tris-Quads-Ex](https://github.com/SaitoTsutomu/Tris-Quads-Ex)から、下記のアドオンのZIPファイルをダウンロードしてください。ZIPファイルは解凍しないでください。

  - [アドオンのZIPファイル](https://github.com/SaitoTsutomu/Tris-Quads-Ex/archive/refs/heads/master.zip)

- Blenderのプリファレンスのアドオンで「ディスクからインストール…」ボタンを押し、ダウンロードしたZIPファイルを選択します

- 下図のように、`Tris to Quads Ex`にチェックを入れてください

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/65391d5d-1b63-d479-00a1-a1db48c901c1.png" width="600">


## 使い方

- 対象のオブジェクトを選んで、編集モードに入ります
- **対象の範囲を選択して、面メニューの「Tris to Quads Ex」を選びます**

※ **選択している辺の中でしか溶解しません**。すべてを対象にする場合は、`A`で全選択してください。

- 実行後、四角面以外を選択します

## 最適化について

「可能な限り三角面を四角面にする」ためには、溶解する辺の数をなるべくたくさん選ぶ必要があります。
一方で、選びすぎるとNゴン（頂点が5以上の多角形）になってしまうので、できる多角形の頂点を4までに抑える必要があります。
このような問題は混合整数最適化問題になります。
混合整数最適化問題とは何かについては、「[組合せ最適化を使おう](https://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)」を参考にしてください。
ここでは、混合整数最適化問題を定式化し、PuLPでモデル化し、CBCソルバーで解きます。

### 定式化

変数は以下の条件を満たす辺ごとに0-1変数を作成します。1が溶解する、0が溶解しないに対応します。

- 選択されている
- 両側の面がともに選択された三角面である

ここでは、下記の定式化を解いて、溶解する辺を求めています。

| 目的関数 | 溶解する辺の数 + 0.1×正規化した辺の長さの和 → 最大化 |
| :------: | :--------------------------------------------------: |
| 制約条件 |          三角面ごとに、溶解する辺は1本以下           |

三角面に対し2本以上を溶解するとNゴンになるため、上記の制約条件になります。

## アドオンのコード（Python）

https://github.com/SaitoTsutomu/Tris-Quads-Ex/blob/master/__init__.py

実際に辺を溶解するのは、`execute()`メソッドになります。

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

以上

