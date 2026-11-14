title: Jupyterのkernelを作ってみる
tags: Python Docker Jupyter
url: https://qiita.com/SaitoTsutomu/items/3c996bde01ef2637aadc
created_at: 2016-01-01 15:26:08+09:00
updated_at: 2018-12-13 13:59:26+09:00
body:

# <i class='fa fa-paw' /> 何をするの？
[Jupyter](http://jupyter.org/)は、50以上の言語に対応しています([IPython kernels for other languages](https://github.com/ipython/ipython/wiki/IPython-kernels-for-other-languages))。
新しい言語に対応させることも簡単にできます。(参考：[Making kernels for Jupyter](https://jupyter-client.readthedocs.org/en/latest/kernels.html))
ここでは、例として、KeyValueというJupyterの新しいkernelを作ってみましょう。

# <i class='fa fa-paw' /> 作るもの
単純にキーと値のペアを管理するものを作ります。

コマンド|説明
:--|:--
?|キー一覧の表示
キー|キーに対応する値を表示
キー 値|キーに対応する値を設定

# <i class='fa fa-paw' /> 実装
2つのファイルを所定の位置に置くだけです。

## JSONファイル
下記のJSONファイルを作成します。作成場所は、[Kernel specs](https://jupyter-client.readthedocs.org/en/latest/kernels.html#kernel-specs)を見てください。
("argv"の"python3"がない場合、"python"に変えてください。)

```json:keyvalue/kernel.json
  "argv": [
    "python", "-m", "keyvaluekernel", "-f", "{connection_file}"
  ],
 "display_name": "KeyValue"
}
```

## Pythonファイル
下記のpythonファイルをpythonのインストール先の配下に作成します。

```py3:keyvaluekernel.py
from ipykernel.kernelbase import Kernel

class KeyValue(Kernel):
    implementation = 'KeyValue'
    implementation_version = '0.1'
    language = 'no-op'
    language_version = '0.1'
    language_info = {'name': 'KeyValue', 'mimetype': 'text/plain'}
    banner = 'Dictionry of Key, Value'
    _d = {}
    def do_execute(self, code, silent, store_history=True,
             user_expressions=None, allow_stdin=False):
        s = code.strip()
        if not silent:
            if s.startswith('?'):
                c = {'name': 'stdout', 'text': ' '.join(KeyValue._d.keys())}
            else:
                ss = s.split(maxsplit=1)
                if len(ss) == 1:
                    if s in KeyValue._d:
                        c = {'name': 'stdout', 'text': KeyValue._d[s]}
                    else:
                        c = {'name': 'stderr', 'text': 'Not found'}
                else:
                    KeyValue._d[ss[0]] = ss[1]
                    c = {'name': 'stdout', 'text': ss[1]}
            self.send_response(self.iopub_socket, 'stream', c)
        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
    def do_complete(self, code, cursor_pos):
        s = code[:cursor_pos]
        return {'status': 'ok', 'matches': [k for k in KeyValue._d if k.startswith(s)],
                'cursor_start': cursor_pos, 'cursor_end': -1, 'metadata': {}}

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=KeyValue)
```

あるいは、任意の場所に配置し、先程のJSONファイルの`env`キーの`PYTHONPATH`に配置場所を指定してください。

```json:keyvalue/kernel.json
{
  "argv": [
    "python", "-m", "keyvaluekernel", "-f", "{connection_file}"
  ],
  "display_name": "KeyValue",
  "env": {
    "PYTHONPATH": "/path/to/your/modules"
  }
}
```

do_executeで実行した結果を計算し返します。
do_completeは、タブを押したときの補完する内容を返します。

OS|作成場所の例
:--|:--
Windows|C:\Anaconda3\Lib\site-packages
Ubuntu|/usr/local/lib/python3.4/dist-packages

# <i class='fa fa-paw' /> 試してみる
- "jupyter notebook"で起動し、[New]から[KeyValue]を選んでください。
- "key1 value1"といれて実行(Shift+Enter)してください。
- "key1"といれて実行すると"value1"と出ます。
- "key2 value2"といれて実行してください。
- "?"と実行するとキー一覧が出ます。
- "k"まで入力して[Tab]を押すと、候補がでます。

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/b6640f69-e806-47a9-158a-2bafdd2dca80.png)

## Dockerイメージ
簡単に確認できるように、dockerイメージ([tsutomu7/keyvalue](https://hub.docker.com/r/tsutomu7/keyvalue/))を用意しました。
下記のように確認できます。

```:ubuntu
docker run -it --rm tsutomu7/keyvalue
```

上記実行後、"http://ホストのIPアドレス:8888"(例えば、"http://172.17.0.2:8888" )を開いてください。

