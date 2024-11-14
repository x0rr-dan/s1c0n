from core.color import Color
from os import getcwd, system, path
from core.utility import clean
import json

def scan_dir(target):
    p = f"{getcwd()}/"
    system(f"dirsearch -u {target} -o {p}.list_dir.json --format=json > /dev/null")
    if path.exists(f"{p}/.list_dir.json"):
        with open(".list_dir.json", encoding="utf-8") as dir:
            jdir = json.load(dir)
            if jdir:
                clean("json")
                dir_found = jdir["results"]
                list_dir_found = []
                for d in dir_found:
                    p_dir = d["url"]
                    status_dir = d["status"]
                    if status_dir in [200, 403, 500, 404]:
                        list_dir_found.append([status_dir, p_dir])

                sorted_dir = sorted(list_dir_found)
                print(f"{Color.bold}{Color.green}\n\t  [+] DIRECTORIES: {len(sorted_dir)}{Color.reset}")
                for d in sorted_dir:
                    if d[0] == 200:
                        print(f"{Color.green}\t    -> {Color.reset}{Color.green}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
                    elif d[0] == 403:
                        print(f"{Color.green}\t    -> {Color.reset}{Color.red}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
                    elif d[0] == 500:
                        print(f"{Color.green}\t    -> {Color.reset}{Color.red}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
                    elif d[0] == 404:
                        print(f"{Color.green}\t    -> {Color.reset}{Color.yellow}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
            else:
                print(f"{Color.bold}{Color.red}\n\t  [-] DIRECTORIES SCANNER CANT FIND ANYTHING USEFULL{Color.reset}")
    else:
        print(f"{Color.bold}{Color.red}\n\t [-] Something wrong went running dirsearch for directory scanner{Color.reset}")
