title: Jupyterの小技
tags: Python pandas Jupyter
url: https://qiita.com/SaitoTsutomu/items/aa19a152dd8c80824d95
created_at: 2016-06-21 10:02:10+09:00
updated_at: 2017-09-20 19:12:43+09:00
body:

# これなに
Python3 のJupyter(IPython notebook)で、以下の方法をご紹介します。

- pandasの大きいDataFrameを省略せずに表示
- ジェネレーターの展開
- Notebookの横幅を広げる
- DataFrameのインデックスを非表示に

## 準備
最初に、more-itertools をインストールしてください。

```bash:bash
pip install more-itertools
```

次に、下記を実行してください。または、<ユーザのディレクトリ>/.ipython/profile_default/startup に下記の内容のファイルを置いてください。

```py3:jupyter
import IPython.core.getipython
from more_itertools import chunked
ip = IPython.core.getipython.get_ipython()
class ChunkedDataFrame:
    def __init__(self, *args): self.df, self.n, self.m = args
    def _repr_html_(self):
        return ('' if not isinstance(self.df, pd.DataFrame) else
            '\n'.join(self.df.iloc[:self.m, r]._repr_html_()
                      for r in chunked(range(self.df.shape[1]), self.n)))
def C_impl(self, args):
    return ChunkedDataFrame(_, *[int(i) for i in (args+' 12 5').split()[:2]])
def L_impl(self, args):
    print(list(_))
if ip:
    ip.define_magic('C', C_impl)
    ip.define_magic('L', L_impl)
```

## pandasの大きいDataFrameを省略せずに表示
ダミーのDataFrameを表示してみましょう。

```py3:jupyter
import numpy as np, pandas as pd
a = pd.DataFrame(np.random.randint(0, 100, (3, 24)))
a
```

<table>
    <tr>
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>14</th>
      <th>15</th>
      <th>16</th>
      <th>17</th>
      <th>18</th>
      <th>19</th>
      <th>20</th>
      <th>21</th>
      <th>22</th>
      <th>23</th>
    </tr>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>30</td>
      <td>60</td>
      <td>68</td>
      <td>53</td>
      <td>81</td>
      <td>60</td>
      <td>10</td>
      <td>49</td>
      <td>28</td>
      <td>...</td>
      <td>49</td>
      <td>84</td>
      <td>24</td>
      <td>92</td>
      <td>6</td>
      <td>54</td>
      <td>52</td>
      <td>60</td>
      <td>52</td>
      <td>71</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18</td>
      <td>86</td>
      <td>70</td>
      <td>14</td>
      <td>10</td>
      <td>51</td>
      <td>94</td>
      <td>10</td>
      <td>9</td>
      <td>46</td>
      <td>...</td>
      <td>90</td>
      <td>81</td>
      <td>22</td>
      <td>65</td>
      <td>50</td>
      <td>93</td>
      <td>28</td>
      <td>83</td>
      <td>71</td>
      <td>22</td>
    </tr>
    <tr>
      <th>2</th>
      <td>62</td>
      <td>58</td>
      <td>42</td>
      <td>79</td>
      <td>83</td>
      <td>71</td>
      <td>22</td>
      <td>44</td>
      <td>7</td>
      <td>52</td>
      <td>...</td>
      <td>54</td>
      <td>63</td>
      <td>93</td>
      <td>14</td>
      <td>8</td>
      <td>54</td>
      <td>55</td>
      <td>73</td>
      <td>0</td>
      <td>26</td>
    </tr>
  </tbody>
</table>

途中が省略されています。DataFrame表示に続けて、以下のように実行します。

```py3:jupyter
%C
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>30</td>
      <td>60</td>
      <td>68</td>
      <td>53</td>
      <td>81</td>
      <td>60</td>
      <td>10</td>
      <td>49</td>
      <td>28</td>
      <td>78</td>
      <td>93</td>
    </tr>
    <tr>
      <th>1</th>
      <td>18</td>
      <td>86</td>
      <td>70</td>
      <td>14</td>
      <td>10</td>
      <td>51</td>
      <td>94</td>
      <td>10</td>
      <td>9</td>
      <td>46</td>
      <td>14</td>
      <td>19</td>
    </tr>
    <tr>
      <th>2</th>
      <td>62</td>
      <td>58</td>
      <td>42</td>
      <td>79</td>
      <td>83</td>
      <td>71</td>
      <td>22</td>
      <td>44</td>
      <td>7</td>
      <td>52</td>
      <td>3</td>
      <td>76</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>12</th>
      <th>13</th>
      <th>14</th>
      <th>15</th>
      <th>16</th>
      <th>17</th>
      <th>18</th>
      <th>19</th>
      <th>20</th>
      <th>21</th>
      <th>22</th>
      <th>23</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>3</td>
      <td>49</td>
      <td>84</td>
      <td>24</td>
      <td>92</td>
      <td>6</td>
      <td>54</td>
      <td>52</td>
      <td>60</td>
      <td>52</td>
      <td>71</td>
    </tr>
    <tr>
      <th>1</th>
      <td>17</td>
      <td>78</td>
      <td>90</td>
      <td>81</td>
      <td>22</td>
      <td>65</td>
      <td>50</td>
      <td>93</td>
      <td>28</td>
      <td>83</td>
      <td>71</td>
      <td>22</td>
    </tr>
    <tr>
      <th>2</th>
      <td>37</td>
      <td>28</td>
      <td>54</td>
      <td>63</td>
      <td>93</td>
      <td>14</td>
      <td>8</td>
      <td>54</td>
      <td>55</td>
      <td>73</td>
      <td>0</td>
      <td>26</td>
    </tr>
  </tbody>
</table>

12列ずつ表示されます。列数を変えたいときは、"%C 8"のように指定できます。もう一度、DataFrameを表示してから、やってみましょう。

```py3:jupyter
a
```

```py3:jupyter
%C 8
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>80</td>
      <td>61</td>
      <td>53</td>
      <td>28</td>
      <td>36</td>
      <td>56</td>
      <td>94</td>
      <td>72</td>
    </tr>
    <tr>
      <th>1</th>
      <td>41</td>
      <td>75</td>
      <td>74</td>
      <td>58</td>
      <td>86</td>
      <td>82</td>
      <td>92</td>
      <td>26</td>
    </tr>
    <tr>
      <th>2</th>
      <td>16</td>
      <td>40</td>
      <td>97</td>
      <td>14</td>
      <td>73</td>
      <td>54</td>
      <td>33</td>
      <td>87</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
      <th>13</th>
      <th>14</th>
      <th>15</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>81</td>
      <td>20</td>
      <td>16</td>
      <td>37</td>
      <td>39</td>
      <td>5</td>
      <td>8</td>
      <td>34</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>0</td>
      <td>43</td>
      <td>16</td>
      <td>5</td>
      <td>46</td>
      <td>25</td>
      <td>25</td>
    </tr>
    <tr>
      <th>2</th>
      <td>60</td>
      <td>42</td>
      <td>72</td>
      <td>43</td>
      <td>44</td>
      <td>70</td>
      <td>58</td>
      <td>42</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>16</th>
      <th>17</th>
      <th>18</th>
      <th>19</th>
      <th>20</th>
      <th>21</th>
      <th>22</th>
      <th>23</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>71</td>
      <td>41</td>
      <td>60</td>
      <td>32</td>
      <td>69</td>
      <td>79</td>
      <td>23</td>
      <td>79</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>71</td>
      <td>92</td>
      <td>31</td>
      <td>25</td>
      <td>26</td>
      <td>6</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>61</td>
      <td>10</td>
      <td>35</td>
      <td>81</td>
      <td>50</td>
      <td>60</td>
      <td>68</td>
      <td>81</td>
    </tr>
  </tbody>
</table>

第2引数で行数を変えることもできます。

```py3:jupyter
a
```

```py3:jupyter
%C 8 2
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>80</td>
      <td>61</td>
      <td>53</td>
      <td>28</td>
      <td>36</td>
      <td>56</td>
      <td>94</td>
      <td>72</td>
    </tr>
    <tr>
      <th>1</th>
      <td>41</td>
      <td>75</td>
      <td>74</td>
      <td>58</td>
      <td>86</td>
      <td>82</td>
      <td>92</td>
      <td>26</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
      <th>13</th>
      <th>14</th>
      <th>15</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>81</td>
      <td>20</td>
      <td>16</td>
      <td>37</td>
      <td>39</td>
      <td>5</td>
      <td>8</td>
      <td>34</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>0</td>
      <td>43</td>
      <td>16</td>
      <td>5</td>
      <td>46</td>
      <td>25</td>
      <td>25</td>
    </tr>
  </tbody>
</table>
<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>16</th>
      <th>17</th>
      <th>18</th>
      <th>19</th>
      <th>20</th>
      <th>21</th>
      <th>22</th>
      <th>23</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>71</td>
      <td>41</td>
      <td>60</td>
      <td>32</td>
      <td>69</td>
      <td>79</td>
      <td>23</td>
      <td>79</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>71</td>
      <td>92</td>
      <td>31</td>
      <td>25</td>
      <td>26</td>
      <td>6</td>
      <td>3</td>
    </tr>
  </tbody>
</table>

## ジェネレーターの展開
ジェネレーターをそのまま見ると、中味がわかりません。"list(_)"とすれば、いいのですが、2文字で済むようにしてみました。

```py3:jupyter
(i for i in range(10))
>>>
<generator object <genexpr> at 0x000000000XXXX>
```

```py3:jupyter
%L
>>>
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## Notebookの横幅を広げる

```py3:jupyter
%%HTML
<style>
    div#notebook-container    { width: 95%; }
    div#menubar-container     { width: 65%; }
    div#maintoolbar-container { width: 99%; }
</style>
```

## DataFrameのインデックスを非表示に

```py3:jupyter
df.style.set_table_styles([{'selector': 'tbody th', 'props': [('visibility','hidden')]}])
```

## 参考
- [IPythonで、値を見ようと思ったらジェネレータだったのでイラッとしたときに思いついたこと。](http://qiita.com/gyu-don/items/bac097407000185659d7)
- [pandasで表示が省略されるのを防ぐ](http://uyamazak.hatenablog.com/entry/2016/09/29/163534)

以上

