import json
import urllib.request
import urllib.error
import ssl

def call_deepseek_api(apikey, url):
    # 准备请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {apikey}"
    }

    # 构造请求体
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ],
        "stream": False
    }

    try:
        # 创建请求对象
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),  # 编码为 bytes
            headers=headers,
            method='POST'
        )

        # 发送请求（添加 SSL 上下文避免证书验证错误）
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as response:
            # 检查 HTTP 状态码
            if response.status != 200:
                raise urllib.error.HTTPError(
                    url,
                    response.status,
                    response.reason,
                    response.headers,
                    response
                )
            
            # 读取并解析响应
            result = json.loads(response.read().decode('utf-8'))
            
            if "choices" in result and result["choices"]:
                assistant_reply = result["choices"][0]["message"]["content"]
                print("Assistant:", assistant_reply)
            else:
                print("Unexpected response format:", result)

    except urllib.error.HTTPError as e:
        print(f"HTTP 错误 ({e.code}): {e.reason}")
        if e.headers.get('Content-Type') == 'application/json':
            error_body = json.loads(e.read().decode('utf-8'))
            print("错误详情:", error_body)
    except urllib.error.URLError as e:
        print(f"URL 错误: {e.reason}")
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
    except Exception as e:
        print(f"发生错误: {str(e)}")