from core.color import Color
from core.random_ag import rangent
from os import path
import requests, re, subprocess

def cms_detection(target, user_agent=None, proxy=None):
    proxies = {"http": proxy, "https": proxy} if proxy else None
    # Regular Expressions for CMS detection
    wgex = re.compile(r'(?:<meta name="generator" content="WordPress|/wp-content/)')  # WordPress
    jgex = re.compile(r'(?:<meta name="generator" content="Joomla|/media/system/js/)')  # Joomla
    druex = re.compile(r'(?:<meta name="generator" content="Drupal|/sites/all/)')  # Drupal
    moex = re.compile(r'(?:<meta name="keywords" content="moodle|/core/)')  # Moodle

    # Read subdomains
    with open(f"report_{target}/subdomain.txt", 'r', encoding='utf-8') as r:
        read_subdo = r.readlines()

    print(f"{Color.bold}{Color.green}\n\t  [+] CMS DETECTION: {len(read_subdo)} sites{Color.reset}")

    # Scan each URL
    for url in read_subdo:
        url = url.strip()

        if user_agent:
            headers = {"User-Agent": user_agent}
        else:
            headers = {"User-Agent": rangent()}

        host = subprocess.check_output(f"echo {url} | httprobe -prefer-https", shell=True, text=True).strip()
        if not host:
            host = f"http://{url}"
        try:
            response = requests.get(f'{host}', headers=headers, timeout=60, proxies=proxies)
            if response.status_code == 200:
                text = response.text
                if wgex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{host} | {Color.green}WordPress{Color.reset}")
                    with open(path.join(f"report_{target}", "wp.txt"), "a") as f:
                        f.write(f"{host}\n")
                elif jgex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{host} | {Color.green}Joomla{Color.reset}")
                    with open(path.join(f"report_{target}", "joomla.txt"), "a") as f:
                        f.write(f"{host}\n")
                elif druex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{host} | {Color.green}Drupal{Color.reset}")
                    with open(path.join(f"report_{target}", "drupal.txt"), "a") as f:
                        f.write(f"{host}\n")
                elif moex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{host} | {Color.green}Moodle{Color.reset}")
                    with open(path.join(f"report_{target}", "moodle.txt"), "a") as f:
                        f.write(f"{host}\n")
                else:
                    print(
                        f"{Color.green}\t    -> {Color.reset}{Color.bold}{host} | {Color.yellow}UNKNOWN CMS{Color.reset}")
            else:
                print(
                    f"{Color.green}\t    -> {Color.reset}{Color.bold}{host} | {Color.red}ERROR {str(response.status_code)}{Color.reset}")
        except requests.exceptions.RequestException as e:
            print(
                f"{Color.green}\t    -> {Color.reset}{Color.bold}{host} | {Color.red}COULD NOT BE REACHED {e}{Color.reset}")

