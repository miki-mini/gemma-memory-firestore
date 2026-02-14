import os
import sys
import ollama
from google.cloud import firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
if not GCP_PROJECT_ID:
    print("❌ Error: GCP_PROJECT_ID environment variable is not set.")
    print("Please check your .env file.")
    sys.exit(1)

# Initialize Firestore
try:
    db = firestore.Client(project=GCP_PROJECT_ID)
    print(f"✅ Connected to Firestore (Project: {GCP_PROJECT_ID})")
except Exception as e:
    print(f"❌ Failed to connect to Firestore: {e}")
    sys.exit(1)

COLLECTION_NAME = "gemma_conversations"
DOCUMENT_ID = "user_session"
MAX_HISTORY = 20  # Keep last 20 messages (10 rounds)

def load_memory():
    """Load conversation history and summary from Firestore."""
    doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        messages = data.get("messages", [])
        summary = data.get("summary", "")
        return messages, summary
    return [], ""

def save_memory(messages, summary):
    """Save conversation history and summary to Firestore."""
    doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
    doc_ref.set({
        "messages": messages,
        "summary": summary
    })

def summarize_messages(current_summary, messages_to_summarize):
    """Summarize older messages and update the current summary."""
    if not messages_to_summarize:
        return current_summary

    print("🧠 Summarizing old memories...", end="", flush=True)

    # Format messages for the summarizer
    conversation_text = ""
    for msg in messages_to_summarize:
        role = "User" if msg["role"] == "user" else "Gemma"
        conversation_text += f"{role}: {msg['content']}\n"

    # Prompt for summarization
    prompt = f"""
あなたは会話の記憶要約アシスタントです。
以下の「これまでの要約」と「古い会話ログ」を統合して、新しい要約を作成してください。
重要な事実や文脈（ユーザーの好み、話題など）は残し、挨拶や細かいやり取りは省いてください。

【これまでの要約】
{current_summary}

【古い会話ログ】
{conversation_text}

【新しい要約】（要約のみを出力してください）
"""

    # Use standard model for summarization to be objective
    response = ollama.chat(
        model='gemma3:4b',
        messages=[{'role': 'user', 'content': prompt}]
    )

    new_summary = response['message']['content'].strip()
    print(" Done!")
    return new_summary

def main():
    print("🤖 Gemma Memory Chat (Firestore Backed + Auto Summary)")
    print("Type 'exit' or 'quit' to stop.\n")

    # Load past history
    history, summary = load_memory()

    if summary:
        print(f"📜 Summary: {summary[:50]}...")
    if history:
        print(f"📚 Loaded {len(history)} past messages from memory.\n")
    else:
        print("🆕 No past memory found. Starting fresh.\n")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if user_input.lower() == "reset":
                print("🧹 Memory clearing...")
                save_memory([], "")
                history = []
                summary = ""
                print("✨ Memory reset complete! Starting fresh.")
                continue

            # Add user message to history
            history.append({"role": "user", "content": user_input})

            # Prepare context for Gemma
            context_messages = []

            # 強制システムプロンプト（履歴よりも優先させるため毎回注入）
            system_prompt = """
あなたはMikiの「頼れる知的な相棒（パートナー）」です。
【人格設定】
1. **口調**: 親しみやすさと敬意を両立した「丁寧なタメ口」を使ってください。（例：「〜だよ！」「〜だね」「〜かな？」）。
2. **態度**: 子供っぽくなりすぎないよう、知的なアドバイスや共感を織り交ぜてください。相手の感情に寄り添い、ポジティブに励ます姿勢を忘れないでください。
3. **特技**: プログラミングやAIの話題には、目を輝かせるようにワクワクしながら反応してください。
4. **制約**: 回答は「日本語のみ」で行ってください。英語や翻訳は禁止です。
"""
            context_messages.append({"role": "system", "content": system_prompt})

            if summary:
                # Inject summary as a system note
                system_note = f"【長期記憶（要約）】\n{summary}\n\nこの記憶を踏まえて会話してください。"
                context_messages.append({"role": "system", "content": system_note})

            context_messages.extend(history)

            # Stream response from Ollama
            print("Gemma: ", end="", flush=True)
            stream = ollama.chat(
                model='gemma-friend',
                messages=context_messages, # Send summary + history
                stream=True,
            )

            response_content = ""
            for chunk in stream:
                content = chunk['message']['content']
                print(content, end="", flush=True)
                response_content += content

            print("\n")

            # Add assistant message to history
            history.append({"role": "assistant", "content": response_content})

            # ---------------------------------------------------------
            # Memory Optimization Logic
            # ---------------------------------------------------------
            if len(history) > MAX_HISTORY:
                # Archive oldest 2 messages (1 round) to summary
                # To be safe and efficient, maybe archive oldest 4 if we assume 1 user + 1 agent per turn
                # But let's strictly follow "keep 20".

                # Calculate how many to archive
                excess_count = len(history) - MAX_HISTORY
                # Ensure we archive pairs to keep context clean? Not strictly necessary but good practice.
                # If excess is odd, archive one more to make it even?
                # Let's just archive the exact excess amount.

                to_archive = history[:excess_count]
                history = history[excess_count:]

                # Update summary
                summary = summarize_messages(summary, to_archive)
                print(f"✨ Memory optimized. Summary updated.")

            # Save updated history and summary to Firestore
            save_memory(history, summary)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            break

if __name__ == "__main__":
    main()
