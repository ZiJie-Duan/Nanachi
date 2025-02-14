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

import json
from pprint import pprint
import signal
import sys
import os
from kittens.tui.handler import kitten_ui
from kitty.boss import Boss

custom_lib = os.path.expanduser("~/Nanachi-python")
sys.path.insert(0, custom_lib)
import httpcore
from deepseek_api import DeepSeekApi
from config_json import Config
from kittylib import focus, Apperance, ctrl_fn_warp
from decoder import get_history_command

def sysinfo():
    # 打印调用该脚本的 Python 解释器路径
    print("Python解释器路径:", sys.executable)
    print("Python版本:", sys.version)
    print("环境变量PATH:", os.getenv('PATH'))
    print("Python前缀路径:", sys.prefix)
    
    print("当前 sys.path:", sys.path)
    print("httpcore 是否存在:", os.path.exists(os.path.join(custom_lib, "httpcore")))


@kitten_ui(allow_remote_control=True)
def main(args: list[str]) -> str:
    
    cfg = Config("/home/zijie/Nanachi/src/config.json") 
    ctrlfn = ctrl_fn_warp(main.remote_control)
    ap = Apperance(ctrlfn, cfg("NANACHI_BG_IMG"))
    deepseek = DeepSeekApi(api_key=cfg("DEEPSEEK_API_KEY"))

    def handle_exit(signal_number, frame):
        ap.remove_back_ground()        
        sys.exit(0)
    # 绑定 SIGINT 信号到 handle_exit 函数
    signal.signal(signal.SIGINT, handle_exit)

    ap.set_back_ground()
    ap.say_hello()

    cp = ctrlfn(["ls"], capture_output=True) 
    cp_json = json.loads(cp.stdout)
    windows = focus(cp_json)

    # for id in windows:
    #     cp = ctrlfn(["get-text", "--match", f"id:{id}", "--extent", "all"],
    #                 capture_output=True)
    #     print(cp.stdout.decode('utf-8'))
    

    cp = ctrlfn(["get-text", "--match", f"id:{windows[0]}", "--extent", "all"],
                    capture_output=True)
    
    history = get_history_command(cp.stdout.decode("utf-8"), "zijie@pop-os:")
    pprint(history)
    print("\n")
    cp = ctrlfn(["get-text", "--match", f"id:{windows[0]}", "--extent", "last_cmd_output"],
                    capture_output=True)
    lastOutPut = cp.stdout.decode("utf-8")

    message = [{"role": "user", 
          "content": \
"这是用户输入命令的历史记录：\n" + "\n".join(history[-10:-1]) +
"这是用户最后一条命令和输出：\n" + history[-2] + lastOutPut +
f"""
请你根据上述的终端历史命令 尤其是最后一条命令和输出 来预测和补全接下来用户会完成的6个最有可能的终端指令
要完整的终端指令，例如 “ls -l ./server/app/”
用以下格式输出：
command1$$$command2$$$command3....
command是你预测的单条指令，用三个$来分隔命令
用户已经输入的部分：{history[-1]}
请你补全指令 写成完整的指令
"""}]
    
    message = [
        {"role":"user","content":input("qc>>")}
    ]
    
    print(message)
    print("\n")

    cmd_list = deepseek.query(
        message
    ).split("$$$")

    for i, cmd in enumerate(cmd_list):
        print(f"{i+1},{cmd}")

    uin = input("/n请选择指令编号:")

    ctrlfn(["send-text", "--match", f"id:{windows[0]}", "\x15"])
    ap.remove_back_ground()
    return cmd_list[int(uin)-1]


def handle_result(args: list[str], answer: str, target_window_id: int, boss: Boss) -> None:
    # get the kitty window into which to paste answer
    w = boss.window_id_map.get(target_window_id)
    if w is not None:
        w.paste_text(answer)