title: BlenderでVOICEVOXの音声をPythonで追加
tags: Python Blender VOICEVOX
url: https://qiita.com/SaitoTsutomu/items/b2ff4b45ffe578ec23a4
created_at: 2022-04-01 23:22:21+09:00
updated_at: 2022-08-06 22:46:30+09:00
body:

## 概要

CSVで用意したテキストをVOICEVOXで音声ファイルを作り、Blenderで取り込みます。
これをPythonで行う方法を紹介します。

## 準備（VOICEVOXのインストールと実行）

VOICEVOXは、無料で使える中品質なテキスト読み上げソフトウェアです。
使用においては、[VOICEVOXの利用規約](https://voicevox.hiroshiba.jp/term)をご確認ください。

下記のサイトから、インストーラーをダウンロードしてインストールしてください。

- https://voicevox.hiroshiba.jp/

インストールしたら、起動してください。
起動したら、GUIでも使えますが、Webサーバーとしても起動します。
Blenderからは`curl`を使ってWebサーバーの方にアクセスします。
もし、`curl`が入ってなければ、インストールしておいてください。

## 手順

Blenderを起動し、下図のように2つのテキストエディターとビデオシーケンサーを開いてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0d66a779-21c2-e81b-80bb-11dfd5f9e08d.png" width="600">

### CSV

「時刻（秒）、キャラクター番号、テキスト」を書いたCSVファイルを用意してください。下記はサンプルです。

```voice.csv
0,2,3DCGなら
1.6,12,ブレンダー!
```

1つ目のテキストエディターでCSVを開いてください。
ファイル選択画面で、デフォルトでCSVは見えませんが、右上のフィルターをオフにすると見えるようになります。

### Pythonコード

2つ目のテキストエディターの新規を押し、下記をコピペしてください。

```py
import bpy
import csv
import time
from pathlib import Path
from subprocess import run

csvfile = [text.filepath for text in bpy.data.texts
           if text.filepath.endswith(".csv")][0]

se = bpy.context.scene.sequence_editor
header = "Content-Type: application/json"
fps = bpy.context.scene.render.fps

tmp = Path("/tmp")
pth = tmp /"wav"
pth.mkdir(exist_ok=True)

# delete all sequence
for s in se.sequences_all:
     se.sequences.remove(s)

with open(csvfile) as fp:
    for i, ss in enumerate(csv.reader(fp), 1):
        try:
            sec, *mnt = map(float, reversed(("0:" + ss[0]).split(":")))
            speaker = int(ss[1])
            text = ss[2]
        except (IndexError, ValueError):
            print(f"Error at line {i}: {ss}")
            break
        frame_start = int((mnt[0] * 60 + sec) * fps)
        url = f"localhost:50021/{{}}?speaker={speaker}"
        namt = str(tmp / "text.txt")
        with open(namt, "w") as fp:
            fp.write(text)
        cmd = f'curl -s -X POST {url.format("audio_query")} --get --data-urlencode text@{namt}'
        res = run(cmd.split(), capture_output=True)
        namq = str(tmp / "query.json")
        with open(namq, "w") as fp:
            fp.write(res.stdout.decode())
        cmd = f'curl -s -H {header} -X POST -d @{namq} {url.format("synthesis")}'
        res = run(cmd.split(), capture_output=True)
        nama = f"audio{i:03}.wav"
        with open(pth / nama, "wb") as fp:
            fp.write(res.stdout)
        ss = se.sequences.new_sound(nama, str(pth / nama), i * 2, frame_start)
        ss = se.sequences.new_effect(f"txt{i:03}", "TEXT", i * 2 + 1, frame_start, frame_end=ss.frame_final_end)
        ss.text = text
        time.sleep(0.1)
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

上記のPythonコードを実行すると、CSVを読み込んで音声ファイルを作成して取り込みます。
スペースキーを押すと再生します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/7fac492e-ce77-de78-a594-220ea51f100d.jpeg" width="600">

また、下記の設定でアニメーションレンダリングすると、音声と字幕付きで作成できました。

- ファイルフォーマット：FFmpeg動画
- エンコーディング
    - コンテナ：MPEG-4
    - オーディオ
        - 音声コーデック：AAC

以上




