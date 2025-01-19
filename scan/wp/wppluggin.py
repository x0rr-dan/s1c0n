from concurrent.futures import ThreadPoolExecutor, as_completed
from core.color import Color
from core.random_ag import rangent
from scan.wp.check_pluggin import check_plugin
import requests
import re

def wpplugin(target_site, user_agent=None, proxy=None):
    if user_agent:
        headers = {"User-Agent": user_agent}
    else:
        headers = {"User-Agent": rangent()}
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        quest = requests.get(target_site, timeout=10, headers=headers, proxies=proxies)
        p = quest.text
        plugins = set(re.findall(r"/wp-content/plugins/([a-zA-Z0-9\-]+)/", p))
        getblock = set(re.findall(r"Please wait while your request is being verified\.\.\.", p))

        if plugins:
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(check_plugin, target_site, plugin, p) for plugin in plugins]
                for future in as_completed(futures):
                    future.result()
        elif getblock:
            print(f"{Color.green}\t     -> {Color.reset}{Color.bold}{target_site} [{Color.red} DETECTED BOT BY IMUNITY360 WAF {Color.reset}{Color.bold}]{Color.reset}")

        else:
            print(f"{Color.green}\t     -> {Color.reset}{Color.bold}{target_site} [{Color.red} CANT FIND ANY PLUGIN{Color.reset}{Color.bold}]{Color.reset}")

    except requests.Timeout:
            print(f"{Color.red}\t     -> {Color.reset}{Color.bold}{target_site} {Color.reset}[{Color.red}{Color.bold} Request time out{Color.reset}]")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
