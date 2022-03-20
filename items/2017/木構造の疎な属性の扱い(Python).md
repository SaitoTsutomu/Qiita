title: 木構造の疎な属性の扱い(Python)
tags: Python
url: https://qiita.com/SaitoTsutomu/items/1be9f7927696370ed06b
created_at: 2017-03-31 18:02:03+09:00
updated_at: 2017-04-02 00:09:30+09:00
body:

# はじめに[^1]

[^1]: 自分が忘れたときのメモ

あるデータ片(例:係)が、木構造(部課係)をなし、いろいろな属性(例:部長、課長、係長)を持っています。
属性をグループ(例:部や課)で設定して使う方法を説明します。

## 概要
木構造の **構成** と、属性(**名前**)の2種類の情報を定義して、使います。

### 元データ(TOML)
```py3;python3
import re, toml
toml._groupname_re = re.compile('^[A-Za-z0-9ぁ-んァ-ー一-龥_*-]+$')

tml = toml.loads("""\
[構成.A部]
L課="X係,Y係"
M課="Z係"
[構成.B部]
N課="W係"

[名前.A部]
部長="A氏"
[名前.A部.L課]
課長="L氏"
[名前.A部.L課.X係]
係長="X氏"
[名前.A部.L課.Y係]
係長="Y氏"
[名前.A部.M課]
課長="M氏"
[名前.A部.M課.Z係]
係長="Z氏"
[名前.B部]
部長="B氏"
[名前.B部.N課]
課長="N氏"
[名前.B部.N課.W係]
係長="W氏"
""")

tml['構成']
>>>
{'A部': {'L課': 'X係,Y係',
         'M課': 'Z係'},
 'B部': {'N課': 'W係'}}

tml['名前']
>>>
{'A部': {'L課': {'X係': {'係長': 'X氏'},
                 'Y係': {'係長': 'Y氏'},
               '課長': 'L氏'},
         'M課': {'Z係': {'係長': 'Z氏'},
               '課長': 'M氏'},
       '部長': 'A氏'},
 'B部': {'N課': {'W係': {'係長': 'W氏'},
               '課長': 'N氏'},
       '部長': 'B氏'}}
```

## 構成データ作成
ortoolpy.MultiKeyDict を使って構成データを作成します。
forでループすると、全データ(全係)にアクセスできます。
なお、MultiKeyDict は、キャッシュされるため、更新できません。
(設定情報のように最初に読込んで、変更しないことを想定)

```py3;python3
from ortoolpy import MultiKeyDict
iskey = lambda x: x[-1] in '部課係' # '部課係'で終わるキーから新たな MultiKeyDict とする
conv = lambda x: ((s,None) for s in x.split(','))
構成 = MultiKeyDict(tml['構成'], iskey=iskey, conv=conv, extend=True)
for ky in 構成:
    print(ky)
>>>
('A部', 'L課', 'X係')
('A部', 'L課', 'Y係')
('A部', 'M課', 'Z係')
('B部', 'N課', 'W係')
```

## 属性データ確認
属性データ(名前)をMultiKeyDict で作成し、構成データをキーにしてアクセスします。

```py3;python3
名前 = MultiKeyDict(tml['名前'], iskey=iskey)
for ky in 構成:
    print(' '.join(ky))
    for ky2, name in 名前[ky].items():
        print(f' %s: %s'%(ky2[-1],name))
>>>
A部 L課 X係
 部長: A氏
 課長: L氏
 係長: X氏
A部 L課 Y係
 部長: A氏
 課長: L氏
 係長: Y氏
A部 M課 Z係
 部長: A氏
 課長: M氏
 係長: Z氏
B部 N課 W係
 部長: B氏
 課長: N氏
 係長: W氏
```

### 別の方法

```py3;python3
for ky in 構成:
    print(' '.join(ky))
    dc = 名前.get_list(ky, True)
    print(f' 部長: %s'%dc['部長'][0])
    print(f' 課長: %s'%dc['課長'][0])
    print(f' 係長: %s'%dc['係長'][0])
>>>
A部 L課 X係
 部長: A氏
 課長: L氏
 係長: X氏
A部 L課 Y係
 部長: A氏
 課長: L氏
 係長: Y氏
A部 M課 Z係
 部長: A氏
 課長: M氏
 係長: Z氏
B部 N課 W係
 部長: B氏
 課長: N氏
 係長: W氏
```

下記のように、[名前.A部]で定義した部長が、[名前.A部.L課.X係]や[名前.A部.L課.Y係]でも「部長="A氏"」と参照できました。

> [名前.A部]
部長="A氏"

このように、木構造のどこで属性を定義したか気にせずに、末端のデータ(係)で属性を取得できます。

以上

