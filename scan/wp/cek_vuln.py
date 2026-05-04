from core.color import Color
from core.random_ag import rangent
import requests
import re
import html

def parse_version(v_str):
    parts = []
    for p in v_str.split('.'):
        try:
            parts.append(int(p))
        except ValueError:
            num = ''.join(c for c in p if c.isdigit())
            parts.append(int(num) if num else 0)
    return parts

def is_vulnerable(current, fixed):
    v1 = parse_version(current)
    v2 = parse_version(fixed)
    length = max(len(v1), len(v2))
    v1.extend([0] * (length - len(v1)))
    v2.extend([0] * (length - len(v2)))
    return tuple(v1) < tuple(v2)

def cek_vuln(plugin, versi, user_agent=None):
    if user_agent:
        headers = {"User-Agent": user_agent}
    else:
        headers = {"User-Agent": rangent()}
    try:
        wpscan = f"https://wpscan.com/plugin/{plugin}"
        rscan = requests.get(wpscan, timeout=10, headers=headers).text
        
        version_pattern = r"Fixed in\s+(\d+\.\d+\.\d+)"
        title_pattern = r'Title\s*</div>\s*<a href="[^"]+">\s*([^<]+)'
        
        versions = re.findall(version_pattern, rscan)
        titles = re.findall(title_pattern, rscan)
        
        vulnerabilities_found = []
        for vuln_version, title in zip(versions, titles):
            if is_vulnerable(versi, vuln_version):
                clean_title = html.unescape(title).strip()
                vulnerabilities_found.append(clean_title)
                
        if vulnerabilities_found:
            print(f"{Color.green}\t\t[+]{Color.reset} {Color.bold}{plugin}{Color.reset} with version {versi} is {Color.green}{Color.bold}vulnerable{Color.reset}")
            
            # Limit the output to top 5 to prevent spamming
            # display_limit = 5
            for title in vulnerabilities_found:
                print(f"\t\t   {Color.green}->{Color.reset} {Color.yellow}{Color.bold}{title}{Color.reset}")
                
            # if len(vulnerabilities_found) > display_limit:
                # print(f"\t\t   {Color.green}->{Color.reset} {Color.yellow}{Color.bold}... and {len(vulnerabilities_found) - display_limit} more vulnerabilities.{Color.reset}")
                
    except requests.exceptions.RequestException:
        print(f"{Color.red}\t\t[!] Failed to retrieve vulnerability information for {plugin}{Color.reset}")
