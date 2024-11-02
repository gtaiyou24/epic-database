# 🗄️ Epic DataBase

<a href="https://github.com/gtaiyou24/epic-database/actions/workflows/test.yml" target="_blank">
  <img src="https://github.com/gtaiyou24/epic-database/actions/workflows/test.yml/badge.svg" alt="Test">
</a>

## 📚 使い方
<details><summary><b>🏃 起動する</b></summary>

```bash
docker-compose up --build
```

</details>

<details><summary><b>📦 MQにプッシュ</b></summary>

```bash
gcloud pubsub topics publish subscriber-topic --message "{\"publisher_name\": \"api-gateway\", \"event_type\": \"health_check\", \"greeting\": \"こんにちは\"}"
```

</details>

<details><summary><b>🗄️ ローカルDBに接続する</b></summary>

| データベース | 保存しているデータ                                                                                    | 接続コマンド                                                                        |
|:------:|:---------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|
| Redis  | ログイン時に発行されるアクセストークン、リフレッシュトークンを保存しています。                                                      | `redis-cli -p 6379`                                                           | 
| MySQL  | ・ユーザーの積立金額やお気に入り投信信託、ニュースデータ、掲示板などのデータ<br>・投信信託のリターン値やリスク値などのファンドや日経平均株価などのインデックス、その他金融市場データ | <pre>mysql -h 127.0.0.1 -P 3306 -u user -p <br /># Enter password: pass</pre> |

</details>

<details><summary><b>🔌 OpenAPI から TypeScript のクライアントコードを生成する</b></summary>

```bash
cd frontend
npm run generate-client
```

利用しているパッケージは「[openapi-typescript | OpenAPI TypeScript](https://openapi-ts.pages.dev/introduction)」です。

</details>

<details><summary><b>✅ テストを実行する</b></summary>

バックエンド(FastAPI)のテストを実行する場合は、下記のコマンドを実行してください。
```bash
# テスト実行に必要なライブラリをインストール
pip install -r backend/requirements.test.txt

# テストを実行
pytest -v ./test
```

</details>

<details><summary><b>🌏 インフラを構築する</b></summary>

事前に [Google Cloud のコンソール画面](https://console.cloud.google.com/welcome) にてプロジェクトを作成してください。プロジェクトを作成したら、以下の作業を行なってください。

- `infrastructure/terraform/gcp/environments/production/terraform.tfvars` に情報を記載してください。
- [お支払い画面](https://console.cloud.google.com/billing/linkedaccount) にて請求先アカウントをリンクしてください。

システムを構築するにあたり、ローカル PC にて Google 認証を完了させてください。
```bash
# Google Cloud SDK と Google アカウントを連携させる
gcloud auth login

# プロジェクトを確認
gcloud projects list

# プロジェクトを変更する
gcloud config set project {PROJECT_ID}
```

最後に Terraform を実行し、システムを構築してください。
```bash
# 適切な環境フォルダを選択してください
cd ./infrastructure/terraform/gcp/environments/production

terraform init  # 初めて実行する場合のみ初期化する
terraform plan  # 定義内容のチェック

terraform apply -auto-approve  # インフラを構築
```

システムを削除する場合は以下のコマンドを実行してください。
```bash
terraform destroy
```

</details>

## 🛠️ 技術スタック
<details><summary><b>🔨 バックエンド</b></summary>

- ⚙️ 開発言語: Python 3.12
- ⚡️ フレームワーク: [FastAPI](https://fastapi.tiangolo.com/)
- ✍️ 設計手法: [DDD(ドメイン駆動設計)](https://amzn.to/4gjk6AQ)
- 🧰 ライブラリ:
  - 💾 [SQLAlchemy](https://www.sqlalchemy.org/) : Python SQL DataBase interactions (ORM).
  - ✅ [PyTest](https://docs.pytest.org/en/stable/) : Python test.
  - 🔈️ [slf4py](https://pypi.org/project/slf4py/) : Logging.
  - 🔀 [di4injector](https://pypi.org/project/di4injector/) : DI injection.
- 💾️ DB: MySQL / Redis
- 🔌 クライアント連携: RESTful API
- 🚀 CI: [GitHub Actions](https://docs.github.com/ja/actions)
- 📃 Doc: Markdown / [Mermaid](https://mermaid.js.org/)

</details>

<details><summary><b>🔧 フロントエンド</b></summary>

- ⚙️ 開発言語: TypeScript
- ⚡️ フレームワーク: [Next.js 14 App Router](https://nextjs.org/docs)
- 🧰 ライブラリ:
  - 🔐 [Auth.js(NextAuth.js V5)](https://authjs.dev/)
- 🎨 CSS: [Tailwind](https://tailwindcss.com/) / [shadcn/ui](https://ui.shadcn.com/) / [Headless UI](https://headlessui.com/)
- 🚀 CI: [GitHub Actions](https://docs.github.com/ja/actions)

</details>

<details><summary><b>☁️ インフラ</b></summary>

- ☁️ クラウドサービス:
  - Compute: GCP Cloud Run
  - DB: [Neon](https://neon.tech/) / [Upstash](https://upstash.com/)
- 🌍️ IaC: [Terraform](https://www.terraform.io/)
- 🐋 DevOps: [Docker Compose](https://www.docker.com)
- 🚨 エラー/ログ監視ツール: [Sentry](https://sentry.io/welcome/) / [New Relic](https://newrelic.com/jp)
- 📧 メールサービス: Gmail / SendGrid

</details>

## 🔗 Appendix
### 🕷️ データソース

**データ項目**

 - 企業情報
 - 求人情報
 - ニュース / 記事
 - イベント
 - お店(ローカルビジネス)
 - レストラン

| データソース | 説明                 |
|:----------:|:-------------------|
| [Custom Search API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com?hl=ja&pli=1&project=mento-staging2) | 企業のホームページを収集       |
| [WebPilot API](https://www.webpilot.ai/contact/) | ホームページURLから企業情報を取得 |
