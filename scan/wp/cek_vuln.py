from core.color import Color
import requests
import re

def cek_vuln(plugin, versi):
    try:
        wpscan = f"https://wpscan.com/plugin/{plugin}"
        rscan = requests.get(wpscan, timeout=10).text
        
        version_pattern = r"Fixed in\s+(\d+\.\d+\.\d+)"
        title_pattern = r'Title\s*</div>\s*<a href="[^"]+">\s*([^<]+)'
        
        versions = re.findall(version_pattern, rscan)
        titles = re.findall(title_pattern, rscan)
        
        for vuln_version, title in zip(versions, titles):
            try:
                if tuple(map(int, versi.split('.'))) <= tuple(map(int, vuln_version.split('.'))):
                    print(f"{Color.green}\t\t[+]{Color.reset} {Color.bold}{plugin}{Color.reset} with version {versi} is {Color.green}{Color.bold}vulnerable{Color.reset}\n\t\t   {Color.green}->{Color.reset} {Color.yellow}{Color.bold}{title}{Color.reset}")
            except ValueError:
                print("[-] Error parsing version numbers.")
    except requests.exceptions.RequestException:
        print(f"{Color.red}\t\t[!] Failed to retrieve vulnerability information for {plugin}{Color.reset}")