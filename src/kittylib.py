import sys

def ctrl_fn_warp(ctrlfn):
    def warp(*args, **kwargs): 
        cp = ctrlfn(*args, **kwargs)
        if cp.returncode != 0:
            sys.stderr.buffer.write(cp.stderr)
            raise SystemExit(cp.returncode)
        else:
            return cp
    return warp


class Apperance:

    def __init__(self, ctrlfn, image) -> None:
        self.ctrlfn = ctrlfn
        self.image = image
    
    def set_back_ground(self):
        self.ctrlfn(["set-background-image", 
                     self.image])
    
    def remove_back_ground(self):
        self.ctrlfn(["set-background-image", 
                     "None"])
    
    def say_hello(self):
        print("Nanachi v0.1")


def focus(data):
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


