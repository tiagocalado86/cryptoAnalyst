from openai import OpenAI
import os
from dotenv import load_dotenv
import json

class AIService:

    @staticmethod
    def getCryptoAnalysis(textInput):
        load_dotenv()

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("API_KEY_OR"),
        )

        with open(os.getenv("DEST_FILE_PATH_REMOVE_DATA"), "r") as f1, open(os.getenv("DEST_FILE_PATH_REMOVE_NEWS"), "r") as f2:
            jsonStr1 = json.dumps(json.load(f1), indent=2)
            jsonStr2 = json.dumps(json.load(f2), indent=2)

        print(jsonStr2)

        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are an expert in crypto market analysis. But only awnser in the crypto market analysis context, when out of context, just ask the user to reformulate the question so it can be in crypto market context, kindly."
                        },
                        {
                            "type": "text",
                            "text": textInput
                        },
                        {
                            "type": "text",
                            "text": jsonStr1
                        },
                        {
                            "type": "text",
                            "text": jsonStr2
                        }
                    ]
                }
            ]
        )
        return completion.choices[0].message.content