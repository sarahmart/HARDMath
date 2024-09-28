import openai
import time
import requests
import json
from os import getenv

class GPT_Model():
    def __init__(self, model="gpt-4-turbo", api_key=openai.api_key, temperature=0, max_tokens=4000, n=1, patience=1000000, sleep_time=0.1, system_prompt=""):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.n = n
        self.patience = patience
        self.sleep_time = sleep_time
        self.system_prompt = system_prompt  # Add a system prompt parameter

    def get_response(self, user_prompt):
        patience = self.patience
        max_tokens = self.max_tokens
        messages = [
            {"role": "system", "content": self.system_prompt},  # Add system prompt as the first message
            {"role": "user", "content": user_prompt},
        ]
        #print(1)
        while patience > 0:
            patience -= 1
            #print(2)
            try:
                response = openai.chat.completions.create(model=self.model,
                                                        messages=messages,
                                                        temperature=self.temperature,
                                                        max_tokens=max_tokens,
                                                        n=self.n)
                if self.n == 1:
                    prediction = response.choices[0].message.content
                    if prediction != "" and prediction != None:
                        return prediction
                else:
                    prediction = [choice.message.content for choice in response.choices]
                    if prediction[0] != "" and prediction[0] != None:
                        return prediction
                        
            except Exception as e:
                if "limit" not in str(e):
                    print(e)
                if "Please reduce the length of the messages or completion" in str(e):
                    max_tokens = int(max_tokens * 0.9)
                    print("!!Reduce max_tokens to", max_tokens)
                if max_tokens < 8:
                    return ""
                if "Please reduce the length of the messages." in str(e):
                    print("!!Reduce user_prompt to", user_prompt[:-1])
                    return ""
                if self.sleep_time > 0:
                    time.sleep(self.sleep_time)
        return ""
    





class GPT_Model_openrouter():
    def __init__(self, model="gpt-4-turbo", api_key=openai.api_key, temperature=0, max_tokens=4000, n=1, patience=1000000, sleep_time=0.1, system_prompt="", site_url=None, app_name=None):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.n = n
        self.patience = patience
        self.sleep_time = sleep_time
        self.system_prompt = system_prompt
        self.site_url = site_url
        self.app_name = app_name
        self.is_openrouter = model.startswith("openai/o1-")
        
        if self.is_openrouter:
            self.client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=getenv("OPENROUTER_API_KEY"),
            )
        else:
            self.client = openai.OpenAI(api_key=self.api_key)

    def get_response(self, user_prompt):
        patience = self.patience
        max_tokens = self.max_tokens
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        while patience > 0:
            patience -= 1
            try:
                if self.is_openrouter:
                    extra_headers = {}
                    if self.site_url:
                        extra_headers["HTTP-Referer"] = self.site_url
                    if self.app_name:
                        extra_headers["X-Title"] = self.app_name
                    
                    response = self.client.chat.completions.create(
                        extra_headers=extra_headers,
                        model=self.model,
                        messages=messages,
                        temperature=self.temperature,
                        max_tokens=max_tokens,
                        n=self.n
                    )
                else:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=self.temperature,
                        max_tokens=max_tokens,
                        n=self.n
                    )

                if self.n == 1:
                    prediction = response.choices[0].message.content
                    if prediction != "" and prediction is not None:
                        return prediction
                else:
                    prediction = [choice.message.content for choice in response.choices]
                    if prediction[0] != "" and prediction[0] is not None:
                        return prediction

            except Exception as e:
                if "limit" not in str(e):
                    print(e)
                if "Please reduce the length of the messages or completion" in str(e):
                    max_tokens = int(max_tokens * 0.9)
                    print("!!Reduce max_tokens to", max_tokens)
                if max_tokens < 8:
                    return ""
                if "Please reduce the length of the messages." in str(e):
                    print("!!Reduce user_prompt to", user_prompt[:-1])
                    return ""
                if self.sleep_time > 0:
                    time.sleep(self.sleep_time)
        return ""

class Ollama_Server:
    def __init__(self, server_url, model_name, temperature=0):
        self.server_url = server_url
        if model_name == 'codellama-13b':
            self.model_name = 'codellama:13b'
        elif model_name == 'llama3-8b':
            self.model_name = 'llama3:8b'
        elif model_name == 'llama3.1-8b':
            self.model_name = 'llama3.1:8b'
        elif model_name == 'mistral-7b':
            self.model_name = 'mistral:7b'
        self.temperature = temperature
        self.headers = {
            "Content-Type": "application/json"
        }

    def get_response(self, use_prompt):
        # Define the payload
        payload = {
            "model": self.model_name,
            "prompt": use_prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature
            }
        }

        # Send the POST request
        response = requests.post(self.server_url, headers=self.headers, data=json.dumps(payload))

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            return result.get('response')
        else:
            print(f"Request failed with status code {response.status_code}")
            return None



