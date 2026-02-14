# Gemma Memory with Firestore (Miki's Partner Edition) 🍎

Gemma (running locally via Ollama) remembers your conversations by storing them in Google Cloud Firestore.
It features a "Smart Memory" system and a custom "Cute Partner" persona.

## ✨ Features

- **🧠 Cloud Persistence**: Conversation history is saved in Firestore, so Gemma remembers you even after restarting the computer.
- **⚡ Smart Memory Management**:
    - **Short-term Memory**: Keeps the exact last **20 messages** for immediate context.
    - **Long-term Memory (Auto-Summary)**: Automatically summarizes older conversations and stores them as "Long-term Memory", allowing for infinite context without slowing down.
- **💖 Custom Persona**:
    - Modeled as **"Miki's energetic and cute partner"**.
    - Speaks in casual Japanese ("だよ！", "ね！") with plenty of emojis (😊✨).
    - **Strictly Japanese**: Configured to avoid switching to English.
- **🏗️ Infrastructure as Code**: Firestore resources are managed via **Terraform**.

## 🚀 Prerequisites

- **Ollama**: Installed and running locally.
    - Model: `gemma3:4b` (will be customized to `gemma-friend`)
- **Google Cloud Platform (GCP)**:
    - A project with billing enabled.
    - `gcloud` CLI installed and authenticated.
- **Python**: 3.8+
- **Terraform**: For infrastructure setup.

## 🛠️ Setup

### 1. Infrastructure (Terraform)
Navigate to the `terraform` directory and apply the configuration.

```bash
cd terraform
# Edit/Create terraform.tfvars with your GCP Project ID
# project_id = "your-project-id"

terraform init
terraform apply
```

This will enable the Firestore API and create a Native Firestore database.

### 2. Python Environment
Install the required dependencies.

```bash
cd ..
pip install -r requirements.txt
```

Create a `.env` file in the root directory:
```env
GCP_PROJECT_ID=your-project-id
```

### 3. Create Custom Model
Create the custom `gemma-friend` model from the `Modelfile`.

```bash
ollama create gemma-friend -f Modelfile
```

## 💬 Usage

Start the chat interface:

```bash
python gemma_chat.py
```

- **Chat**: Type your message and press Enter.
- **Reset Memory**: Type `reset` to clear all conversation history and start fresh.
- **Exit**: Type `exit` or `quit`.

## 📁 Project Structure

```
.
├── gemma_chat.py        # Main Python script for chat & memory logic
├── Modelfile            # Custom model definition (Persona settings)
├── terraform/           # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   └── ...
└── requirements.txt     # Python dependencies
```

## 📝 License
MIT
