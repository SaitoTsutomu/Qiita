title: pandasのtips
tags: Python tips pandas 高速化
url: https://qiita.com/SaitoTsutomu/items/7881cf3499f513fcdbe2
created_at: 2017-09-26 10:08:31+09:00
updated_at: 2017-09-26 10:08:31+09:00
body:

# pandasの効率的な書き方

## なるべくforを使わない

pandasのベースはnumpyなので、numpyのテクニックが有効です。

例として、下記の表xの行の積の和を求めたいとします。

```py3:jupyter
x = pd.DataFrame(np.random.rand(100000,3),columns=list('abc'))
x[:3] # 先頭3行
```

<table>
  <thead>
    <tr>
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.902417</td>
      <td>0.443804</td>
      <td>0.678391</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.873176</td>
      <td>0.405184</td>
      <td>0.845241</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.050312</td>
      <td>0.040537</td>
      <td>0.686412</td>
    </tr>
  </tbody>
</table>

下記のように for を使うことなく計算できます。

```py3:jupyter
%%time
print((x.a*x.b*x.c).sum())
>>>
12501.777226525046
Wall time: 7 ms
```


## DataFrameやSeriesを通して頻繁にアクセスしない

先ほどの例で、forで**行ベースで計算しないといけない場合**も、工夫次第で高速化できます。
行ベースで、よく使うのは、iterrows() でしょう。

```py3:jupyter
%%time
s = 0
for _,r in x.iterrows():
    s += r.a*r.b*r.c
print(s)
>>>
12501.7772265
Wall time: 5.71 s
```

forを使わない場合より 3桁遅いです。
DataFrameは、列(Series)で構成されているので、各Seriesをzipにした方が、まだ高速です。

```py3:jupyter
%%time
s = 0
for a,b,c in zip(x.a,x.b,x.c):
    s += a*b*c
print(s)
>>>
12501.7772265
Wall time: 111 ms
```

次によく使うのは、index参照でしょう。

```py3:jupyter
%%time
s = 0
for i in range(len(x)):
    s += x.a[i]*x.b[i]*x.c[i]
print(s)
>>>
12501.7772265
Wall time: 4.59 s
```

速度的には、iterrows()と同じくらいです。
Seriesを通すと遅いので、先にlistにすると高速化できます。

```py3:jupyter
%%time
s = 0
a,b,c = x.a.tolist(),x.b.tolist(),x.c.tolist()
for i in range(len(x)):
    s += a[i]*b[i]*c[i]
print(s)
>>>
12501.777226525046
Wall time: 66 ms
```

以上

