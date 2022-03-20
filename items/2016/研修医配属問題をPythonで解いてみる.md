title: 研修医配属問題をPythonで解いてみる
tags: Python 数学 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/443300bce64d0d0f2865
created_at: 2016-02-12 19:45:14+09:00
updated_at: 2016-02-19 18:08:09+09:00
body:

# <i class='fa fa-venus-mars' />はじめに
1962年にD. Gale（デイヴィッド・ゲール）と L. S. Shapley（ロイド・シャプレイ）によって、安定結婚問題が提唱されました。シャプレイは、この一連の功績により2012年にノーベル経済学賞を受賞しています。

安定結婚問題とは、以下のような問題です。(Wikipediaより)

    安定結婚問題の例題は N 人の男性と N 人の女性、および、各個人の希望リストからなる。
    希望リストとは各個人の好みに基づき異性全員を全順序で並べたリストである。
    安定結婚問題の解は安定なマッチングである。安定結婚問題の例題に対し、
    互いに現在組んでいる相手よりも好きであるペア（以下ブロッキングペアとする）が
    存在しないマッチングを安定なマッチングという。

安定結婚問題は安定マッチング問題の1種であり、安定マッチング問題は、研修医の病院への配属、大学生の研究室への配属など、広く使われています。
研修医配属については、アメリカでは1950年頃から利用されており、日本でも最近利用され始めました。

安定マッチング問題は、Pythonの[ortoolpy](https://pypi.python.org/pypi/ortoolpy)の[stable_matchingで解く](http://qiita.com/Tsutomu-KKE@github/items/2ec5f7626054f4b4de63)ことができます。実際に試してみましょう。

# <i class='fa fa-venus-mars' /> Pythonで解く

ortoolpyのstable_matchingは、研修医と配属先が同数の場合しか解くことができません。
ここでは、配属先Aの受入可能数が2の場合、配属先A_0、配属先A_1のように配属先のダミーを作成してマッチングさせることにしましょう。そのように拡張した安定マッチング問題を解くメソッド stable_matching2 を定義します。

```py3:python3
from itertools import accumulate
from ortoolpy import stable_matching
def stable_matching2(prefs, prefl, capa):
    """
    非対称マッチング
    prefs: 研修医が持つ配属先に対する選好
    prefl: 研修医に対する選好(全ての配属先は同じ選好とする)
    capa: 配属先の受入可能数
    """
    acca = list(accumulate([0] + capa[:-1])) # 累積受入可能数
    idx = [i for i, j in enumerate(capa) for _ in range(j)] # ダミー配属先→配属先の変換リスト
    prefs = [[j+acca[i] for i in pr for j in range(capa[i])] for pr in prefs] # ダミーの選考
    res = stable_matching([prefl] * len(prefl), prefs)
    return{k:idx[v] for k, v in res.items()} # ダミーをオリジナルに戻して返す
```

ランダムに問題を作成します。

```py3:python3
lab_capa = [2, 3, 3, 2] # 配属先の受入可能数
ns, nl = sum(lab_capa), len(lab_capa) # 研修医数と配属先数

import numpy as np
np.random.seed(1)
def shuffled(n):
    """0..n-1をシャッフルして返す"""
    a = np.arange(n)
    np.random.shuffle(a)
    return a.tolist()
performance = shuffled(ns) # 研修医に対する選好
preferences = [shuffled(nl) for i in range(ns)] # 配属先に対する選好

print(performance)
print(preferences)
>>>
[2, 9, 6, 4, 0, 3, 1, 7, 8, 5]
[[2, 0, 1, 3], [3, 0, 1, 2], [3, 1, 2, 0], [3, 1, 0, 2], [1, 3, 2, 0],
 [3, 0, 2, 1], [3, 2, 1, 0], [1, 0, 2, 3], [0, 3, 1, 2], [2, 0, 3, 1]]
```

解いて結果を表示します。

```py3:python3
res = stable_matching2(preferences, performance, lab_capa)
for k, v in res.items():
    print('研修医%d -> 配属先%d'%(k,v))
>>>
研修医0 -> 配属先2
研修医1 -> 配属先0
研修医2 -> 配属先3
研修医3 -> 配属先1
研修医4 -> 配属先1
研修医5 -> 配属先2
研修医6 -> 配属先3
研修医7 -> 配属先1
研修医8 -> 配属先0
研修医9 -> 配属先2
```

# <i class='fa fa-venus-mars' /> 組合せ最適化との関連
安定マッチング問題は、ブロッキングペアがないマッチングを求める問題で、気にするのは、選好順序という相対的な値です。
そもそも選好が絶対的な値の場合は、組合せ最適化問題の重みマッチング問題になります。

絶対的な値というのは、例えば、研修医の自宅から配属先までの通勤時間などがあたります。このとき、全研修医の通勤時間の総和を最小化する問題は、重みマッチング問題でありエドモンズ法などで解くことができます。

重みマッチング問題の解は安定マッチングになりますが、安定マッチング問題の解は重みマッチング問題の最適解とは限りません。

結局、以下のようになります。
> 確からしい重みを考えることができる → 重みマッチング問題
> はっきりした重みは不明だが順序はわかる → 安定マッチング問題

参考
[安定結婚問題を解きながらHaskellプログラミングを紹介しつつ恋愛について学ぶ](http://qiita.com/cutsea110/items/27d9f6db834b70e52dd9)
以上

