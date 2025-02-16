import sys,os,json

class Apperance:

    def __init__(self, ctrlfn, image) -> None:
        self.ctrlfn = ctrlfn
        self.image = image
        
    def sysinfo(self):
        # 打印调用该脚本的 Python 解释器路径
        print("Python解释器路径:", sys.executable)
        print("Python版本:", sys.version)
        print("环境变量PATH:", os.getenv('PATH'))
        print("Python前缀路径:", sys.prefix) 
        print("当前 sys.path:", sys.path)
    
    def set_back_ground(self):
        self.ctrlfn(["set-background-image", 
                     self.image])
    
    def remove_back_ground(self):
        self.ctrlfn(["set-background-image", 
                     "None"])
    
    def say_hello(self):
        print("Nanachi v0.1")
        print("啊呀，上层来的人类呀……\n呐拥抱黑暗吧……\n你从终端深渊召唤了咱，我娜娜奇，来帮帮你吧……\n")

class KittenDriver:

    def __init__(self, main_remote_control) -> None:
        self.windows = []
        self.ctrlfn = KittenDriver.ctrl_fn_warp(main_remote_control)
        self.get_windows()

    @staticmethod
    def ctrl_fn_warp(ctrlfn):
        def warp(*args, **kwargs): 
            cp = ctrlfn(*args, **kwargs)
            if cp.returncode != 0:
                sys.stderr.buffer.write(cp.stderr)
                raise SystemExit(cp.returncode)
            else:
                return cp
        return warp

    def get_windows(self):
        cp = self.ctrlfn(["ls"], capture_output=True) 
        cp_json = json.loads(cp.stdout)
        windows = self.focus(cp_json)
        self.windows = windows

    def focus(self, data):
        """
        get a list of windows id
        the first id in list is self-window id 
        """
        windows = {}
        for tab in data[0]["tabs"]:
            tab_focused = False
            if tab['is_focused']:
                tab_focused = True
            
            for window in tab["windows"]:
                if window["is_focused"]:
                    windows[window["id"]] = {
                        "window_focused" : True,
                        "tab_focused" : tab_focused
                    }
                else:
                    windows[window["id"]] = {
                        "window_focused" : False,
                        "tab_focused" : tab_focused
                    }

        # 这里假设 需要用到娜娜奇的Kitty Tab 只有一个 Window 
        windows_id = []
        for id, status in windows.items():
            if status["tab_focused"] and not status["window_focused"]:
                windows_id.insert(0, id)
            elif status["tab_focused"] and status["window_focused"]:
                pass
            else:
                windows_id.append(id)

        return windows_id


    def color_print(self, text, color = "None"):
        """
        打印带颜色的文本
        
        参数:
            text: 要打印的文本
            color: 颜色代码，可以是以下值:
                'red': 红色
                'green': 绿色
                'yellow': 黄色
                'blue': 蓝色
                'purple': 紫色
                'cyan': 青色
        """
        color_codes = {
            'red': '\033[91m',
            'green': '\033[92m', 
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m'
        }
        end_code = '\033[0m'
        
        if color in color_codes:
            print(f"{color_codes[color]}{text}{end_code}")
        else:
            print(text)
    
    def clean_in_line(self, windows_id = None):
        if windows_id == None:
            windows_id = self.windows[0]
        self.ctrlfn(["send-text", "--match", f"id:{windows_id}", "\x15"])

