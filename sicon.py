# importing dependencies
from os import path, system, getcwd, getuid, mkdir
import subprocess
import json
import requests
import sys
import time
import re
import builtwith
import urllib.error
# import nmap

# color text
class Color:
    reset = "\33[0m"
    bold = "\33[1m"
    red = "\33[31m"
    green = "\33[32m"
    yellow = "\33[33m"

# 1.1 checking distro, to install tools
def distro():
    try:
        ## read os-release to check the distro
        with open('/etc/os-release', 'r') as file:
             lines = file.readlines()
             for line in lines:
                  if line.startswith('ID='):
                       return line.split('=')[1].strip().strip('"')
    except FileNotFoundError:
         print("[-] /etc/os-release not found ...")
         print("[*] Your not using linux ... if u using mac or other opratation system u should install tools manually")
         pass
    return None

# 1.2 checking tools 
def check(tool):
    if path.exists(f"/usr/bin/{tool}"):
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
        if dis in ['arch','blackarch']: # arch based, i only test this script in arch if any distro based on arch can run this, please add issue https://github.com/root-x-krypt0n-x/s1c0n
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
            
        elif dis in ['kali', 'parrot']: # debian based u can add if u can, dont forget to add issue if any distro is not include but can install from apt https://github.com/root-x-krypt0n-x/s1c0n
             if user == 0:
                  process = subprocess.run(f"apt install {tool} -y")
                  if process.returncode != 0:
                    print(f"{Color.red}[-] Failed to install {Color.bold}{aur}{Color.reset}")
                    print(f"{Color.red}[-] Error output: {Color.bold}{process.stderr}{Color.reset}")
                    sys.exit(1)
                  else:
                    pass
             else:
                  print(f"{Color.r}{Color.bold}[!] {tool} is missing, Please run me with sudo to install {tool}{Color.reset}")
                  exit()
        else:
             print("[!] ur not using linux ...")
# 1.3 wellcome screen
def logo():
    system("clear")
    print(Color.green + Color.bold + """
    \t          ┏━┓╺┓ ┏━╸┏━┓┏┓╻
    \t          ┗━┓ ┃ ┃  ┃┃┃┃┗┫
    \t          ┗━┛╺┻╸┗━╸┗━┛╹ ╹ v1.6

                        Simple Recon
              Coded by """ + Color.reset + Color.red + Color.bold + """root@x-krypt0n-x A.K.A x0r""" + Color.yellow + Color.bold + """\n\thttps://github.com/root-x-krypt0n-x/s1c0n"""  + Color.red + Color.bold + """\n\t          System of Pekalongan""" + Color.red)
# 1.4 help
def break_and_help():
    print("\n\t   [?] Usage example: sicon -u target.com")

# 1.5 clean file that doesnt use
def clean(extension):
    system(f"rm -rf .list*.{extension}")

# 1.6 create folder report
def create_report_folder(target):
    folder_name = f"report_{target}"
    if not path.exists(folder_name):
        mkdir(folder_name)
    else:
        pass
# 1.7 detecting waf that target use
def waf_scanning(target):
    create_report_folder(target)
    try:
        host = subprocess.check_output(f"echo {target} | httprobe -prefer-https", shell=True, text=True).strip()
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


# 1.7 scanning open port and subdomain
def port_scanning(target):
    system(f"nmap -sV {target} -o .list_nmap.txt > /dev/null")
    system("cat .list_nmap.txt | grep open > .list_nmap_finish.txt")
    with open(".list_nmap_finish.txt", encoding="utf-8") as file_nmap:
        port = file_nmap.read().splitlines()
    clean("txt")
    print(f"{Color.bold}{Color.green}\n\t  [+] OPENED PORTS: {len(port)}{Color.reset}")
    for p in port:
        print(f"\t    {Color.green}-> {Color.reset}{Color.bold}{p}{Color.reset}")

# 1.8 scanning subdomain
def subdo_scanning(target):
    # importing nmap
    try:
        import nmap
    except ImportError as error:
        print("\n\t   [!] Error on import", error)
        dis = distro()
        if dis == 'arch':
            print("\n\t   [!] Installing python-nmap...")
            system("yay -S python-nmap --noconfirm")
        else:
            system("pip3 install python-nmap")
    # Ensure the report directory exists
    report_dir = f"{target}"
    create_report_folder(report_dir)
    port_scan = nmap.PortScanner()
    # Run subfinder and redirect output to /dev/null
    subprocess.run(["subfinder", "-d", f"{target}", "-o", ".list_subfinder.txt", "-silent"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Run sublist3r and redirect output to /dev/null
    subprocess.run(["sublist3r", "-d", f"{target}", "-o", ".list_sublist3r.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Run assetfinder and redirect output to /dev/null
    subprocess.run(["assetfinder", target], stdout=open('.list_assetfinder.txt', 'w'), stderr=subprocess.DEVNULL)
    # Combine the results
    system("cat .list*.txt > .list_subdo.txt")
    
    with open(".list_subdo.txt", encoding="utf-8") as subdo_file:
        subdo_list = subdo_file.read().splitlines()
    # remove dup
    subdoo_list = set(subdo_list)
    # separate cpanel and non-cpanel domains
    cpanel_subdo = [sub for sub in subdoo_list if sub.startswith(("cpanel.", "webdisk.", "webmail.", "cpcontacts.", "whm.", "autoconfig.", "mail.", "cpcalendars.", "autodiscover."))]
    not_cpanel_subdo = [sub for sub in subdoo_list if not sub.startswith(("cpanel.", "webdisk.", "webmail.", "cpcontacts.", "whm.", "autoconfig.", "mail.", "cpcalendars.", "autodiscover."))]
    
    with open(path.join(f"report_{report_dir}", "cpanel_subdomain.txt"), "w") as f:
        f.write("\n".join(cpanel_subdo))
    
    with open(path.join(f"report_{report_dir}", "subdomain.txt"), "w") as f:
        if not_cpanel_subdo:
            f.write("\n".join(not_cpanel_subdo))
        else:
            f.write("")
    
    clean("txt")
    
    print(f"{Color.bold}{Color.green}\n\t  [+] SUBDOMAINS DETECTED: {len(subdoo_list)}{Color.reset}")
    for su in subdoo_list:
        # python-nmap quick port scan
        qscan = port_scan.scan(hosts=su, arguments="-F")
        # just check if 'scan' key exists in qscan
        if "scan" in qscan:
            h = list(qscan["scan"].keys())
            if len(h) > 0:
                if "tcp" in qscan["scan"][h[0]]:
                    topen = str(list(qscan["scan"][h[0]]["tcp"].keys()))
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{su} | {Color.green}{topen}{Color.reset}")
                else:
                    print(f"{Color.reset}{Color.green}\t    -> {Color.reset}{Color.bold}{su} | {Color.red} THERE NO OPEN PORTS{Color.reset}")
            else:
                print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{su} | {Color.red}HOST OFFLINE{Color.reset}")
        else:
            print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{su} | {Color.red}SCAN DATA NOT AVAILABLE")

# 1.9 checking cms
def cms_detection(target):
    wgex = re.compile(r'wp-')
    jgex = re.compile(r'joomla')
    with open(f"report_{target}/subdomain.txt", 'r', encoding='utf-8') as r:
        read_subdo = r.readlines()
    print(f"{Color.bold}{Color.green}\n\t  [+] CMS DETECTION: {len(read_subdo)} sites{Color.reset}")
    for url in read_subdo:
        url = url.strip()
        try:
            response = requests.get(f'https://{url}', timeout=60)
            if response.status_code == 200:
                text = response.text
                if wgex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Wordpress{Color.reset}")
                    with open(path.join(f"report_{target}", "wp.txt"), "a") as f:
                        f.write("http://"+ url + "\n")
                elif jgex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Joomla{Color.reset}")
                    with open(path.join(f"report_{target}", "joomla.txt"), "a") as f:
                        f.write("http://"+ url + "\n")
                else:
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.yellow}FAIL DETECT CMS{Color.reset}")
            else:
                print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.red}ERROR {str(response.status_code)}{Color.reset}")
        except requests.exceptions.RequestException:
            print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.red}COULD NOT BE REACHED {Color.reset}")
            
# 1.10 checking dir using dirsearch
def scan_dir(target):
    path = f"{getcwd()}/"
    system(f"dirsearch -u {target} -o {path}.list_dir.json --format=json > /dev/null")
    with open(".list_dir.json", encoding="utf-8") as dir:
        jdir = json.load(dir)
    clean("json")
    dir_found = jdir["results"]
    list_dir_found = []
    for d in dir_found:
        path_dir = d["url"]
        status_dir = d["status"]
        if status_dir in {200, 403, 500}:
            list_dir_found.append([status_dir, path_dir])
    
    sorted_dir = sorted(list_dir_found)
    print(f"{Color.bold}{Color.green}\n\t  [+] DIRECTORIES: {len(sorted_dir)}{Color.reset}")
    for d in sorted_dir:
        if d[0] == 200:
            print(f"{Color.green}\t    -> {Color.reset}{Color.green}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
        elif d[0] == 403:
            print(f"{Color.green}\t    -> {Color.reset}{Color.yellow}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
        elif d[0] == 500:
            print(f"{Color.green}\t    -> {Color.reset}{Color.red}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")

# 1.11 more information about target, showing the technoloy that target use, but there is bug, when target is unreachable it will show error message  from librarry urillib that idk how to hide that error
def remove_color_codes(text):
    """Hapus kode warna ANSI dari teks."""
    ansi_escape = re.compile(r'\x1b[^m]*m')
    return ansi_escape.sub('', text)

def more_info(target):  
    try:
        with open(f"report_{target}/subdomain.txt", 'r', encoding='utf-8') as r:
            read_subdo = r.readlines()
        
        print(f"{Color.bold}{Color.green}\n\t  [+] WEB TECHNOLOGY: {len(read_subdo)} sites{Color.reset}")
        
        # Menyiapkan file output
        output_file_path = f"report_{target}/subdomain_with_tech.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for url in read_subdo:
                url = f"https://{url.strip()}"
                try:
                    # Mendapatkan informasi teknologi dari builtwith
                    data = builtwith.builtwith(url)
                    keys_of_interest = ['web-servers', 'javascript-frameworks', 'web-frameworks']
                    technologies = []
                    for key in keys_of_interest:
                        if key in data:
                            technologies.extend(data[key])
                    technologies_str = " | ".join(technologies) if technologies else f"{Color.red}No technology detected"
                    
                    # Menambahkan deteksi Laravel
                    try:
                        response = requests.get(url)
                        cookies = response.cookies
                        if 'XSRF-TOKEN' in cookies or 'laravel_session' in cookies:
                            technologies_str += " | Laravel"
                    except requests.exceptions.RequestException:
                        technologies_str += " | Failed to retrieve data"
                    
                    # Menulis hasil ke file tanpa kode warna
                    output_file.write(f"{url} | {remove_color_codes(technologies_str)}\n")
                    
                    # Menampilkan hasil di konsol dengan kode warna
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} {Color.reset}| {Color.bold}{Color.green}[{technologies_str}{Color.green}]{Color.reset}")

                except urllib.error.URLError as e:
                    output_file.write(f"{url} | Failed to retrieve data: {e.reason}\n")
                    print(f"{Color.red}\t    -> {Color.reset}{Color.bold}{url} {Color.reset}| {Color.bold}{Color.red}Failed to retrieve data: {e.reason}{Color.reset}")
                except urllib.error.HTTPError as e:
                    output_file.write(f"{url} | HTTP Error: {e.code}\n")
                    print(f"{Color.red}\t    -> {Color.reset}{Color.bold}{url} {Color.reset}| {Color.bold}{Color.red}HTTP Error: {e.code}{Color.reset}")
                except Exception as e:
                    output_file.write(f"{url} | An unexpected error occurred: {e}\n")
                    print(f"{Color.red}\t    -> {Color.reset}{Color.bold}{url} {Color.reset}| {Color.bold}{Color.red}An unexpected error occurred: {e}{Color.reset}")

    except FileNotFoundError:
        print(f"{Color.red}File report_{target}/subdomain.txt not found.{Color.reset}")

def main():
    # 2.1 checking another tools that help this code run
    list_tool = ['nmap','wafw00f','sublist3r','subfinder','assetfinder','dirsearch','httprobe']
    for tool in list_tool:
        check(tool)
    logo()
    # 2.2 argsparser 
    command_arguments = sys.argv[1:]
    if (len(command_arguments) > 0):
        flag = command_arguments[0].upper()
        if flag == "-U" or flag == "--URL":
            URL_TARGET = command_arguments[1]
        else:
            break_and_help()
    else:
        break_and_help()
    # 2.3 scanning
    print(f"{Color.bold}{Color.green}\n\t[*] Starting recon on : {URL_TARGET}{Color.reset}")
    waf_scanning(URL_TARGET)
    port_scanning(URL_TARGET)
    subdo_scanning(URL_TARGET)
    more_info(URL_TARGET)
    cms_detection(URL_TARGET)
    scan_dir(URL_TARGET)
if __name__ == "__main__":
    main()
