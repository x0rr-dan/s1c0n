from core.color import Color
from os import path
import requests
import re

def cms_detection(target):
    wgex = re.compile(r'(?:<meta name="generator" content="WordPress|/wp-content/)') # wordpress
    jgex = re.compile(r'(?:<meta name="generator" content="Joomla|/media/system/js/)') # joomla
    druex = re.compile(r'(?:<meta name="generator" content="Drupal|/sites/all/)') # drupal
    moex = re.compile(r'(?:<meta name="keywords" content="moodle|/core/)') # moodle
    with open(f"report_{target}/subdomain.txt", 'r', encoding='utf-8') as r:
        read_subdo = r.readlines()
    print(f"{Color.bold}{Color.green}\n\t  [+] CMS DETECTION: {len(read_subdo)} sites{Color.reset}")
    for url in read_subdo:
        url = url.strip()
        try:
            response = requests.get(f'https://{url}', timeout=60)
            if response.status_code == 200:
                text = response.text
                if wgex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Wordpress{Color.reset}")
                    with open(path.join(f"report_{target}", "wp.txt"), "a") as f:
                        f.write("http://"+ url + "\n")
                elif jgex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Joomla{Color.reset}")
                    with open(path.join(f"report_{target}", "joomla.txt"), "a") as f:
                        f.write("http://"+ url + "\n")
                elif druex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Drupal{Color.reset}")
                    with open(path.join(f"report_{target}", "drupal.txt"), "a") as f:
                        f.write("http://"+ url + "\n")
                elif moex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Moodle{Color.reset}")
                    with open(path.join(f"report_{target}", "moodle.txt"), "a") as f:
                        f.write("http://"+ url + "\n")
                else:
                    pass
            else:
                print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.red}ERROR {str(response.status_code)}{Color.reset}")
        except requests.exceptions.RequestException:
            print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.red}COULD NOT BE REACHED {Color.reset}")
