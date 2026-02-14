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
DOCUMENT_ID = "user_session" # For simplicity, using a single session ID for now

def load_memory():
    """Load conversation history from Firestore."""
    doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return data.get("messages", [])
    return []

def save_memory(messages):
    """Save conversation history to Firestore."""
    doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
    doc_ref.set({"messages": messages})

def main():
    print("🤖 Gemma Memory Chat (Firestore Backed)")
    print("Type 'exit' or 'quit' to stop.\n")

    # Load past history
    history = load_memory()
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

            # Add user message to history
            history.append({"role": "user", "content": user_input})

            # Stream response from Ollama
            print("Gemma: ", end="", flush=True)
            stream = ollama.chat(
                model='gemma3:4b', # Make sure you have this model pulled: ollama pull gemma:2b
                messages=history,
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

            # Save updated history to Firestore
            save_memory(history)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            break

if __name__ == "__main__":
    main()
