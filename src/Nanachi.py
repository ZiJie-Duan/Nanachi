import json
import sys
from pprint import pprint

from kittens.tui.handler import kitten_ui

def focus(data):
    """
    get the tabs and windows
    lable it as focused or not
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
    
    pprint(windows)
    input()



@kitten_ui(allow_remote_control=True)
def main(args: list[str]) -> str:
    cp = main.remote_control(["ls"], capture_output=True)
    if cp.returncode != 0:
        sys.stderr.buffer.write(cp.stderr)
        raise SystemExit(cp.returncode)
    output = json.loads(cp.stdout)
    pprint(output)
    focus(output)
    return "None"