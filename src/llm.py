import os
from dotenv import load_dotenv
import ollama


class Mistral:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = ollama.Client(host=self.host)

    def respond(self, prompt, **kwargs):
        """get response from mistral"""
        try:
            response = self.client.generate(model="mistral", prompt=prompt, **kwargs)
            return response["response"]
        except Exception as e:
            raise RuntimeError(f"response failed: {e}")

    def ping(self):
        """ping llm and print pong"""
        try:
            result = self.respond("Respond with just 'pong'")
            print(result.strip())
        except Exception as e:
            raise RuntimeError(f"ping failed: {e}")
