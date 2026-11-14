title: Blenderファイルのサムネイルを取得するには
tags: Python Blender thumbnail pillow
url: https://qiita.com/SaitoTsutomu/items/dda5b92ba636728bbb39
created_at: 2024-07-23 21:03:22+09:00
updated_at: 2024-07-23 21:03:22+09:00
body:

## はじめに

Blenderファイルのサムネイルを取得する方法を検索すると、BlenderのPythonでファイルを開いてレンダリングする方法が出てきたりします。
実は、Blenderファイル自体がサムネイルを持っているので、レンダリングする必要はありません。

## サムネイルの設定

サムネイルの設定は、プリファレンスのセーブ＆ロードのBlendファイルのファイルプレビュータイプです。

![image1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bc797d4c-a098-b66e-61a2-f3d15b5ef57b.png)

「なし」を選んで保存したファイルからは、サムネイルが取得できないのでご注意ください。

## サムネイルを取得する準備

Pythonを使いますが、Blenderに付属するPythonを使う必要はありません。
次のように必要なものをインストールしてください。

```
pip install blender-asset-tracer pillow
```

## サムネールを取得してファイルに保存

`sample.blend`というBlenderファイルのサムネイルを取得して`thmbnail.png`に保存するには、次のようにします。

```python
import struct
from pathlib import Path
from PIL import Image
from blender_asset_tracer import blendfile

bf = blendfile.open_cached(Path("sample.blend"))
data = bf.find_blocks_from_code(b'TEST')[0].raw_data()
w, h = struct.unpack('>BxxxBxxx', data[:8])
image = Image.frombytes("RGBA", (w, h), data[8:])
image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save("thmbnail.png")
```

`transpose(Image.FLIP_TOP_BOTTOM)`は、画像の上下を反転させます。


Blender4.2のファイルを試した限りでは次のように取得できましたが、完全に理解しているわけではないので、環境によっては動かないかもしれません。

![thmbnail.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/42bf8e63-8a0e-2521-b5d0-7addaed6977d.png)

以上

