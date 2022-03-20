title: PDFにページ番号を追加
tags: Python PDF reportlab PyPDF2 pdfformfiller
url: https://qiita.com/SaitoTsutomu/items/5a7bb9ae2e60b327a311
created_at: 2017-02-01 10:36:53+09:00
updated_at: 2018-09-23 01:06:11+09:00
body:

# これなに
**Python** を使って、**無料で PDF を編集する方法** を紹介します。
サンプルとして、各ページにページ番号を追加してみます。

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/15a7359a-2eb4-d8eb-1df5-101ef461a52c.png)

# インストール
下記を使用します。

- [ReportLab](http://www.reportlab.com/): Python用、PDF生成ライブラリ。有料版と無料版がある。
- [PyPDF2](http://pythonhosted.org/PyPDF2/): Page単位のPDF編集ライブラリ。
- [PdfFormFiller](https://pdfformfiller.readthedocs.io/en/latest/): PDFにテキストを挿入するライブラリ。

```bash:インストール
conda install -y reportlab
pip install PyPDF2 pdfformfiller
```

[Anaconda](https://www.continuum.io/downloads) を使っていない場合は、conda の代わりに pip を使ってください。

# ページ番号を追加するサンプル
日本語フォントとして、[IPAexGothic フォント](http://ipafont.ipa.go.jp/)を使っていますが、別のフォントでも構いません。
(Ubuntu では、apt-get install fonts-ipaexfont でインストールできます)

注意点として、用紙サイズを表す PyPDF2.pdf.PageObject.mediaBox の要素である FloatObject が Decimalを返すため、実数との加減演算でエラーになります。ここでは、無理やり、FloatObject が実数と加減演算できるように置き換えています。

addPage(入力ファイル, 出力ファイル) とすると、元のPDFに、ページ番号を追加したPDFを作成できます。

```py3:python
import PyPDF2
class FloatObject(PyPDF2.generic.FloatObject):
    def __add__(self, other):
        return self.as_numeric() + other
    def __radd__(self, other):
        return self.as_numeric() + other
    def __sub__(self, other):
        return self.as_numeric() - other
    def __rsub__(self, other):
        return -self.as_numeric() + other
PyPDF2.generic.FloatObject = FloatObject

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfformfiller import PdfFormFiller

def addPage(infile, outfile):
    # Linuxでは、'/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'など
    pdfmetrics.registerFont(TTFont('IPAexGothic', 'c:/Windows/Fonts/ipaexg.ttf'))
    sty = ParagraphStyle('sty', alignment=TA_CENTER, fontName='IPAexGothic', fontSize=9)
    ff = PdfFormFiller(infile)
    for i in range(ff.pdf.getNumPages()):
        p = ff.pdf.getPage(i)
        ff.add_text('ページ %d'%(i+1), i, (0,p.mediaBox[3]-30), p.mediaBox.getUpperRight(), sty)
    ff.write(outfile)
```

- Windows, Ubuntu, Alpine-Linux で稼働確認しています。

### 追記

パッケージ化しました。

https://pypi.org/project/addpage/

以上

