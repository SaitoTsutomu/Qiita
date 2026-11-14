title: Anaconda 2.5 Release
tags: Python Anaconda
url: https://qiita.com/SaitoTsutomu/items/c6676cba82cf46a3d0ea
created_at: 2016-02-16 10:43:19+09:00
updated_at: 2016-02-16 10:43:19+09:00
body:

# ニュース

Python科学技術計算ディストリビューションの[Anaconda](https://www.continuum.io/why-anaconda)の2.5がリリースされました。
[DEVELOPER BLOG](https://www.continuum.io/blog/developer-blog/anaconda-25-release-now-mkl-optimizations)によると、今まで有料版で提供されていたMKL(Intel Math Kernel Library)が無料版でも提供されるようになったようです。

どのくらい高速になったのか確認してみました。
これまでのOpenBLAS[^1]版とMKL版の[docker](https://hub.docker.com/r/tsutomu7/scientific-python/)を用意し、DigitalOceanの一番小さいやつで確認してみました。

[^1]: "conda install nomkl" とすれば OpenBLAS版になります。

2000×2000のランダムな行列の逆行列計算の時間を計ってみました。

```bash
$ docker run -it --rm tsutomu7/scientific-python python -m timeit -c \
         'import numpy as np; np.linalg.inv(np.random.rand(2000, 2000))'
10 loops, best of 3: 2.61 sec per loop

$ docker run -it --rm tsutomu7/scientific-python:mkl python -m timeit -c \
         'import numpy as np; np.linalg.inv(np.random.rand(2000, 2000))'
10 loops, best of 3: 1.61 sec per loop
```

40%ほど速くなったようです。

ちなみに、デフォルトで4コア並列実行可能です。4コアを超えて設定できないようです。

```py3:python
import mkl
mkl.get_max_threads()
>>>
4

mkl.set_num_threads(1)
mkl.get_max_threads()
>>>
1

mkl.set_num_threads(8)
mkl.get_max_threads()
>>>
4
```

以上

