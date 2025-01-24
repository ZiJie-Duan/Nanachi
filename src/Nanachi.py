import json
import sys
from pprint import pprint

from kittens.tui.handler import kitten_ui
from kittylib import focus

@kitten_ui(allow_remote_control=True)
def main(args: list[str]) -> str:

    main.remote_control(["set-background-image", "/home/zijie/.config/kitty/Nanachi.png"])
    
    cp = main.remote_control(["ls"], capture_output=True)
    if cp.returncode != 0:
        sys.stderr.buffer.write(cp.stderr)
        raise SystemExit(cp.returncode)
    cp_json = json.loads(cp.stdout)

    pprint(cp_json)
    windows = focus(cp_json)

    for id in windows:
        cp = main.remote_control(["get-text", "--match", f"id:{id}", "--extent", "all"],
                                 capture_output=True)
        if cp.returncode != 0:
            sys.stderr.buffer.write(cp.stderr)
            raise SystemExit(cp.returncode)
        print(cp.stdout.decode('utf-8'))

    input() 
    main.remote_control(["set-background-image", "None"])
    return "None"