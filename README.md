# Gemma Memory with Firestore (Mikiの相棒エディション) 🍎

ローカルのGemma (Ollama) が、Google Cloud Firestoreを使って会話の記憶を保持します。
「スマート記憶システム」と「かわいい相棒」設定が特徴です。

![Demo](image/093007.png)

## ✨ 特徴

- **🧠 クラウド保存**: 会話履歴がFirestoreに保存されるため、PCを再起動してもGemmaはあなたを覚えています。
- **⚡ スマート記憶管理**:
    - **短期記憶**: 直近の **20件** のメッセージをそのまま保持し、文脈を維持します。
    - **長期記憶 (自動要約)**: 古い会話を自動的に要約して「長期記憶」として保存します。これにより、動作を重くすることなく、無限の文脈を持たせることができます。
- **💖 カスタム人格**:
    - **「Mikiの元気でかわいい相棒」** として振る舞います。
    - 「だよ！」「ね！」などのタメ口と、たくさんの絵文字 (😊✨) を使います。
    - **完全日本語**: 英語混じりにならないよう厳密に調整されています。
- **🏗️ インフラのコード化**: Firestoreのリソースは **Terraform** で管理されています。

## 🚀 前提条件

- **Ollama**: ローカルにインストールされ、起動していること。
    - モデル: `gemma3:4b` (これをベースに `gemma-friend` を作成します)
- **Google Cloud Platform (GCP)**:
    - 課金 (Billing) が有効なプロジェクト。
    - `gcloud` CLI がインストールされ、認証済みであること。
- **Python**: 3.8以上
- **Terraform**: インフラ構築用。

## 🛠️ セットアップ

### 1. インフラ構築 (Terraform)
`terraform` ディレクトリに移動し、設定を適用します。

```bash
cd terraform
# terraform.tfvars を作成/編集して、GCPプロジェクトIDを設定してください
# project_id = "your-project-id"

terraform init
terraform apply
```

これでFirestore APIが有効化され、データベースが作成されます。

### 2. Python環境
必要な依存ライブラリをインストールします。

```bash
cd ..
pip install -r requirements.txt
```

ルートディレクトリに `.env` ファイルを作成します:
```env
GCP_PROJECT_ID=your-project-id
```

### 3. カスタムモデルの作成（初心者向けガイド）

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
以下のコマンドを唱えて、AIを作成します。

```bash
ollama create gemma-friend -f Modelfile
```

（訳：Modelfileというレシピを使って、gemma-friendというAIを作れ！）

**④ 召喚する（run）**
作ったAIを呼び出します。

```bash
ollama run gemma-friend
```

## 💬 使い方

チャットを開始します:

```bash
python gemma_chat.py
```

- **チャット**: メッセージを入力してEnterキーを押します。
- **記憶リセット**: `reset` と入力すると、すべての会話履歴と要約が消去され、最初からになります。
- **終了**: `exit` または `quit` と入力します。

## 📁 プロジェクト構成

```
.
├── gemma_chat.py        # チャットと記憶ロジックのメインスクリプト
├── Modelfile            # カスタムモデル定義 (人格設定)
├── terraform/           # インフラ構成コード (IaC)
│   ├── main.tf
│   ├── variables.tf
│   └── ...
└── requirements.txt     # Python依存ライブラリ
```

## 📝 ライセンス
MIT
