from typing import Annotated

from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_openai import ChatOpenAI
from langgraph.types import Command, interrupt

import operator
# 我希望 这个程序进行 模糊补全，并可以进行提问和修正
# 命令部分 是 in line 中的前半部分
# 提示命令 部分是 inline # 的后半部分
    # 如果不存在 提示命令，则默认补全和修正 指令
# 程序会 根据 整个 
"""For basic init and call"""
import os
from langchain_community.llms import QianfanLLMEndpoint
from langchain_community.chat_models import QianfanChatEndpoint

class State(TypedDict):
    in_line: str
    in_msg: str
    in_history: str
    bg_info: str
    out_lines: list


graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-4o")

def info_summarizer(state: State):
    prompt = f"""以下是 一段终端的 命令行输入和输出
    Terminal_History: {state["in_history"]}
    请你根据以上记录 列出重要的信息。重要的，可以从终端记录中得到的信息。
    """
    message = llm.invoke(prompt)
    return {"bg_info": [message]}

def 

def get_command(state: State):
    prompt = f"""请你根据 背景信息和 用户已经输入的 信息预测可能的命令行
    Background: {state["bg_info"]}
    User_input: {state["in_line"]}
    将你的输出用 <<< 和 >>> 包裹，同时将指令用$$$分割开来
    例如：<<<ls cat$$$cd cat$$$git pull>>>
    请你预测10个不同的指令
    """
    message = llm.invoke(prompt)
    commands_str = message.content.split("<<<")[1].split(">>>")[0]
    commands_list = commands_str.split("$$$")
    return {"out_lines": commands_list}

# def ActionInterface(state: InferenceState):

#     survey_questions_raw = state["survey_questions"]
#     survey_questions_valid = [y for _, y in survey_questions_raw.items() if y != ""] 

#     survey_questions = []

#     for struct_data in survey_questions_valid:
#         question = {
#             "question_type": struct_data.question_type,
#             "question": struct_data.question,
#             "section": struct_data.section
#         }
#         survey_questions.append(question)

#     survey_questions_json = json.dumps(survey_questions)

#     logger.info(f"survey_questions_json: {survey_questions_json}")
    
#     answer_raw = interrupt(survey_questions_json)
#     answer_json = json.loads(answer_raw)

#     answer_list = []
#     for answer in answer_json:
#         answer_list.append(answer)

#     return {"survey_answers": answer_list,
#             "questions_record": answer_list
#             } 
#     # set break point

graph_builder.add_node("info_summarizer", info_summarizer)
graph_builder.add_node("get_command", get_command)
graph_builder.add_edge(START, "info_summarizer")
graph_builder.add_edge("info_summarizer", "get_command")

memory = MemorySaver()
graph = graph_builder.compile(
    checkpointer=memory
)