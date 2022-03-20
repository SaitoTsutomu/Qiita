title: 別exeの実行状況を画面(textBox1)に非同期に表示する
tags: C# 非同期処理
url: https://qiita.com/SaitoTsutomu/items/8726ab528dfe9f0a0ae9
created_at: 2013-01-06 11:04:52+09:00
updated_at: 2013-01-06 11:04:52+09:00
body:

```c#:C#
private IAsyncResult sr;
private Process pr = new Process();
private byte[] bb = new byte[4096];
private void callback(object o)
{
  int n = pr.StandardOutput.BaseStream.EndRead(sr);
  var s = Encoding.GetEncoding(932).GetString(bb, 0, n);
  textBox1.Text += s;
  textBox1.SelectionStart = textBox1.Text.Length - 1;
  textBox1.ScrollToCaret();
  if (n == 0) return;
  sr = pr.StandardOutput.BaseStream.BeginRead(bb, 0, bb.Length, callback, null);
}
private void button1_Click(object sender, EventArgs e)
{
  pr.StartInfo.FileName = XXX;
  pr.StartInfo.RedirectStandardOutput = true;
  pr.StartInfo.UseShellExecute = false;
  pr.Start();
  sr = pr.StandardOutput.BaseStream.BeginRead(bb, 0, bb.Length, callback, null);
  pr.WaitForExit();
}
```
