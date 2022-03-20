title: Jupyterの小技4
tags: Python Jupyter アイデア大全 フィンケのあいまいな部品
url: https://qiita.com/SaitoTsutomu/items/34847c066880ebfdebf7
created_at: 2017-03-01 18:49:38+09:00
updated_at: 2017-10-18 11:02:18+09:00
body:

[Jupyterの小技3](http://qiita.com/Tsutomu-KKE@github/items/67ff53d58955082fd582)の続き
# これなに
下記の15個の図形から、ランダムに3個の絵を表示させます[^1]。

[^1]: 書籍「[アイデア大全](https://www.amazon.co.jp/dp/4894517450)」の「09 フィンケのあいまいな部品」参照。
<img src="https://qiita-image-store.s3.amazonaws.com/0/13955/da4f9bb9-2fa8-aab2-0f56-c6651fa07de9.png" width="70%">

準備として、まず、下記を実行してください。

```py3:jupyter_notebook
from IPython.display import display, SVG
import numpy as np, IPython.core.getipython
ss = """\
1/e50 50 50 50 url(#g) black 0.5
1/e50 50 50 50 url(#g)/r0 0 100 50 white/e 50 50 50 10 #E0E0E0 black 0.5
0/pM1,34_L35,10_L99,10_L66,34_L99,10_L99,75_L66,99 #E0E0E0 black 0.5/r1 34 65 65 #C0C0C0 black 0.5
0/e50 82 50 17 #E0E0E0 black 0.5/pM0,80_L50,0_L100,80 #E0E0E0 black 0.5
0/e90 50 10 30 #E0E0E0 black 0.5/pM90,20_L10,20_L10,80_L90,80 #E0E0E0 black 0.5/e10 50 10 30 #C0C0C0 black 0.5
0/pM10,70_C10,60_30,30_50,30_C70,40_50,60_70,70_C90,70_90,40_90,30 none black
0/pM10,70_C10,60_30,30_50,30_C70,40_50,60_70,70_C90,70_90,40_90,30 none black 10\
/pM10,69.2_C10,60_30,30_50,30_C70,40_50,60_70,70_C90,70_90,40_90,30.8 none white 8.4
0/pM0,70_L30,30_L100,30_L70,70_Z #E0E0E0 black 0.8
0/pM20,20_L20,80_L80,80 none black 10/pM20,21_L20,80_L79,80 none white 8.4
0/pM1,50_L80,25_L99,25_L25,50_M99,25_L99,50_L25,75_L25,50 #E0E0E0 black 0.5/r1 50 25 25 #C0C0C0 black 0.5
0/pM25,40_C50,-15_99,40_67,67_C60,70_50,80_50,98 none black 0.8/c 25 40 1.2/c 50 98 1.2
0/e20 39.5 16 24 gray black 0.5/e24 40 16 24 #C0C0C0 black 0.5/e24 40 2 3 #555/l24 40 84 60 gray 2\
/e80 59.5 16 24 gray black 0.5/e84 60 16 24 #C0C0C0 black 0.5/e84 60 2 3 #555
0/l10 10 90 90 black 10/l10.5 10.5 89.5 89.5 white 8.4/l10 90 90 10 black 10/l10.5 89.5 89.5 10.5 white 8.4
0/c50 50 40 none black 10/c50 50 40 none white 8.4
0/pM10,70_A40,40_0_0_1_90,70 none black 10/pM10,69.2_A40,39.2_0_0_1_90,69.2 none white 8.4""".splitlines()
tt = {
      'p':'path d fill stroke stroke-width'.split(),
      'l':'line x1 y1 x2 y2 stroke stroke-width'.split(),
      'c':'circle cx cy r fill stroke stroke-width'.split(),
      'e':'ellipse cx cy rx ry fill stroke stroke-width'.split(),
      'r':'rect x y width height fill stroke stroke-width'.split(),
}
def make_svg(ids, ss=ss, tt=tt):
    rs, n = [], len(ids)
    for i, j in enumerate(ids):
        rr = ['<g transform="translate(%d,0)">'%(i*120)]
        vv = ss[j].split('/')
        if vv[0] == '1':
            rr.append("""\
                <defs><radialGradient id="g" gradientUnits="userSpaceOnUse"
                  cx="50" cy="50" r="50" fx="20" fy="50">
                <stop offset="0%" stop-color="white" />
                <stop offset="100%" stop-color="gray" />
                </radialGradient></defs>""")
        for s in vv[1:]:
            uu = tt[s[0]]
            rr.append('<%s %s />'%(uu[0],' '.join('%s="%s"'%(u,
                a.replace('_',' ')) for u, a in zip(uu[1:], s[1:].split()))))
        rs.append('\n'.join(rr+['</g>']))
    return SVG('<svg width="%d" height="100">%s</svg>'%(n*120,'\n'.join(rs)))
def F_impl(s):
    return make_svg(np.random.choice(range(15), int(s) if s else 3, False))
ip = IPython.core.getipython.get_ipython()
if ip:
    ip.register_magic_function(F_impl, magic_name='F')
```

# 実行してみる

```py3:jupyter_notebook
F
```

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/e953b84f-a668-2e7c-da6f-0219525d71e7.png)


```py3:jupyter_notebook
F
```

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/661f7966-5cf9-6c57-8ac3-1f328930f216.png)


```py3:jupyter_notebook
for i in range(1,4):
    svg = %F {i}
    display(svg)
```

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/70fb29b6-1ddd-5b2e-d77a-b01ed0b3d164.png)


「{ }」で囲むと、先に評価(eval)できます。
また、一旦、結果を変数に保存して使うこともできます。

以上

