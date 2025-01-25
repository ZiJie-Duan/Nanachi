from openai import OpenAI

class DeepSeekApi:
    """
    DeepSeek API Class
    """
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.model = "deepseek-chat"  # 设置默认模型

    def set_model(self, model: str):
        """设置模型"""
        self.model = model

    def query(self, 
            messages, 
            temperature = 0.5, 
            max_tokens = 100,
            model = None,
            full = False,
            timeout = 30) -> str:
        
        if not model:
            model = self.model

        response = self.client.chat.completions.create(
                model = model,
                messages = messages,
                temperature = temperature,
                max_tokens = max_tokens,
                timeout = timeout
            )
        if full:
            return response
        else:
            return response.choices[0].message.content


    def query_stream(self, 
            messages, 
            temperature = 0.5, 
            max_tokens = 100,
            model = None,
            full = False,
            timeout = 30):

        if not model:
            model = self.model
        
        response = self.client.chat.completions.create(
            model = model,
            messages = messages,
            temperature = temperature,
            max_tokens = max_tokens,
            stream=True,
            timeout = timeout
        )

        if full:
            for chunk in response:
                yield chunk
        
        else:
            for chunk in response:
                word = chunk["choices"][0].get("delta", {}).get("content")
                if word:
                    yield word 
    
