from core.color import Color
from core.utility import create_report_folder
from scan.bhttprobe import better_httprobe
import subprocess
import re

def waf_scanning(target):
    create_report_folder(target)
    try:
        host = better_httprobe(target)
        waf_output = subprocess.check_output(f"wafw00f {host}", shell=True, text=True)
        # print(waf_output)  # Uncomment for debugging if needed
        if "is behind" in waf_output:
            # Extract WAF name
            match = re.search(r'is behind\s(.+?)\s\(', waf_output)
            if match:
                wafname = match.group(1).strip()
                print(f"{Color.bold}{Color.green}\n\t  [+] WAF: DETECTED [ {wafname} ]{Color.reset}")
            else:
                print(f"{Color.bold}{Color.red}\n\t  [-] WAF: DETECTION FAILED {Color.reset}")
        else:
            print(f"{Color.bold}{Color.yellow}\n\t  [-] WAF: NOT DETECTED {Color.reset}")
    except subprocess.CalledProcessError as e:
        print(f"{Color.bold}{Color.red}\n\t  [-] ERROR: {e}{Color.reset}")
