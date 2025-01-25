import json
from pprint import pprint
import signal
import sys
import os
from kittens.tui.handler import kitten_ui

custom_lib = os.path.expanduser("~/Nanachi-python")
sys.path.insert(0, custom_lib)
import httpcore
from deepseek_api import DeepSeekApi
from config_json import Config
from kittylib import focus, Apperance, ctrl_fn_warp

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

    cp = ctrlfn(["ls"], capture_output=True) 
    cp_json = json.loads(cp.stdout)
    windows = focus(cp_json)

    for id in windows:
        cp = ctrlfn(["get-text", "--match", f"id:{id}", "--extent", "all"],
                    capture_output=True)
        #print(cp.stdout.decode('utf-8'))

    print(deepseek.query(
        [{"role": "user", "content": "Talk some Interesting thing "}]
    ))

    ap.say_hello()
    input()

    ap.remove_back_ground()
    return "None"