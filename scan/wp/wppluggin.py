from concurrent.futures import ThreadPoolExecutor, as_completed
from core.color import Color
from scan.wp.check_pluggin import check_plugin
import requests
import re

def wpplugin(target_site):
    try:
        quest = requests.get(target_site, timeout=10)
        p = quest.text
        plugins = set(re.findall(r"/wp-content/plugins/([a-zA-Z0-9\-]+)/", p))

        if plugins:
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(check_plugin, target_site, plugin, p) for plugin in plugins]
                for future in as_completed(futures):
                    future.result()

        else:
            print(f"{Color.green}\t     -> {Color.reset}{Color.bold}{target_site} [{Color.red} CANT FIND ANY PLUGIN {Color.reset}{Color.bold}]{Color.reset}")

    except requests.Timeout:
            print(f"{Color.red}\t     -> {Color.reset}{Color.bold}{target_site} {Color.reset}[{Color.red}{Color.bold} Request time out{Color.reset}]")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
