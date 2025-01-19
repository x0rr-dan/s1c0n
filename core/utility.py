from os import system, path, mkdir
import sys, requests, re
from core.color import Color
# 1.3 wellcome screen
def logo():
    system("clear")
    print(f"""{Color.green}{Color.bold}
    \t              ┏━┓╺┓ ┏━╸┏━┓┏┓╻
    \t              ┗━┓ ┃ ┃  ┃┃┃┃┗┫
    \t              ┗━┛╺┻╸┗━╸┗━┛╹ ╹ v1.8
{Color.yellow}{Color.bold}\n\t       https://github.com/x0rr-dan/s1c0n{Color.red}{Color.bold}\n\t           Dinus Open Source Community{Color.red}{Color.reset}""")
# 1.4 help
def break_and_help():
    print(f"""{Color.bold}{Color.green}S1c0n{Color.reset} is a {Color.bold}{Color.green}recon tool{Color.reset} designed to assist cybersecurity professionals and penetration testers in identifying potential vulnerabilities in web servers. By integrating various scanning and recon tools, s1c0n simplifies the process of information gathering and security assessment on web infrastructure.\n""")

# 1.5 clean file that doesnt use
def clean(extension):
    system(f"rm -rf .list*.{extension}")

def make_sure(proxy=None):
    proxies = {"http": proxy, "https": proxy} if proxy else None
    tor_url = "https://check.torproject.org/"
    try:
        response = requests.get(tor_url, proxies=proxies)
        if response.status_code == 200:
            res = response.text
            match = re.search(r'Congratulations\. This browser is configured to use Tor', res)
            if match:
                return True
            else:
                return False
        else:
            return False
    except requests.exceptions.RequestException:
        return False
        # print("[!] An error occurred while checking Tor:", e)
        # exit()


# 1.6 create folder report
def create_report_folder(target):
    folder_name = f"report_{target}"
    if not path.exists(folder_name):
        mkdir(folder_name)
    else:
        pass
