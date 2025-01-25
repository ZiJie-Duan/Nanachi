
import json
from pprint import pprint
from kittens.tui.handler import kitten_ui
from kittylib import focus, Apperance, ctrl_fn_warp
from config_json import Config
import signal
import sys
import os
from test import call_deepseek_api

# user_site = os.path.expanduser("~/.local/lib/python3.12/site-packages")
# if user_site not in sys.path:
#     sys.path.append(user_site)
# from deepseek_api import GptApi

@kitten_ui(allow_remote_control=True)
def main(args: list[str]) -> str:


    import sys
    import os
    # 打印调用该脚本的 Python 解释器路径
    print("Python解释器路径:", sys.executable)
    print("Python版本:", sys.version)
    print("环境变量PATH:", os.getenv('PATH'))
    print("Python前缀路径:", sys.prefix)
    
    cfg = Config("/home/zijie/Nanachi/src/config.json") 
    ctrlfn = ctrl_fn_warp(main.remote_control)
    ap = Apperance(ctrlfn, cfg("NANACHI_BG_IMG"))

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

    # gpt = GptApi(api_key=cfg("DEEPSEEK_API_KEY"))
    # print(gpt.query(
    #     [{"role": "user", "content": "Hello"}]
    # ))
    print(call_deepseek_api(cfg("DEEPSEEK_API_KEY"),"https://api.deepseek.com/chat/completions"))

    ap.say_hello()
    input()
    ap.remove_back_ground()

    return "None"