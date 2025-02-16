import os, sys
custom_lib = os.path.expanduser("~/Nanachi-python")
sys.path.insert(0, custom_lib)

from pathlib import Path
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

class FastFill:

    def __init__(self) -> None:
        pass
    
    @classmethod
    def prompt_message(self, in_line, in_msg, in_history, in_k) -> list:
        prompt = f"""
        你是一个linux 终端专家
        请你根据以下提供的Background信息 根据用户的要求 User_request
        来补全 User_Command_Line 的内容
        Background: {in_history}
        User_Command_Line: {in_line}
        User_request: {in_msg}
        将你的输出用 <<< 和 >>> 包裹，同时将指令用$$$分割开来
        例如：<<<ls cat$$$cd cat$$$git checkout main>>>
        请你预测{in_k}个最有可能用户需要的命令
        """
        return [{"role": "user", "content": prompt}]

    @classmethod
    def get_commands(self, text):
        commands_str = text.split("<<<")[1].split(">>>")[0]
        commands_list = commands_str.split("$$$")
        return commands_list


def bash_history_injection(commands):
    hist_file = Path.home() / ".bash_history"
    with open(hist_file, "a", encoding="utf-8") as f:
        f.write(commands + "\n")


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

    kd.color_print("--Nanachi-Fast-Fill--", "green")
    kd.color_print(f"  LLM: {llm.model}", "green")
    kd.color_print(f"  Config: {cfg.file}\n", "green")
    ap.say_hello()

    kd.color_print("---------- VIEW ---------", "yellow")


    cp = kd.ctrlfn(["get-text", "--match", f"id:{kd.windows[0]}", "--extent", "all"],
                    capture_output=True) 
    raw_text = cp.stdout.decode("utf-8")
    history = get_n_history(raw_text,"zijie@pop-os:", 5)
    kd.color_print(history,"yellow")

    kd.color_print("------ END OF VIEW ------\n", "yellow")
    # cp = kd.ctrlfn(["get-text", "--match", f"id:{kd.windows[0]}", "--extent", "last_cmd_output"],
    #                 capture_output=True)
    # lastOutPut = cp.stdout.decode("utf-8")

    in_line = ""
    in_msg = ""
    in_k = 6

    in_line_raw = get_history_command(raw_text,"zijie@pop-os:")[-1]
    if "#" in in_line_raw:
        in_list = in_line_raw.split("#")
        in_line = in_list[0]
        in_msg = in_list[1]
        if len(in_list) == 3:
            in_k = int(in_list[2])
    else:
        in_line = in_line_raw
        in_msg = "Complete command"
        

    kd.color_print(f"Raw Input: {in_line_raw}", "red")
    kd.color_print(f"Already typed line: {in_line}", "red")
    kd.color_print(f"Command: {in_msg}", "red")
    kd.color_print(f"K Number: {in_k}\n", "red")

    messages = fast_fill.prompt_message(
        in_history=history,
        in_line=in_line,
        in_msg=in_msg,
        in_k = in_k
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

    if len(uin) > 1:
        ul = [int(x) for x in uin]
        uin = ul[0]
        commands_temp = [commands[x-1] for x in ul]
        bash_history_injection("\n".join(commands_temp))
        commands[int(uin)-1] = "bash"

    kd.clean_in_line()
    ap.remove_back_ground()
    return commands[int(uin)-1]


def handle_result(args: list[str], answer: str, target_window_id: int, boss: Boss) -> None:
    # get the kitty window into which to paste answer
    w = boss.window_id_map.get(target_window_id)
    if w is not None:
        w.paste_text(answer)