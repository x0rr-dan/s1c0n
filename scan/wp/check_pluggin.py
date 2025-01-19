from core.color import Color
from core.random_ag import rangent
from scan.wp.cek_db import cek_db
import requests
import re

def check_plugin(target_site, plugin, page_content, user_agent=None, proxy=None):
    he = rangent()
    if user_agent:
        headers = {"User-Agent": user_agent}
    else:
        headers = {"User-Agent": he}
    detect = set()
    for file in ["changelog.txt", "readme.txt"]:
        try:
            e = requests.get(f"{target_site}/wp-content/plugins/{plugin}/{file}", timeout=10, headers=headers, proxies=proxy)
            if e.status_code == 200:
                topver = re.search(r"== Changelog ==\s+= ([\d.]+) - (\d{4}-\d{2}-\d{2}) =", e.text) or \
                         re.search(r"= ([\d.]+) - (\d{4}-\d{2}-\d{2}) =", e.text)
                if topver:
                    versi = topver.group(1)
                    detect.add(plugin)
                    cek_db(target_site, plugin, versi, user_agent)
                    return
        
        except requests.Timeout:
            print(f"{Color.red}\t     -> {Color.reset}{Color.bold}{target_site} {Color.reset}[{Color.red}{Color.bold} Request time out{Color.reset}]")
        except requests.exceptions.RequestException:
            continue

    if plugin not in detect:
        assets = [f"{target_site}/wp-content/plugins/{plugin}/plugin.php",
                  f"{target_site}/wp-content/plugins/{plugin}/style.css",
                  f"{target_site}/wp-content/plugins/{plugin}/script.js"]
        for asset in assets:
            try:
                a = requests.get(asset, timeout=10, headers=headers, proxies=proxy)
                version_in_header = re.search(r"Version:\s*([\d.]+)", a.text)
                if version_in_header:
                    versi = version_in_header.group(1)
                    detect.add(plugin)
                    cek_db(target_site, plugin, versi, user_agent)
                    return

            except requests.Timeout:
                print(f"{Color.red}\t     -> {Color.reset}{Color.bold}{target_site} {Color.reset}[{Color.red}{Color.bold} Request time out{Color.reset}]")
            except requests.exceptions.RequestException:
                continue

    if plugin not in detect:
        meta_version = re.search(rf"{plugin}.*?ver=([\d.]+)", page_content)
        if meta_version:
            versi = meta_version.group(1)
            detect.add(plugin)
            cek_db(target_site, plugin, versi, user_agent)
