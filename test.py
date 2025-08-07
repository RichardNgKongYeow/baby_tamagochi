from ai.grok import GrokInterface
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    xai_api_key = os.getenv("XAI_API_KEY")
    if not xai_api_key:
        print("Error: XAI_API_KEY not found in .env file")
        return

    # Enable mock mode since xAI API is not fully available
    grok = GrokInterface(xai_api_key, use_mock=True)
    print("Grok CLI: Type your prompt, /reset to clear history, /model <model_name> to switch models, or /exit to quit.")
    
    while True:
        user_input = input("> ").strip()

        if user_input.lower() == "/exit":
            print("Goodbye!")
            break

        if user_input.lower() == "/reset":
            grok.reset()
            print("Conversation history reset.")
            continue

        if user_input.lower().startswith("/model "):
            new_model = user_input[7:].strip()
            if new_model:
                grok.set_model(new_model)
                print(f"Model switched to {new_model}.")
            else:
                print("Error: Please specify a model (e.g., /model grok-3).")
            continue

        if not user_input:
            print("Please enter a prompt.")
            continue

        # Send to Grok
        response = grok.send_message(user_input)
        print(f"Grok: {response}")

if __name__ == "__main__":
    main()