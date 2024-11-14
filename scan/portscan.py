from os import system
from core.color import Color
from core.utility import clean

def port_scanning(target):
    system(f"nmap -sV {target} -o .list_nmap.txt > /dev/null")
    system("cat .list_nmap.txt | grep open > .list_nmap_finish.txt")
    with open(".list_nmap_finish.txt", encoding="utf-8") as file_nmap:
        port = file_nmap.read().splitlines()
    clean("txt")
    print(f"{Color.bold}{Color.green}\n\t  [+] OPENED PORTS: {len(port)}{Color.reset}")
    for p in port:
        print(f"\t    {Color.green}-> {Color.reset}{Color.bold}{p}{Color.reset}")
