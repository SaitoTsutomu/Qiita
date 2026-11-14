title: AWS CDK (Python) と LocalStack で作る！サーバーレスAPIローカル開発環境
tags: Python AWS Docker LocalStack CDK
url: https://qiita.com/SaitoTsutomu/items/02f628b7a03f758b4c18
created_at: 2025-08-21 19:34:58+09:00
updated_at: 2025-08-22 09:39:26+09:00
body:

## はじめに

「AWS CDK を試してみたいけれど、いきなり実際の AWS アカウントを使うのは少し不安…」

そんなときに大活躍するのが **LocalStack** です。LocalStack を使えば、AWS の主要なサービスをご自身のPC（ローカル環境）に再現でき、AWS の利用料金を気にすることなく、CDK のデプロイやテストを安全に試せます。

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9dc86914-de6c-4ee7-a7e3-d16dae259120.jpeg)

この記事では、**AWS CDK (Python)とLocalStack** を組み合わせ、**S3・Lambda・API Gateway** で構成されるシンプルなサーバーレスAPIを構築し、動作確認するまでの一連の手順を解説します。

**対象読者**

* AWS CDK を Python で学んでみたい方
* LocalStack を使って、ローカル環境で AWS 開発を体験したい方
* CDK を用いたインフラ構築の基本的な流れを理解したい方

**前提知識**

* Python と仮想環境（venv）の基本的な操作
* Docker および Docker Compose が利用できる環境
* AWS CLI のインストールと基本的なコマンドの知識

**参考リンク**

https://www.localstack.cloud/

https://github.com/localstack/localstack

https://github.com/localstack/aws-cdk-local

## 環境準備

まず、開発に必要なツールを準備します。

**Node.js / npm の準備**

AWS CDK は Node.js を利用するため、インストールと最新化を行います。バージョン管理ツール `nvm` を使うのがおすすめです。

```shell
# nvm を使って最新のLTS版をインストール
nvm install --lts
nvm use --lts

# npm自体も最新化しておく
npm install -g npm@latest

# バージョン確認
npm -v  # 例: 11.5.2
node -v  # 例: v22.18.0
```

**AWS CDK / cdklocal のインストール**

次に、AWS CDK 本体と、LocalStack と連携するためのラッパーツール `aws-cdk-local` をグローバルにインストールします。

```shell
npm install -g aws-cdk aws-cdk-local

# インストールされたか確認
cdklocal -v
# cdklocal v3.0.1
# cdk cli version v2.1025.0
```

## LocalStack の起動

次に、ローカルAWS環境である LocalStack を Docker Compose を使って起動します。

**`compose.yaml`の作成**

プロジェクトのルートディレクトリに、以下の内容で `compose.yaml` ファイルを作成します。

```shell
services:
  localstack:
    image: localstack/localstack
    ports:
      - "4566:4566"
      - "4510-4559:4510-4559"
    environment:
      - SERVICES=s3,dynamodb,lambda,apigateway,iam,sts,cloudformation,ssm,logs
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
```

**LocalStackの起動**

`compose.yaml`があるディレクトリで、以下のコマンドを実行します。

```shell
docker compose up -d
```

コンテナが起動し、ローカルでAWS APIが利用できるようになります。

## CDK プロジェクトの作成

作業用ディレクトリを作り、CDK の Python アプリを初期化します。

```shell
mkdir cdk
cd cdk

# Python言語でCDKアプリを初期化
cdklocal init app --language python

# チュートリアル説明を非表示
cdklocal acknowledge 34892

# 仮想環境の有効化
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt awscli-local
```

**ローカル環境向けの設定**

ターミナルで以下の環境変数を設定し、AWS CLI や CDK が LocalStack を向くようにします。

```shell
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_ENDPOINT_URL_S3=http://s3.localhost.localstack.cloud:4566
```

:::note info
LocalStackのS3を`virtual-hosted-style`で利用する場合は`s3.localhost.localstack.cloud`を使うのが推奨です。
:::

## CDK スタックの作成とデプロイ

`app.py`を以下のように編集し、インフラ構成を定義します。

```python
from aws_cdk import App, Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as s3
from constructs import Construct


class LocalStackCdkApp(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3バケット
        s3.Bucket(self, "MyBucket")

        # Lambda関数
        lambda_function = _lambda.Function(
            self,
            "MyLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_inline("""
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda'
    }"""),
        )

        # API Gateway
        apigateway.LambdaRestApi(self, "MyApi", handler=lambda_function)


app = App()
LocalStackCdkApp(app, "LocalStackCdkApp")
app.synth()
```

**LocalStack へのデプロイ**

定義したスタックを LocalStack にデプロイします。

```shell
# 初回のみCDKのブートストラップを実行
cdklocal bootstrap

# スタックをデプロイ（途中で差分が表示され、承認を求められたら 'y' を入力）
cdklocal deploy
```

:::note info
`cdklocal ls`で表示されるスタック名を指定して
`cdklocal deploy スタック名`でもデプロイ可能です。
:::

## 動作確認

デプロイした各リソースが正しく動作するか、AWS CLI を使って確認します。

**S3 バケットの確認**

```shell
# バケット名取得
BUCKET_NAME=$(awslocal cloudformation list-stack-resources \
  --stack-name LocalStackCdkApp --query \
  "StackResourceSummaries[?starts_with(LogicalResourceId, 'MyBucket')].PhysicalResourceId" \
  --output text)

# 適当なファイルをアップロード
touch dummy.txt
awslocal s3 cp dummy.txt s3://$BUCKET_NAME

# アップロードされたことを確認
awslocal s3 ls s3://$BUCKET_NAME
```

**Lambda関数の実行**

```shell
# 関数名取得
FUNC_NAME=$(awslocal lambda list-functions --query \
  "Functions[0].FunctionName" --output text)

# 実行
awslocal lambda invoke --function-name $FUNC_NAME output.json
cat output.json
```

**API Gatewayの動作確認**

```shell
# URL取得
API_URL=$(awslocal cloudformation describe-stacks \
  --stack-name LocalStackCdkApp --query \
  "Stacks[0].Outputs[0].OutputValue" --output text)

# 実行
curl $API_URL
```

## まとめ

この記事では、AWS CDK (Python) と LocalStack を使って、サーバーレスAPIをローカル環境に構築し、動作確認する手順を紹介しました。

LocalStack を活用することで、**実際のAWS環境や料金を気にすることなく**、手軽に CDK のコーディングとデプロイのサイクルを試すことができます。インフラのコード化（IaC）の学習や、新しいAWSサービスの検証に非常に役立ちますので、ぜひ活用してみてください。

