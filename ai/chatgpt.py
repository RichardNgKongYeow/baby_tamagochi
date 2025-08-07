import openai

class ChatGPTInterface:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        """
        Initialize ChatGPT interface with your API key and model (default: gpt-3.5-turbo)
        """
        self.api_key = api_key
        openai.api_key = api_key
        self.model = model
        self.message_history = []

    def ask(self, prompt):
        """
        Send a prompt to ChatGPT and return the response.
        """
        if not self.api_key:
            return "Error: No API key provided."
        
        self.message_history.append({"role": "user", "content": prompt})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.message_history
            )
            reply = response['choices'][0]['message']['content']
            self.message_history.append({"role": "assistant", "content": reply})
            return reply
        except openai.error.InvalidRequestError as e:
            if "does not have access to model" in str(e):
                return f"Error: Project does not have access to model {self.model}. Try using 'gpt-3.5-turbo' or check your OpenAI project settings."
            return f"Error: {e}"
        except openai.error.RateLimitError as e:
            return "Error: You exceeded your current quota, please check your plan and billing details."
        except Exception as e:
            return f"Error: {e}"

    def reset(self):
        """
        Reset the conversation history.
        """
        self.message_history = []