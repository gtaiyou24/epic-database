# 🗄 Epic DataBase

<a href="https://github.com/gtaiyou24/epic-database/actions/workflows/test.yml" target="_blank"><img src="https://github.com/gtaiyou24/epic-database/actions/workflows/test.yml/badge.svg" alt="Test"></a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/gtaiyou24/epic-database" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/gtaiyou24/epic-database.svg" alt="Coverage"></a>

## 📚 使い方
<details><summary><b>🏃 起動する</b></summary>

```bash
docker-compose up --build
```

</details>

<details><summary><b>✉️ メッセージをキューイング</b></summary>

```bash
# キューの一覧を表示
$ aws sqs list-queues --endpoint-url http://localhost:4566

# メッセージを作成
$ aws sqs send-message \
    --queue-url http://localhost:4566/000000000000/financial-market \
    --endpoint-url http://localhost:4566 \
    --message-body '{
    "notification_id": 1, 
    "event": {
      "isin_code": "JP90C000GKC6", 
      "ita_code": "03311187",  
      "name": "eMAXIS Slim米国株式(S&P500)",
      "asset_type": "STOCK", 
      "management_type": "INDEX", 
      "destination": "NORTH_AMERICA", 
      "trade_types": [
        "NISA_TSUMITATE", 
        "NISA_SEITYOU", 
        "OPEN_END"
      ]
    },
    "occurred_on": "2024-03-05 15:19:24", 
    "event_type": "ProductCrawled.1", 
    "version": 1,
    "producer_name": "epic-crawler"
  }
'

# キューイングされたメッセージを表示
$ aws sqs receive-message \
    --queue-url http://localhost:4566/000000000000/financial-market \
    --endpoint-url http://localhost:4566
```

</details>

<details><summary><b>🗄️ ローカルDBに接続する</b></summary>

|   データベース   | 保存しているデータ                               | 接続コマンド                                                                        |
|:----------:|:----------------------------------------|:------------------------------------------------------------------------------|
|   Redis    | ログイン時に発行されるアクセストークン、リフレッシュトークンを保存しています。 | `redis-cli -p 6379`                                                           | 
| PostgreSQL | 万が一 KVS のデータが失われた時に復元できるようにするためのデータ     | <pre>mysql -h 127.0.0.1 -P 3306 -u user -p <br /># Enter password: pass</pre> |

</details>

<details><summary><b>🔌 OpenAPI から TypeScript のクライアントコードを生成する</b></summary>

```bash
npm run generate-client
```

利用しているパッケージは「[openapi-typescript | OpenAPI TypeScript](https://openapi-ts.pages.dev/introduction)」です。

</details>

<details><summary><b>✅ テストを実行する</b></summary>

バックエンド(FastAPI)のテストを実行する場合は、下記のコマンドを実行してください。
```bash
# テスト実行に必要なライブラリをインストール
pip install -r api/requirements.test.txt

# テストを実行
pytest -v ./test
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

<details><summary><b>☁️ インフラ</b></summary>

- ☁️ クラウドサービス:
    - Compute: GCP Cloud Run
    - DB: [Neon](https://neon.tech/) / [Upstash](https://upstash.com/)
- 🌍️ IaC: [Terraform](https://www.terraform.io/)
- 🐋 DevOps: [Docker Compose](https://www.docker.com)
- 🚨 エラー/ログ監視ツール: [Sentry](https://sentry.io/welcome/) / [New Relic](https://newrelic.com/jp)
- 📧 メールサービス: Gmail / SendGrid

</details>