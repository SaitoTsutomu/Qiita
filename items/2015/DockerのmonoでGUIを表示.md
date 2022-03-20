title: DockerのmonoでGUIを表示
tags: Ubuntu mono Docker
url: https://qiita.com/SaitoTsutomu/items/74d3e3d7d0d00f719cf0
created_at: 2015-11-24 08:57:49+09:00
updated_at: 2015-11-24 08:57:49+09:00
body:

http://postd.cc/running-gui-apps-with-docker/ を参考にUbuntu14.04 でC#のWindows.Formを動かしてみる。
「test」フォルダを作り下記の2ファイルを作成する。

```c#:test/test.cs
using System;
using System.Windows.Forms;
class Program
{
  [STAThread]
  static void Main(string[] args)
  {
    var frm = new Form();
    var btn = new Button();
    btn.Text = "Push!";
    btn.Click += delegate { MessageBox.Show("Hello"); };
    frm.Controls.Add(btn);
    Application.Run(frm);
  }
}
```

```test:test/Dockerfile 
FROM mono
 
# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/test && \
    echo "test:x:${uid}:${gid}:Test,,,:/home/test:/bin/bash" >> /etc/passwd && \
    echo "test:x:${uid}:" >> /etc/group && \
    chown ${uid}:${gid} -R /home/test
USER test
WORKDIR /home/test
COPY test.cs /home/test/
RUN mcs test.cs -r:/usr/lib/mono/4.5/System.Windows.Forms.dll
CMD mono test.exe
```

以下を実行すれば、起動する。

```bash:ubuntu
docker build -t test test
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro test
```

