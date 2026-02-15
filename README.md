# Gemma Memory with Firestore (Mikiの相棒エディション) 🍎

ローカルのGemma (Ollama) が、Google Cloud Firestoreを使って会話の記憶を保持します。
「スマート記憶システム」と「かわいい相棒」設定が特徴です。

![Demo](image/Gemma.png)

## ✨ 特徴

- **🧠 クラウド保存**: 会話履歴がFirestoreに保存されるため、PCを再起動してもGemmaはあなたを覚えています
- **⚡ スマート記憶管理**:
    - **短期記憶**: 直近の **20件** のメッセージをそのまま保持し、文脈を維持します
    - **長期記憶 (自動要約)**: 古い会話を自動的に要約して「長期記憶」として保存します。これにより、動作を重くすることなく、無限の文脈を持たせることができます
- **💖 カスタム人格**:
    - **「Mikiの元気でかわいい相棒」** として振る舞います
    - 「だよ！」「ね！」などのタメ口と、たくさんの絵文字 (😊✨) を使います
    - **完全日本語**: 英語混じりにならないよう厳密に調整されています
- **🏗️ インフラのコード化**: Firestoreのリソースは **Terraform** で管理されています

## 🚀 前提条件

- **Ollama**: ローカルにインストールされ、起動していること
    - モデル: `gemma3:4b` (これをベースに `gemma-friend` を作成します)
- **Google Cloud Platform (GCP)**:
    - 課金 (Billing) が有効なプロジェクト
    - `gcloud` CLI がインストールされ、認証済みであること
- **Python**: 3.8以上
- **Terraform**: 1.14.0以上

## 🛠️ セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/miki-mini/gemma-memory-firestore.git
cd gemma-memory-firestore
```

### 2. インフラ構築 (Terraform)

`terraform` ディレクトリに移動し、設定を適用します。

```bash
cd terraform

# terraform.tfvars を作成して、GCPプロジェクトIDを設定
echo 'project_id = "your-project-id"' > terraform.tfvars

terraform init
terraform apply
```

これでFirestore APIが有効化され、データベースが作成されます。

### 3. Python環境

```bash
cd ..
pip install -r requirements.txt
```

主な依存ライブラリ:
- `ollama` — Ollamaとの通信
- `google-cloud-firestore` — Firestoreへの読み書き
- `python-dotenv` — `.env` ファイルの読み込み

### 4. 環境変数の設定

ルートディレクトリに `.env` ファイルを作成します:

```env
GCP_PROJECT_ID=your-project-id
```

> ⚠️ `.env` ファイルには秘密情報が含まれるため、Gitにコミットしないでください。`.gitignore` に含まれています。

### 5. GCP認証

Firestoreに接続するため、ローカル環境でGCPの認証を行います:

```bash
gcloud auth application-default login
```

### 6. カスタムモデルの作成

![Demo](image/093007.png)

**① Modelfileを作る**
メモ帳などで `Modelfile` という名前のファイルを作ります。

**② 催眠術を書く**
中身に以下の2行を書くだけ！（難しいテンプレートは自動で読み込まれます）

```dockerfile
FROM gemma3:4b

# ここに設定を書くだけ！
SYSTEM "あなたはMikiの相棒です。タメ口で、元気よく話してください。"
```

**③ 調理する（create）**

```bash
ollama create gemma-friend -f Modelfile
```

（訳：Modelfileというレシピを使って、gemma-friendというAIを作れ！）

**④ 召喚する（run）**

```bash
ollama run gemma-friend
```

## 💬 使い方

チャットを開始します:

```bash
python gemma_chat.py
```

| コマンド | 説明 |
| --- | --- |
| (メッセージを入力) | Gemmaとチャット |
| `reset` | すべての会話履歴と要約を消去して最初からやり直し |
| `exit` / `quit` | チャットを終了 |

## 📁 プロジェクト構成

```
.
├── gemma_chat.py        # チャットと記憶ロジックのメインスクリプト
├── Modelfile            # カスタムモデル定義 (人格設定)
├── .env                 # 環境変数 (※Gitには含まれません)
├── .gitignore
├── requirements.txt     # Python依存ライブラリ
├── image/               # スクリーンショット
│   └── 093007.png
└── terraform/           # インフラ構成コード (IaC)
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

## 📝 ライセンス

MIT