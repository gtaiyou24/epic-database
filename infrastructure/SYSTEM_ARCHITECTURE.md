# 🛠️ システムアーキテクチャ

 - [Nginx を使用したフロントエンド プロキシ  |  Cloud Run Documentation  |  Google Cloud](https://cloud.google.com/run/docs/internet-proxy-nginx-sidecar?hl=ja)
 - [外部アプリケーション ロードバランサの概要  |  Load Balancing  |  Google Cloud](https://cloud.google.com/load-balancing/docs/https?hl=ja)

## ☁️ GCP

```mermaid
graph TD;
    User((👦 <br/>ユーザー)) -->|example.com <br/>api.example.com| DNS
    User -->|HTTP リクエスト| LB

    subgraph Cloud [☁️ GCP]
        DNS{{📋 Cloud DNS}}
        SecretManager[(🔐 Secret Manager)]
        Storage[(️🗄️ Cloud Storage)]
        MQ[(️📦️ Cloud Pub/Sub)]
        Schedular[🕰️ Cloud Scheduler] -.-> |Push|MQ

        subgraph LB [⚖️ Load Balancing]
            %% Web Application Firewall
            WAF{{🔥 Cloud Armor}}    
        end
        subgraph Compute [Cloud Run / web-application]
            Nginx[🚥 Nginx] -.-> |localhost:3000| Frontend[⚡️Next.js App Router]
            Nginx -.-> |localhost:8000| Backend[⚡FastAPI]
            Frontend -.-> |localhost:8000|Backend
        end
        subgraph Subscriber [Cloud Run / subscriber]
            Messaging[⚡️FastAPI]
        end
        subgraph Batch [Cloud Run Job / batch]
            Python[⚡Python]
        end
        Schedular -.-> |起動|Batch
        
        subgraph DB [VPC ネットワーク]
            SQL[(💾️ Cloud SQL)]
        end

        LB -->|HTTP リクエスト| Compute
        LB --> |閲覧|Storage
        Compute --> Storage
        Compute --> SecretManager
        Subscriber --> Storage
        Subscriber --> SecretManager
        Compute -.-> |Push|MQ
        Compute --> DB[(💾️ Cloud SQL)]
        Batch --> DB
        Batch --> Storage
        MQ -.-> |Push|Subscriber
    end

    Subscriber --> DB
    Compute --> Cache[(💾️ Upstash)]
    Monitering[/🚨 Sentry / New Relic/]
    
    subgraph GitHub [🐙GitHub]
        Repository[🐙GitHub]
        CICD[/🚀GitHub Actions/]
    end

    CICD -.-> |Deploy|Cloud
    Engineer((🧑‍💻 <br/> エンジニア)) -.-> |Push|Repository
    Engineer((🧑‍💻 <br/> エンジニア)) -.-> |Deploy|CICD

%%---スタイル設定
%% 外部要素
classDef External fill:#aaa,color:#fff,stroke:#fff
%% DB 関連
classDef DataBase fill:#0e3feb,color:#fff,stroke:#fff
%% Network 関連
classDef Network fill:#84d,color:#fff,stroke:#fff
%% Compute 関連
classDef Compute fill:#ed7100,color:#fff,stroke:#fff
%% Storage 関連
classDef Storage fill:#0e4503,color:#fff,stroke:#fff
%% Security 関連
classDef Security fill:#d6242d,color:#fff,stroke:#fff
%% アプリケーション統合 関連
classDef Integration fill:#c41f5d,color:#fff,stroke:#fff

class User,Engineer External
class SQL,Cache DataBase
class DNS,CDN,LB,DB Network
class Compute,Subscriber,Batch Compute
class Storage Storage
class SecretManager Security
class MQ,Schedular Integration
```
