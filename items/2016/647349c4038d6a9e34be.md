title: geopandasを使ってみる
tags: Python Docker GIS
url: https://qiita.com/SaitoTsutomu/items/647349c4038d6a9e34be
created_at: 2016-08-30 16:37:15+09:00
updated_at: 2016-08-30 20:34:09+09:00
body:

# これなに
[PyData.Tokyo Meetup #9 -「地理情報データ」](http://pydatatokyo.connpass.com/event/38198/)で紹介されていた **geopandas** を[StatsFragments](http://sinhrks.hatenablog.com/entry/2015/07/18/215951) を参考に試してみました。

# インストール
Anaconda入れて、[Anaconda cloud](https://anaconda.org/) の conda-forge 使えば簡単。下記のコマンド一発[^1]。

```bash:bash
conda install -y geopandas -c conda-forge
```

Dockerイメージ[tsutomu7/geopandas](https://hub.docker.com/r/tsutomu7/geopandas/)も用意しました。下記のようにすればできるはず。(Jupyterサーバー起動後にブラウザを更新してください)

```bash:bash
firefox http://localhost:8888 &
docker run -it --rm -p 8888:8888 tsutomu7/geopandas sh -c "jupyter notebook --ip=*"
```

# Jupyterで試してみる
準備。flattenは、配列の配列を配列にするもの。

```py3:python3
%matplotlib inline
import numpy as np, pandas as pd, geopandas as gpd
from bokeh.plotting import output_notebook, show, figure
output_notebook()
flatten = lambda i: [a for b in i for a in (flatten(b) if hasattr(b,'__iter__') else (b,))]
```

geopandas のバージョンは、0.2.1 で現時点で最新。

```py3:python3
gpd.__version__
>>>
'0.2.1'
```

東京のデータを地球地図日本からダウンロード。

```py3:python3
!wget --no-check-certificate https://github.com/dataofjapan/land/raw/master/tokyo.geojson
```

最初の3行を見てみる。

```py3:python3
df = gpd.read_file('tokyo.geojson')
df[:3]
```

 |area_en|area_ja|code|geometry|ward_en|ward_ja
:--|:--|:--|:--|:--|:--|:--
0|Tokubu|都区部|131211.0|POLYGON ((139.821051 35.815077, 139.821684 35....|Adachi Ku|足立区
1|Tokubu|都区部|131059.0|POLYGON ((139.760933 35.732206, 139.761002 35....|Bunkyo Ku|文京区
2|Tokubu|都区部|131016.0|POLYGON ((139.770135 35.705352, 139.770172 35....|Chiyoda Ku|千代田区

geometry にポリゴンデータが入っています。
matplotlib で描画。

```py3:python3
df[df['area_en'] == 'Tokubu'].plot();
```

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/eeb465cf-7bc1-2a3d-0328-9550b681ca44.png)

今度は、bokehで描画。
geometryのポリゴンは、shapely.geometry.polygon.Polygon と shapely.geometry.multipolygon.MultiPolygon が混じっているので、flattenでPolygonの配列にします。

```py3:python3
xy = [i.exterior.coords.xy for i in flatten(df[df.area_en == 'Tokubu'].geometry)]
p = figure(plot_width=400, plot_height=300)
p.patches([tuple(i[0]) for i in xy], [tuple(i[1]) for i in xy], 
          fill_color='white', line_color="black", line_width=0.5)
show(p);
```

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/5ae4cb3b-97f5-6915-5c7a-125a41829102.png)

Geocodingはうまくいきませんでした。

参考リンク

- [Python geopandas + Bokeh で地理情報をプロットしたい](http://sinhrks.hatenablog.com/entry/2015/07/18/215951)
- [GeoPandas Doc](http://geopandas.org/)
- [GeoPandas PyPI](https://pypi.python.org/pypi/geopandas/)
- [PythonとQGISを使って地理空間を可視化する – UFO目撃情報でのケーススタディ](http://postd.cc/using-python-and-qgis-for-geospatial-visualizations-a-case-study/)
- [PyData.Tokyo Meetup #9 -「地理情報データ」](http://pydatatokyo.connpass.com/event/38198/)
- [Anaconda cloud](https://anaconda.org/)
- [Pythonで地理情報をプロットする](http://qiita.com/K-1/items/dacb66fed98c2d738963)
- [地球地図日本](http://www.gsi.go.jp/kankyochiri/gm_jpn.html)
- [AnacondaのJupyter notebookでnbextensionsを使う](http://qiita.com/Tsutomu-KKE@github/items/1326e05eb992a8aa849d)
- [tsutomu7/geopandas/](https://hub.docker.com/r/tsutomu7/geopandas/)

[^1]: "conda install -y pyproj shapely fiona; pip install geopandas" でもできました。

以上

