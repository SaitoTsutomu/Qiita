title: Blenderで花火を打ち上げるアドオン
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/9c7aae103bf13d72dd5c
created_at: 2022-04-11 07:10:13+09:00
updated_at: 2022-08-27 14:56:10+09:00
body:

## Blenderで花火を打ち上げるアドオン

Blender3.1で、花火を打ち上げるアドオンをPythonで作成したので紹介します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a5d919a0-ae1e-e31f-af96-580e25f88813.gif" width="300">

## やり方

### アドオンのインストール

- [Blender Add-on: Fireworks](https://github.com/SaitoTsutomu/Fireworks)の画面にしたがってインストールしてください。
    - アドオンのチェックでは「テスト中」を選んでください。

### PyYamlのインストール

本アドオンは、PythonのPyYamlモジュールを利用しています。
そのため、下記のように、コマンドラインでBlenderにPyYamlをインストールする必要があります。コマンドラインからBlenderを操作する方法については、「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」も参考にしてください。

- macOSの場合
```
/Applications/Blender.app/Contents/Resources/3.1/python/bin/python3.10 -m pip install pyyaml
```

- Windowsの場合
```
"C:\Program Files\Blender Foundation\Blender 3.1\3.1\python\bin\python" -m pip install pyyaml
```

※ Windowsで、インストールできるのに`import`で**エラーになる場合**は、一旦アンインストールしてから、**管理者権限のコマンドプロンプトでインストール**し直すとうまくいくかもしれません。

### Yamlファイルの作成

花火の設定は、Yamlファイルで行います。
作成例は下記のようになります。

```
shot1:
  radius: 0.1
  particle_size: 0.06
  material:
    color: [1, 1, 0.5, 1]
    strength: 30
  launch: 1
  launch_location: [0, 0, 0]
  explode: 60
  explode_location: [2, 3, 10]
  particle_systems:
    up:
      count: 200
      frame_start: launch + 0
      frame_end: explode + 15
      lifetime: 20
      material:
        color: [1, 1, 0.5, 1]
        strength: 30
    ex1:
      count: 400
      frame_start: explode + 0
      frame_end: explode + 5
      lifetime: 40
      factor_random: 1
      gravity: 0
      material:
        color_ramp:
          - position: 0.5
            color: [1, 1, 0, 1]
          - position: 1
            color: [1, 1, 0, 0.1]
        strength: 30
    ex2:
      count: 1000
      frame_start: explode - 2
      frame_end: explode + 10
      lifetime: 50
      factor_random: 2
      gravity: 0
      material:
        color_ramp:
          - position: 0.5
            color: [0, 1, 0, 1]
          - position: 1
            color: [1, 0, 0, 0.1]
        strength: 30
```

`shot1`は、作成する花火のオブジェクトの名前です。任意の名前が使えます。花火はいくつでも作成できます。
`launch`は打ち上げ時のフレームです。`explode`は爆発時のフレームです。

花火はパーティクルで実現しています。
上記では、下記の３つのパーティクルシステムを設定しています。いくつでも設定できます。パーティクルシステムの名前も任意です。

- `up`：爆発までの火花
- `ex1`：内側の爆発
- `ex2`：外側の爆発

### 作成

- サイドバーの編集タブの「Fireworks」を開いてください。
- `file`に作成したファイルをフルパスで記述します。
- `Make（作成）`ボタンを押します。

## 補足

花火の色はカラーランプで、時間により色が変わるようにしています。Cyclesではパーティクル情報ノードが使えたようなのですが、Eeveeだとパーティクルの情報が取得できなかったので、ドライバーで設定しています。爆発時にカラーランプの係数が0で爆発終了＋寿命で係数が1になります。

### Pythonのコード

https://github.com/SaitoTsutomu/Fireworks/blob/main/__init__.py

以上

