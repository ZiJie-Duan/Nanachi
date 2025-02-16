from openai import OpenAI

class BaiduLLM:
    """
    Baidu LLM API Class
    """
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key, base_url="https://qianfan.baidubce.com/v2")
        self.model = "deepseek-v3"  # 设置默认模型

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



# if __name__ == "__main__":
#     from src.config_json import Config
#     cfg = Config("/home/zijie/Nanachi/src/config.json")

#     # 初始化API客户端
#     api = BaiduLLM(api_key=cfg("BAIDU_API_KEY"))
    
#     # 测试普通查询
#     messages = [
#         {"role": "user", "content": "你好,请介绍一下你自己"}
#     ]
    
#     print("\n=== 测试普通查询 ===")
#     response = api.query(messages=messages)
#     print(response)
    
