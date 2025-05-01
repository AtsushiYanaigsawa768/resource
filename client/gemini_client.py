from .not_websocket_client import Client
import random
import time
import json
import google.api_core.exceptions
import google.generativeai as genai
# Load API keys from api.json
with open('./api.json', 'r') as f:
    api_data = json.load(f)
    api_keys = api_data.get("apikeys", [])
# Safety settings for Gemini
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

prompt = [

]

def GeminiGeneration(raw_documents, prompt,model="gemini-2.0-flash"):
    """
    input:
        raw_documents: a list of text chunks (list of strings)
        prompt: instructions for the model (list of strings)

    output:
        response.text: the generated graph response from the model (string)

    This function sends a request to the OpenAI API to generate a graph based on the input text.
    It retries with another API key if the current one exceeds its quota (429 error).
    
    We usually use "gemini-1.5-flash-001" model for the graph generation.
    There are following reasons:
    1. The API fees are cheaper than any other famous models.
    2. It reproduces many answers for almost every tasks in this project.
    3. The quality of the answers and the speed of the response are better than any other models.
    
    The choice of the model:
    1. gemini-1.5-flash-001
    2. gemini-1.5-flash-002
    3. gemini-1.5-pro
    4. gemini-2.0-flash <= now we use
    5. gemini-1.5-flash-8b (similar to gemini-1.5-flash-001)
    See more information :https://ai.google.dev/gemini-api/docs/models/gemini?hl=ja
    """

    # try multiple API keys in order
    for api_key in api_keys:
        try:
            # setting API keys
            genai.configure(api_key=api_key)

            # setting the Gemini model
            model = genai.GenerativeModel(
                model_name=model,
                system_instruction=" ".join(prompt),
                safety_settings=safety_settings,
            )

            # combine the text and send the request
            response = model.generate_content(" ".join(raw_documents))
            return response.text
        except google.api_core.exceptions.ResourceExhausted as e:
            # Check whether the error is 429 (ResourceExhausted)
            # print("ResourceExhausted")
            continue
            # In case of 429 error (resource limitation), switch to the next API key
        except Exception as e:
            # If there is any other error, stop and return the error message
            return None

    # If all API keys are used, return None
    return None

class GeminiSampleClient(Client):
    def AI_player_action(self,others_info, sum, log, actions, round_num):
        # カスタムロジックを実装
        print(f"[GeminiSampleClient] AI deciding action based on sum: {sum}, log: {log}, actions: {actions},others_info: {others_info}, round_num: {round_num}" )
        # input: others_info, sum, strategy, log
        actions = GeminiGeneration(
            raw_documents=[others_info, str(sum), str(log)],
            prompt=[
                "あなたはCoyoteというゲームのAIプレイヤーです。",
                "あなたは、他のプレイヤーの情報をもとに、次の行動を決定する必要があります。",
                "あなたの行動は、他のプレイヤーの情報、合計値、戦略、ログに基づいています。",
                "あなたの行動は、以下の選択肢から選んでください。",
                "選択肢: " + str(actions),
                "あなたの行動を選んでください。"
            ]
        )
        print(actions)
        # output: action, strategy
        action = 1
        print(f"[GeminiSampleClient] AI selected action: {action}")
        return action