title: MinIOで簡単AWS S3のテスト
tags: Python AWS S3 Docker minio
url: https://qiita.com/SaitoTsutomu/items/a64c4cd37bd5a61a70ca
created_at: 2020-08-29 14:22:29+09:00
updated_at: 2020-08-29 14:22:29+09:00
body:

# はじめに

AWS S3のテストをしたいときに、[MinIO](https://github.com/minio/minio#minio-quickstart-guide)を使って、ローカルにS3のモックを建てる方法を紹介します。

## MinIOサーバーの起動

MinIOは、下記を実行するだけで（インストールせずに）利用できます。

```bash
docker run -d -p 9000:9000 --name minio -v $PWD/data:/data \
  -e "MINIO_ACCESS_KEY=AKIA0123456789ABCDEF" \
  -e "MINIO_SECRET_KEY=0123456789/abcdefghi/ABCDEFGHI0123456789" \
  minio/minio server /data
```

- `MINIO_ACCESS_KEY`と`MINIO_SECRET_KEY`は20文字と40文字で適宜変更してください。
- `http://127.0.0.1:9000`でブラウザで管理できます。
- S3の内容はカレントディレクトリの`data`に作成されます。

## 環境変数によるboto3のサンプル

### 準備

```py
import os
import boto3

bucket_name = 'sample'  # バケット名
use_minio = True  # MinIOを使うかどうか
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIA0123456789ABCDEF'
os.environ['AWS_SECRET_ACCESS_KEY'] = '0123456789/abcdefghi/ABCDEFGHI0123456789'
```

環境変数`AWS_ACCESS_KEY_ID`と`AWS_SECRET_ACCESS_KEY`にdockerで指定したものが入っているとします。

### バケットの作成

```py
kwargs = dict(
    region_name="ap-northeast-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

if use_minio:
    kwargs["endpoint_url"] = "http://127.0.0.1:9000"

bucket = boto3.resource("s3", **kwargs).Bucket(bucket_name)
```

MinIOを使う場合は、`endpoint_url`に`"http://127.0.0.1:9000"`を指定するだけで切り替えられます。

※ docker-composeを使う場合、`127.0.0.1`にはサービス名を指定します。


### 実行サンプル

カレントディレクトリにファイル`test_file`が存在するとします。

```py
bucket.create()  # バケット作成
bucket.upload_file("test_file", "upload_file")  # upload_fileとしてアップロード
print(list(bucket.objects.all()))  # ファイル一覧
bucket.download_file("upload_file", "download_file")  # download_fileとしてダウンロード
bucket.Object("upload_file").delete()  # ファイル削除
bucket.delete()  # バケット削除
```

通常のS3と同じように動作します。
適宜、`http://127.0.0.1:9000`で確認してください。

## プロフィールによるboto3のサンプル

環境変数を使うよりプロフィールを使う方法をおすすめします。

### 準備

- [aws CLI](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/install-cliv2.html)をインストールしてください。
- `aws configure --profile test`でプロフィールを作成してください。`test`は適宜変えてください。

### バケットの作成

作成したプロフィールを使ってバケットを作成します。
MinIOを使う場合は、`profile_name`と`endpoint_url`を指定することになります。

```py
profile_name = "test"

cr = boto3.Session(profile_name=profile_name).get_credentials()
kwargs = dict(aws_access_key_id=cr.access_key, aws_secret_access_key=cr.secret_key)

if use_minio:
    kwargs["endpoint_url"] = "http://localhost:9000"

bucket = boto3.resource("s3", **kwargs).Bucket(bucket_name)
```

作成したバケットは、前サンプルと同じように使えます。

以上

