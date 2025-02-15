from langgraph_sdk import get_sync_client
import pprint
from openai_api import OpenAiApi
from config_json import Config

cfg = Config("/home/zijie/Nanachi/src/config.json") 
llm = OpenAiApi(api_key=cfg("OPENAI_API_KEY"))

def fetch_backend(in_line, in_msg, in_history):
    prompt = f"""
    你是一个linux 终端专家
    请你根据以下提供的Background信息 根据用户的要求 User_request
    来补全 User_Command_Line 的内容
    Background: {in_history}
    User_Command_Line: {in_line}
    User_request: {in_msg}
    将你的输出用 <<< 和 >>> 包裹，同时将指令用$$$分割开来
    例如：<<<ls cat$$$cd cat$$$git checkout main>>>
    请你预测五个最有可能用户需要的命令
    """
    
    response = llm.query(messages=[{"role": "user", "content": prompt}])
    commands_str = response.split("<<<")[1].split(">>>")[0]
    commands_list = commands_str.split("$$$")
    return commands_list



# client = get_sync_client(url="http://localhost:2024")


# def fetch_backend(in_line, in_msg, in_history):
#     last_chunk = None
#     for chunk in client.runs.stream(
#         None,  # Threadless run
#         "agent",  # Name of assistant. Defined in langgraph.json.
#         input={
#             "in_line": in_line,
#             "in_msg": in_msg,  # Fixed typo from im_msg to in_msg
#             "in_history": in_history,
#         },
#         stream_mode="updates",
#     ):
#         last_chunk = chunk
#         print(f"Receiving new event of type: {chunk.event}...")
#         print(chunk.data)
#         print("\n\n")
    
#     return last_chunk