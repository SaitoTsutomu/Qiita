# このフォルダを OKF 化する検討

作成日: 2026-10-28 / 状態: 検討のみ(未実施)

## 前提

OKF は Google Cloud の Open Knowledge Format(2026年6月公開)と解釈した。AIエージェント向けの「Markdown ファイルのフォルダ + frontmatter + 相互リンク」の形式で、SDK は不要。仕様の細部は検索結果の要約だけで、原典は未確認。実施前に確認すること。

## 現状

- `items/<年>/<タイトル>.md` に Qiita 記事(2013〜2025年)が入っている。
- 各ファイルは `title: / tags: / url: / created_at: / updated_at: / body:` という独自のヘッダ形式。
- `items.md` が記事一覧。
- `src/downloads_all_items.py` が Qiita API から取得して書き出す。

OKF の形にかなり近い構造になっている。

## 方針

1. 取得スクリプトの `write_item` を YAML frontmatter 形式の出力に変える(`tags` は配列にする)。
2. `items.md` を `index.md` に置き換え、タイトル・タグ・1行要約を載せた目次にする。
3. 概念単位のページ(`tags/polars.md`、`topics/mcp.md` など)を足し、記事同士や概念ページへリンクする。
4. ファイル名を日本語タイトルから Qiita の記事IDかスラッグに変える。
5. README に OKF バンドルであることと再生成手順を書く。手書きの概念ページは生成物と分けて、再生成で消えないようにする。

## メリット

- AIエージェントが読みやすくなり、過去記事を RAG なしで渡せる。
- メタデータ(特にタグ)が機械可読になる。
- 概念ページがあると、古い記事の更新漏れや重複を見つけやすい。
- ツールに依存せず、普通の Markdown なので移行しやすい。

## デメリット

- 公開された OKF バンドルを自動で読むエージェントはまだほぼなく、効果が不確かな先行投資になる。
- Qiita が一次情報でここはバックアップなので、記事の保存先としては過剰。
- 概念ページの作成と保守に手間がかかる。自動生成すると、タグ集約程度の浅いものになる。
- 仕様が新しく、後で修正が必要になる可能性がある。
- ヘッダ形式とファイル名を変えると、全記事が差分になる。
- Qiita 記法(`:::note` など)や画像リンクは、そのままでは変わらない。

## おすすめ

小さく始めるなら、手順1・2・4(frontmatter 化、`index.md`、ID ファイル名)だけで十分。工数が小さく、元に戻しやすい。概念ページ(手順3)は、実際にエージェントから参照したい場面が出てからにする。

## 参考

- [Open Knowledge Format (OKF): Google's New Markdown Format for AI Agents](https://suganthan.com/blog/open-knowledge-format/)
- [Google Cloud's Open Knowledge Format (the-decoder)](https://the-decoder.com/google-clouds-open-knowledge-format-turns-scattered-docs-into-markdown-files-for-ai-agents/)
- [Open Knowledge Format (hjarni)](https://hjarni.com/docs/open-knowledge-format)
- [What Is OKF? (outcomeschool)](https://outcomeschool.com/blog/what-is-okf-open-knowledge-format)
