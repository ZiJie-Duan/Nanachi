"""
娜娜奇 功能：

基础功能
1, 复制屏幕上的 输出内容
    a, 可以选择复制的条目数量

AI 功能
1, 补全当前指令 代码
    a, 根据记忆 和 过往的命令 精确补全
    b, 根据记忆 和 过往的命令 以及 提示的语言 进行补全
2, 根据历史记录 进入对话模式

想法：
1, 可以将补全 多种模式作为一个整体来进行展现。

交互系统设计
两个入口
1, 通用控制入口 启动Nanachi 主界面
2, 快速启动，命令行补全


拷贝一个 终端的路径
""" 

import os, sys
custom_lib = os.path.expanduser("~/Nanachi-python")
sys.path.insert(0, custom_lib)

import json
from pprint import pprint
import signal
from kittens.tui.handler import kitten_ui
from kitty.boss import Boss
import httpcore
from config_json import Config
from kitten_api.kittylib import Apperance, KittenDriver
from kitten_api.decoder import get_history_command, get_n_history
from llm.baidu_api import BaiduLLM
from llm.fast_fill import FastFill


@kitten_ui(allow_remote_control=True)
def main(args: list[str]) -> str:
    
    cfg = Config("/home/zijie/Nanachi/src/config.json") 
    kd = KittenDriver(main_remote_control=main.remote_control)
    ap = Apperance(kd.ctrlfn, cfg("NANACHI_BG_IMG"))
    llm = BaiduLLM(api_key=cfg("BAIDU_API_KEY"))
    fast_fill = FastFill()
    
    def handle_exit(signal_number, frame):
        ap.remove_back_ground()        
        sys.exit(0)
    # 绑定 SIGINT 信号到 handle_exit 函数
    signal.signal(signal.SIGINT, handle_exit)

    ap.set_back_ground()
    ap.say_hello()

    cp = kd.ctrlfn(["get-text", "--match", f"id:{kd.windows[0]}", "--extent", "all"],
                    capture_output=True)
    
    raw_text = cp.stdout.decode("utf-8")
    history = get_n_history(raw_text,"zijie@pop-os:", 5)

    # cp = kd.ctrlfn(["get-text", "--match", f"id:{kd.windows[0]}", "--extent", "last_cmd_output"],
    #                 capture_output=True)
    # lastOutPut = cp.stdout.decode("utf-8")

    if "#" in history[-1]:
        in_line_raw = history[-1].split("#")
    else:
        in_line_raw = [history[-1],"Complete command"]

    kd.color_print(get_n_history(raw_text,"zijie@pop-os:", 5),"yellow")
    # 写它！！！ 
    messages = fast_fill.prompt_message(
        in_history=get_n_history(raw_text,"zijie@pop-os:", 5),
        in_line=in_line_raw[0],
        in_msg=in_line_raw[1]
    )
    data = llm.query(messages=messages)
    commands = fast_fill.get_commands(data)

    #commands = data.data["get_command"]["out_lines"]
    for i, command in enumerate(commands, 1):
        print(f"{i}. {command}")
 
    uin = input("/n请选择指令编号(q退出):")
    if uin == "q":
        ap.remove_back_ground()
        return None

    kd.clean_in_line()
    ap.remove_back_ground()
    return commands[int(uin)-1]

def handle_result(args: list[str], answer: str, target_window_id: int, boss: Boss) -> None:
    # get the kitty window into which to paste answer
    w = boss.window_id_map.get(target_window_id)
    if w is not None:
        w.paste_text(answer)