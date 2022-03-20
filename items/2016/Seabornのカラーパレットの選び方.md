title: Seabornのカラーパレットの選び方
tags: Python seaborn
url: https://qiita.com/SaitoTsutomu/items/c79c9973a92e1e2c77a7
created_at: 2016-03-01 14:53:40+09:00
updated_at: 2020-01-28 09:05:36+09:00
body:

# <i class='fa fa-line-chart' /> はじめに
pythonの描画パッケージseabornの[Choosing color palettes](http://stanford.edu/~mwaskom/software/seaborn/tutorial/color_palettes.html)をまとめたものです。
[Jupyterファイル](http://nbviewer.jupyter.org/gist/Tsutomu-KKE/e578cc7b031795bdefdb)も用意してあります。

## <i class='fa fa-line-chart' /> 準備
```py3:python
%matplotlib inline
import seaborn as sns, numpy as np
from ipywidgets import interact, FloatSlider
```

## <i class='fa fa-line-chart' /> color_palette()を用いた作成方法<br />(Building color palettes with color_palette())
- color_paletteを用いると、ほとんどのカラーパレットを作成できます。
- set_paletteを用いると、デフォルトのカラーパレットを設定できます(例は後述)。

## <i class='fa fa-line-chart' /> 定性的なカラーパレット<br />(Qualitative color palettes)
- カラーパレット名を指定しないと、現在のカラーパレットが取得できます。(下記は、デフォルトのカラーパレット)
- palplotは、カラーパレットを表示します。

```py3:python
current_palette = sns.color_palette(n_colors=24)
sns.palplot(current_palette)
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/7440ea7b-2dd8-85e0-04d5-104570c8dc92.png)

デフォルトのカラーパレットは、6つのテーマ(deep, muted, pastel, bright, dark, colorblind)があります。(デフォルトはdeep)
Jupyterで、テーマをインタラクティブに確認できるようにしました。

```py3:python
def show_pal0(palette):
    sns.palplot(sns.color_palette(palette, 24))
interact(show_pal0, palette='deep muted pastel bright dark colorblind'.split());
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/51dd03da-e029-f882-fafb-b03e28991b8a.png)

## <i class='fa fa-line-chart' /> 色相カラーパレット<br />(Using circular color systems)
よく使われるのは、hlsです。color_paletteでも、hls_paletteでも作成できます。

```py3:python
sns.palplot(sns.color_palette("hls",24))
sns.palplot(sns.hls_palette(24))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/b4b291c5-ac68-8fbf-883a-2cc6e0c94c72.png)
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/b4b291c5-ac68-8fbf-883a-2cc6e0c94c72.png)

パラメータ l で明度を、s で彩度を指定できます。

```py3:python
sns.palplot(sns.hls_palette(24, l=0.2))
sns.palplot(sns.hls_palette(24, s=0.2))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/6766c741-a528-e330-6f40-43f9d336ea24.png)
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/b9459e9a-9853-49c2-bed3-ba2f65ec053c.png)

下記の様にするとくっきりしたカラーパレットになります。

```py3:python
sns.palplot(sns.hls_palette(24, l=0.5, s=1))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/7d03b0fc-41e1-1f78-1902-52c61ab84966.png)

Jupyterで、明度と彩度をインタラクティブに確認できるようにしました。

```py3:python
def show_pal1(l, s):
    sns.palplot(sns.hls_palette(24, l=l, s=s))
interact(show_pal1, l=FloatSlider(0.6, max=1), s=FloatSlider(0.65, max=1));
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/bb7196c4-a422-6b9e-7a98-53be4955343b.png)

hlsの色相ごとの明度のばらつきを少なくしたhuslも利用できます。

```py3:python
sns.palplot(sns.husl_palette(24))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/c105e567-e14a-d6e0-0946-83eff8864fde.png)

## <i class='fa fa-line-chart' /> カテゴリカラー<br />(Using categorical Color Brewer palettes)
名前のついたカラーパレットです。 少し古いですが、一覧([印刷用PDF](https://www.dropbox.com/s/8autfrvx6dpll96/pal.pdf))を用意しました。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/279e0621-678a-8345-49b5-d5af7dec1544.png)

参考：https://matplotlib.org/examples/color/colormaps_reference.html

```py3:python
sns.palplot(sns.color_palette("Set1", 24))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/b23dfc98-9436-9aa4-2d61-70100d207564.png)

Jupyterでは、簡単に確認できます。

```py3:python
sns.choose_colorbrewer_palette('qualitative');
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/4c455d11-b9e1-8781-0226-a36e3389a14a.png)

RGBで指定してカラーパレットを作成することもできます。

```py3:python
flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
sns.palplot(sns.color_palette(flatui, 24))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/c7f83704-ace3-fd13-28f7-8617e6801cb2.png)

## <i class='fa fa-line-chart' /> 連続カラーパレット<br />(Sequential color palettes)
- 特定の名前を指定すると、連続的なカラーパレットになります。
- 名前に"_d"をつけるとdarkになります。(つけないとlight)
- 名前に"_r"をつけると逆順になります。

```py3:python
sns.palplot(sns.color_palette("Blues", 24))
sns.palplot(sns.color_palette("Blues_d", 24))
sns.palplot(sns.color_palette("Blues_r", 24))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/185565f3-344c-d9a4-fc3b-79c6e9690630.png)
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/96e86db0-3dd3-6c51-089b-e5183081a9a3.png)
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/022a046e-d736-f0b5-e112-5c259e454b6a.png)

Jupyterでは、簡単に確認できます。

```py3:python
sns.choose_colorbrewer_palette('sequential');
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/3c4bd984-f031-1f7d-fa9c-8a9eb6d15305.png)

## <i class='fa fa-line-chart' /> cubehelix_paletteを用いた連続カラーパレット<br />(Sequential palettes with cubehelix_palette())

cubehelixを使って色調を変化させながら、明るさを連続的に変化させたカラーパレットを作成できます。

```py3:python
sns.palplot(sns.color_palette("cubehelix", 24))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/1e7c3041-f2c8-2389-b9bc-d397e09237dd.png)

cubehelix_paletteは、違うカラーパレットになるようです。

```py3:python
sns.palplot(sns.cubehelix_palette(24))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/6f55bced-24cd-0be1-0a6f-e5d23679b7cc.png)

as_cmap=Trueとすることで、cmapパラメータを持つグラフ描画で使えるようになります。

```py3:python
np.random.seed(1)
x, y = np.random.multivariate_normal([0, 0], [[1, -.5], [-.5, 1]], size=300).T
cmap = sns.cubehelix_palette(light=1, as_cmap=True)
sns.kdeplot(x, y, cmap=cmap, shade=True);
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/69aa2d3e-5aae-3100-aa7b-27146e245a0d.png)

Jupyterで、cubehelix_palette カラーパレットをインタラクティブに確認できるようにしました。

```py3:python
def show_pal2(start, rot):
    sns.palplot(sns.cubehelix_palette(24, start=start, rot=rot))
interact(show_pal2, start=FloatSlider(max=1), rot=FloatSlider(0.4, max=1));
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/a165973e-45d7-c398-8b6a-b26ca46b1322.png)

## <i class='fa fa-line-chart' /> カスタム連続カラーパレット<br />(Custom sequential palettes with light_palette() and dark_palette())

light_paletteやdark_paletteを使うこともできます。

```py3:python
sns.palplot(sns.light_palette("blue", 24))
sns.palplot(sns.dark_palette("blue", 24))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/ab7e2f81-c236-9077-75c4-ad072b9c9f44.png)
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/2e686455-522e-1f22-3041-64e35638c36d.png)

先ほどの図の等高線に使ってみましょう。

```py3:python
cmap = sns.dark_palette("palegreen", as_cmap=True)
sns.kdeplot(x, y, cmap=cmap);
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/8b14f0ba-8f99-22e0-cc2b-60aea463cfd7.png)

Jupyterで、インタラクティブに確認できるようにしました。

```py3:python
def show_pal3(light_or_dark, color, reverse):
    sns.palplot(eval('sns.%s_palette'%light_or_dark)(color=color, n_colors=24, reverse=reverse))
interact(show_pal3, light_or_dark=('light', 'dark'), color=('blue', 'navy', 'green', 'palegreen', 'red'), reverse=False);
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/036f8f45-2ef7-aa0a-4324-77b1c9c0b97e.png)


## <i class='fa fa-line-chart' /> 2色に分かれたカラーパレット<br />(Diverging color palettes)

両端が別の色で、中間が白色のカラーパレットです。
color_paletteで指定すれば作成できます。

```py3:python
sns.palplot(sns.color_palette("BrBG", 24))
sns.palplot(sns.color_palette("RdBu_r", 24))
sns.palplot(sns.color_palette("coolwarm", 24))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/e4d169b5-ce41-a94d-6eec-5b432c8e4737.png)
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/cadb60d9-5901-83c8-d29d-eca459dd33e9.png)
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/31fff8b8-c3e6-e5ee-65ee-406ed630835a.png)

Jupyterでは、簡単に確認できます。

```py3:python
sns.choose_colorbrewer_palette('diverging');
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/acacfd34-70fe-f278-9442-16dc67aee340.png)

## <i class='fa fa-line-chart' /> 2色に分かれたカスタムカラーパレット<br />(Custom diverging palettes with diverging_palette())

diverging_paletteでカスタムできます。
中間を暗くすることもできます。

```py3:python
sns.palplot(sns.diverging_palette(220, 20, n=24))
sns.palplot(sns.diverging_palette(145, 280, s=85, l=25, n=24))
sns.palplot(sns.diverging_palette(255, 133, l=60, n=24, center="dark"))
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/c6045d9c-e545-53af-aa0d-e35729ec4637.png)
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/36fa462b-6cf3-5b8f-ec3d-f4562024eccb.png)
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/2939b275-a190-430d-a9b9-6d72e98b6a0f.png)

Jupyterで、インタラクティブに確認できるようにしました。

```py3:python
def show_pal4(h_neg, h_pos, s, l, center):
    sns.palplot(sns.diverging_palette(h_neg, h_pos, n=24, s=s, l=l, center=center))
interact(show_pal4, h_neg=FloatSlider(220, max=360), h_pos=FloatSlider(20, max=360), 
         s=FloatSlider(75, max=99), l=FloatSlider(50, max=99), center=('light', 'dark'));
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/0ef54c48-bcb4-ad2c-dba7-f88412f0bf17.png)

## <i class='fa fa-line-chart' /> デフォルトカラーパレットの設定<br />(Changing default palettes with set_palette())

set_paletteでデフォルトカラーパレットを設定できます。
設定なしで描画します。

```py3:python
def sinplot(flip=1):
    x = np.linspace(0, 14, 100)
    for i in range(1, 7):
        plt.plot(x, np.sin(x + i * .5) * (7 - i) * flip)

sinplot()
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/161b4359-af71-6cd4-0410-dd65cd37a5b9.png)

設定して描画します。

```py3:python
sns.set_palette("husl")
sinplot()
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/dcb9f275-34c1-207c-7ac4-6b5d74c8fc7a.png)

with句を使うと、局所的に変更できます。

```py3:python
with sns.color_palette("PuBuGn_d"):
    sinplot()
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/5f1d9889-6bb3-d23b-1c0b-8e488f618dbe.png)

以上

