from os import path, getuid
from core.distro import distro
from core.color import Color
import subprocess
import time
import sys

# 1.2 checking tools 
def check(tool):
    if path.exists(f"/usr/bin/{tool}") or path.exists(f"/usr/local/bin/{tool}"):
        print(f"{Color.green}{Color.bold}[*] {tool} exist{Color.reset}")
        time.sleep(0.2)
    else:
        # checking user privileges
        user = getuid()
         # installing missing requirements
        print(f"{Color.red}{Color.bold}[!] {tool} missing{Color.reset}")
        print(f"{Color.red}{Color.bold}[!] installing {tool}{Color.reset}")
        time.sleep(0.2)
        dis = distro()
        if dis in ['arch','blackarch']:
            if path.exists("/usr/bin/yay"):
                if tool == 'httprobe':
                    aur = f"{tool}-bin" if tool == 'httprobe' else tool
                    process = subprocess.run(['yay', '-S', '--noconfirm', f'{aur}'], capture_output=True, text=True)
                    if process.returncode != 0:
                        print(f"{Color.red}[-] Failed to install {Color.bold}{aur}{Color.reset}")
                        print(f"{Color.red}[-] Error output: {Color.bold}{process.stderr}{Color.reset}")
                        sys.exit(1)
                    else:
                        pass
                else:
                     aur = tool
                     process = subprocess.run(['yay', '-S', '--noconfirm', f'{aur}'], capture_output=True, text=True)
                     if process.returncode != 0:
                        print(f"{Color.red}[-] Failed to install {Color.bold}{aur}{Color.reset}")
                        print(f"{Color.red}[-] Error output: {Color.bold}{process.stderr}{Color.reset}")
                        sys.exit(1)
                     else:
                        pass
            else:
                 print(f"{Color.re}{Color.bold}[!] yay is not installed, Please install yay and run this script again ...")
            
        elif dis in ['kali', 'parrot']:
             if user == 0:
                  process = subprocess.run(f"apt install {tool} -y")
                  if process.returncode != 0:
                    print(f"{Color.red}[-] Failed to install {Color.bold}{aur}{Color.reset}")
                    print(f"{Color.red}[-] Error output: {Color.bold}{process.stderr}{Color.reset}")
                    sys.exit(1)
                  else:
                    pass
             else:
                  print(f"{Color.red}{Color.bold}[!] {tool} is missing, Please run me with sudo to install {tool}{Color.reset}")
                  exit()
        else:
             print("[!] ur not using linux ...")
