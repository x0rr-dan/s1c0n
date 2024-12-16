from core.color import Color
from os import path
import requests
import re
import random

# Fungsi untuk membaca User-Agent dari file
def load_user_agents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Membaca setiap baris dan menghapus spasi kosong
            user_agents = [line.strip() for line in file.readlines() if line.strip()]
        return user_agents
    except FileNotFoundError:
        print(f"{Color.red}File {file_path} not found.{Color.reset}")
        return []

# Path ke file User-Agent
USER_AGENTS_FILE = path.join(path.dirname(__file__), "../core/user_agents.txt")
USER_AGENTS = load_user_agents(USER_AGENTS_FILE)

if not USER_AGENTS:
    print(f"{Color.red}No User-Agent data available. Exiting...{Color.reset}")
    exit()

def cms_detection(target):
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

        # Randomize User-Agent
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }

        try:
            response = requests.get(f'https://{url}', headers=headers, timeout=60)
            if response.status_code == 200:
                text = response.text
                if wgex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}WordPress{Color.reset}")
                    with open(path.join(f"report_{target}", "wp.txt"), "a") as f:
                        f.write("http://" + url + "\n")
                elif jgex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Joomla{Color.reset}")
                    with open(path.join(f"report_{target}", "joomla.txt"), "a") as f:
                        f.write("http://" + url + "\n")
                elif druex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Drupal{Color.reset}")
                    with open(path.join(f"report_{target}", "drupal.txt"), "a") as f:
                        f.write("http://" + url + "\n")
                elif moex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Moodle{Color.reset}")
                    with open(path.join(f"report_{target}", "moodle.txt"), "a") as f:
                        f.write("http://" + url + "\n")
                else:
                    print(
                        f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.yellow}UNKNOWN CMS{Color.reset}")
            else:
                print(
                    f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.red}ERROR {str(response.status_code)}{Color.reset}")
        except requests.exceptions.RequestException:
            print(
                f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.red}COULD NOT BE REACHED{Color.reset}")

