from core.color import Color
from scan.wp.cek_vuln import cek_vuln
import requests
import re

def cek_db(target_site, plugin, versi):
    try:
        url = f"https://wordpress.org/plugins/{plugin}/"
        rq = requests.get(url, timeout=10)
        version_match = re.search(r"Version\s*<strong>([\d.]+)</strong>", str(rq.text))
        ver = version_match.group(1) if version_match else f"cant find last version of plugin {plugin}"
        if versi < ver:
            print(f"{Color.green}\t     -> {Color.reset}{Color.bold}{target_site} [{Color.green} {plugin} {Color.reset}| {Color.reset}{Color.green}{versi}{Color.reset} ]{Color.reset}")
            cek_vuln(plugin, versi)
        elif versi == ver:
            print(f"{Color.yellow}\t     -> {Color.reset}{Color.bold}{target_site} [{Color.yellow} {plugin} {Color.reset}| {Color.reset}{Color.red}{versi}{Color.reset} | {Color.bold}{Color.red}updated{Color.reset} ]")
        else:
            print(f"{Color.red}\t     -> {Color.reset}{Color.bold}{target_site} [{Color.red} {plugin} {Color.reset}| {Color.reset}{Color.red}{versi} {Color.reset}| {Color.bold}{Color.red} can't find exact version{Color.reset} ]")
    except requests.exceptions.RequestException:
        print(f"{Color.red}\t     -> {Color.reset}{Color.bold}{target_site} [{Color.red} {plugin} {Color.reset}| {Color.reset}{Color.red}{versi} {Color.reset}| {Color.bold}{Color.red} failed to check last version{Color.reset} ]")
