title: 最長しりとりを組合せ最適で解く
tags: Python 数学 最適化 パズル 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/ba2dedb5795cae36f8a1
created_at: 2016-01-11 13:15:35+09:00
updated_at: 2018-03-02 10:25:49+09:00
body:

# <i class='fa fa-chain' /> 最長しりとりを解く
[組合せ最適化](http://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)を使うと最長しりとりも簡単に解けます。

# <i class='fa fa-chain' /> 定式化
[典型問題](http://qiita.com/SaitoTsutomu/items/0f6c1a4415d196e64314)の中の2部グラフの最大マッチング問題の変種になります。
しりとりに使われる単語を$kw$とします。
$kw$を左右にそれぞれ並べ、左を先行、右を後行とします。そして、つながる場合に線を引くことを考えます。下記の図では、"alignas"の後に"sizeof"を繋げることを表しています。

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/9071a6fd-5514-695e-ec87-a148d19016ae.png)

この線を引くか引かないかを$x_{ij} \in \{0, 1\}$で表すことにします。

<table>
<tr><td>$\mbox{objective}$</td><td>$\sum_i{\sum_j{x_{ij}}}$</td><td>なるべく繋げる (0)</td></tr>
<tr><td rowspan="3">$\mbox{variables}$</td><td>$x_{ij} \in \{0, 1\} ~ \forall i, j$</td><td>$kw_i$の次が$kw_j$かどうか (1)</td></tr>
<tr><td>$y_i \ge 0 ~ \forall i$</td><td>$kw_i$が先頭かどうか (2)</td></tr>
<tr><td>$z_i \ge 0 ~ \forall i$</td><td>$kw_i$の順番 (3)</td></tr>
<tr><td rowspan="4">$\mbox{subject to}$</td><td>$\sum_j{x_{ij}} = 1 ~ \forall i$</td><td>$kw_i$から出る数は1以下 (4)</td></tr>
<tr><td>$\sum_j{x_{ji}} = 1 ~ \forall i$</td><td>$kw_i$へ入る数は1以下 (5)</td></tr>
<tr><td>$\sum_j{x_{ij}} \le \sum_j{x_{ji}} + y_i ~ \forall i$</td><td>$y$に関する制約 (6)
<tr><td>$z_i \le z_j + 1-(n+1)\times(1-x_{ij}) ~ \forall i, j$</td><td>$z$に関する制約 (7)</td></tr>
<tr><td>$\sum_i{y_i} = 1$</td><td>先頭は1つだけ (8)</td></tr>
</table>


# <i class='fa fa-chain' /> Pythonで解く
C++のキーワード84個を使ってみましょう。キーワードは、文字列の配列(kw)に入っているとします。

```py3:python
kw = "alignas,alignof,and,and_eq,asm,auto,bitand,bitor,bool,break,case," \
     "catch,char,char16_t,char32_t,class,compl,const,constexpr,const_cast," \
     "continue,decltype,default,delete,do,double,dynamic_cast,else,enum," \
     "explicit,export,extern,false,float,for,friend,goto,if,inline,int,long," \
     "mutable,namespace,new,noexcept,not,not_eq,nullptr,operator,or,or_eq," \
     "private,protected,public,register,reinterpret_cast,return,short," \
     "signed,sizeof,static,static_assert,static_cast,struct,switch,template," \
     "this,thread_local,throw,true,try,typedef,typeid,typename,union," \
     "unsigned,using,virtual,void,volatile,wchar_t,while,xor,xor_eq".split(',')
```

[pulp](http://qiita.com/Tsutomu-KKE@github/items/bfbf4c185ed7004b5721#%E3%82%BD%E3%83%95%E3%83%88%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)を使って定式化して解いてみましょう。

```py3:python
from pulp import * # pip install pulp
n, r = len(kw), range(len(kw))
m = LpProblem(sense=LpMaximize) # 数理モデル
x = [[0 if kw[i][-1] != kw[j][0] else LpVariable('x%d_%d'%(i,j), cat=LpBinary)
      for j in r] for i in r] # kw_i から kw_j に繋げるかどうか (1)
y = [LpVariable('y%d'%i, lowBound=0) for i in r] # kw_iが先頭かどうか (2)
z = [LpVariable('z%d'%i, lowBound=0) for i in r] # kw_iの順番 (3)
m += lpSum(x[i][j] for i in r for j in r) # なるべく繋げる (0)
for i in r:
    cou = lpSum(x[i][j] for j in r) # kw_i から出る数
    cin = lpSum(x[j][i] for j in r) # kw_i へ入る数
    m += cou <= 1 # kw_i から出る数は1以下 (4)
    m += cin <= 1 # kw_i へ入る数は1以下 (5)
    m += cou <= cin + y[i] # yに関する制約 (6)
    for j in r:
        m += z[i] <= z[j]-1+(n+1)*(1-x[i][j]) # zに関する制約 (7)
m += lpSum(y) == 1 # 先頭は1つだけ (8)
%time m.solve() # 求解
print(int(value(m.objective)) + 1) # 最長しりとり数
rr = range(1,n+1)
vx = np.vectorize(value)(x).astype(int)
i, s = 0, int(np.vectorize(value)(y)@rr)
while s:
    if i:
        print(' -> ', end='')
    i += 1
    print('[%d]%s'%(i,kw[s-1]), end=' ')
    s = vx[s-1]@rr
>>>
35
[1]alignas  -> [2]signed  -> [3]default  -> [4]typedef  -> 
[5]friend  -> [6]do  -> [7]operator  -> [8]reinterpret_cast  -> 
[9]thread_local  -> [10]long  -> [11]goto  -> [12]or  -> 
[13]register  -> [14]return  -> [15]new  -> [16]wchar_t  -> 
[17]true  -> [18]export  -> [19]throw  -> [20]while  -> 
[21]else  -> [22]enum  -> [23]mutable  -> [24]explicit  -> 
[25]this  -> [26]static  -> [27]class  -> [28]sizeof  -> 
[29]float  -> [30]template  -> [31]extern  -> [32]noexcept  -> 
[33]typeid  -> [34]dynamic_cast  -> [35]try
```
規模が大きい場合は、[最長しりとり問題の解法](http://ci.nii.ac.jp/naid/110002768734)を参考にしてください。

2017/1/16 追記
ループを含む解を避けるために、変数zを追加しました。ループがあると式(7)が成り立たなくなります。

参考:
[Pythonで最長駅名しりとりを探索してみた](https://qiita.com/hira_physics/items/60ee9eb31b60fba93d16)
[CodeIQ 「組合せ最適化：C++予約語から最長のしりとりを作ろう！」](https://codeiq.jp/magazine/2013/08/1710/)
[数独を組合せ最適で解く](http://qiita.com/SaitoTsutomu/items/4f919f453aae95b3834b)
[献立を組合せ最適化で考える](http://qiita.com/SaitoTsutomu/items/f8be15f56cbacdbb7bd9)
[洗濯物を干しながら最適化してみた](http://qiita.com/SaitoTsutomu/items/3b42fbbebb74463a24c5)

