from core.color import Color
from scan.wp.wppluggin import wpplugin
from core.random_ag import rangent
from os import path
import time

def wp_enum(target, user_agent=None, proxy=None):
    he = rangent()
    if user_agent:
        pass
    else:
        user_agent = he
    # read wordpress file that save in folder report
    if path.exists(f"report_{target}/wp.txt"):
        with open(f"report_{target}/wp.txt", 'r', encoding='utf-8') as r:
            read_subdo = r.readlines()
            print(f"{Color.bold}{Color.green}\n\t  [+] WORDPRESS ENUMERATION: {len(read_subdo)} sites{Color.reset}")
            for i in read_subdo:
                i = i.strip()
                wpplugin(i, user_agent, proxy)
                time.sleep(5)
    else:
        pass
