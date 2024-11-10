# importing dependencies
from os import path, system, getcwd, getuid, mkdir
import subprocess
import json
import requests
import sys
import time
import re
import builtwith
import time
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
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
                  print(f"{Color.r}{Color.bold}[!] {tool} is missing, Please run me with sudo to install {tool}{Color.reset}")
                  exit()
        else:
             print("[!] ur not using linux ...")
# 1.3 wellcome screen
def logo():
    system("clear")
    print(Color.green + Color.bold + """
    \t              ┏━┓╺┓ ┏━╸┏━┓┏┓╻
    \t              ┗━┓ ┃ ┃  ┃┃┃┃┗┫
    \t              ┗━┛╺┻╸┗━╸┗━┛╹ ╹ v1.8

                        Simple Recon
                        Coded by """ + Color.reset + Color.red + Color.bold + """x0r""" + Color.yellow + Color.bold + """\n\t       https://github.com/x0rr-dan/s1c0n"""  + Color.red + Color.bold + """\n\t           Dinus Open Source Community""" + Color.red)
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
    wgex = re.compile(r'(?:<meta name="generator" content="WordPress|/wp-content/)') # wordpress
    jgex = re.compile(r'(?:<meta name="generator" content="Joomla|/media/system/js/)') # joomla
    druex = re.compile(r'(?:<meta name="generator" content="Drupal|/sites/all/)') # drupal
    moex = re.compile(r'(?:<meta name="keywords" content="moodle|/core/)') # moodle
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
                elif druex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Drupal{Color.reset}")
                    with open(path.join(f"report_{target}", "drupal.txt"), "a") as f:
                        f.write("http://"+ url + "\n")
                elif moex.search(text):
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.green}Moodle{Color.reset}")
                    with open(path.join(f"report_{target}", "moodle.txt"), "a") as f:
                        f.write("http://"+ url + "\n")
                else:
                    pass
            else:
                print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.red}ERROR {str(response.status_code)}{Color.reset}")
        except requests.exceptions.RequestException:
            print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.red}COULD NOT BE REACHED {Color.reset}")
            
# 1.10 checking dir using dirsearch
def scan_dir(target):
    path = f"{getcwd()}/"
    system(f"dirsearch -u {target} -o {path}.list_dir.json --format=json > /dev/null")
    if path.exist(f"{target}/.list_dir.json"):
        with open(".list_dir.json", encoding="utf-8") as dir:
            jdir = json.load(dir)
            if jdir:
                clean("json")
                dir_found = jdir["results"]
                list_dir_found = []
                for d in dir_found:
                    path_dir = d["url"]
                    status_dir = d["status"]
                    if status_dir in [200, 403, 500, 404]:
                        list_dir_found.append([status_dir, path_dir])

                sorted_dir = sorted(list_dir_found)
                print(f"{Color.bold}{Color.green}\n\t  [+] DIRECTORIES: {len(sorted_dir)}{Color.reset}")
                for d in sorted_dir:
                    if d[0] == 200:
                        print(f"{Color.green}\t    -> {Color.reset}{Color.green}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
                    elif d[0] == 403:
                        print(f"{Color.green}\t    -> {Color.reset}{Color.red}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
                    elif d[0] == 500:
                        print(f"{Color.green}\t    -> {Color.reset}{Color.red}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
                    elif d[0] == 404:
                        print(f"{Color.green}\t    -> {Color.reset}{Color.yellow}{str(d[0])}{Color.reset} | {Color.bold} {d[1]}{Color.reset}")
            else:
                print(f"{Color.bold}{Color.red}\n\t  [-] DIRECTORIES SCANNER CANT FIND ANYTHING USEFULL{Color.reset}")
    else:
        print(f"{Color.bold}{Color.red}\n\t [-] Something wrong went running dirsearch for directory scanner{Color.reset}")

# 1.11 detecting technology but have some bug in output
def more_info(target):  
    try:
        with open(f"report_{target}/subdomain.txt", 'r', encoding='utf-8') as r:
            read_subdo = r.readlines()
        
        print(f"{Color.bold}{Color.green}\n\t  [+] WEB TECHNOLOGY: {len(read_subdo)} sites{Color.reset}")
        
        output_file_path = f"report_{target}/subdomain_with_tech.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for url in read_subdo:
                url = f"https://{url.strip()}"
                try:
                    # detected technology target using builtwith
                    data = builtwith.builtwith(url)
                    keys_of_interest = ['web-servers', 'javascript-frameworks', 'web-frameworks']
                    technologies = []
                    for key in keys_of_interest:
                        if key in data:
                            technologies.extend(data[key])
                    technologies_str = " | ".join(technologies) if technologies else f"{Color.red}No technology detected"
                    
                    # detected laravel from cookie
                    try:
                        response = requests.get(url)
                        cookies = response.cookies
                        if 'XSRF-TOKEN' in cookies or 'laravel_session' in cookies:
                            technologies_str += " | Laravel"
                    except requests.exceptions.RequestException:
                        technologies_str += " | Failed to retrieve data"
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

# 1.12 wp plugin enum
# wp enum, scan user, plugin etc
# wp enum i think done but idk, it will update soon
# wp user enum is under development
def wp_enum(target):
    # read wordpress file that save in folder report
    if path.exists(f"report_{target}/wp.txt"):
        with open(f"report_{target}/wp.txt", 'r', encoding='utf-8') as r:
            read_subdo = r.readlines()
            print(f"{Color.bold}{Color.green}\n\t  [+] WORDPRESS ENUMERATION: {len(read_subdo)} sites{Color.reset}")
            for i in read_subdo:
                i = i.strip()
                wpplugin(i)
                time.sleep(5)
    else:
        pass
# checking in index that have any plugin
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

# check plugin if there is a changelog or readme in inside plugin folder
# overall this technique is helpfull
def check_plugin(target_site, plugin, page_content):
    detect = set()
    for file in ["changelog.txt", "readme.txt"]:
        try:
            e = requests.get(f"{target_site}/wp-content/plugins/{plugin}/{file}", timeout=10)
            if e.status_code == 200:
                topver = re.search(r"== Changelog ==\s+= ([\d.]+) - (\d{4}-\d{2}-\d{2}) =", e.text) or \
                         re.search(r"= ([\d.]+) - (\d{4}-\d{2}-\d{2}) =", e.text)
                if topver:
                    versi = topver.group(1)
                    detect.add(plugin)
                    cek_db(target_site, plugin, versi)
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
                a = requests.get(asset, timeout=10)
                version_in_header = re.search(r"Version:\s*([\d.]+)", a.text)
                if version_in_header:
                    versi = version_in_header.group(1)
                    detect.add(plugin)
                    cek_db(target_site, plugin, versi)
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
            cek_db(target_site, plugin, versi)

# check if plugin version is last update
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

# check if the plugin is out of date then compare it in wpscan, and scrap it if found the version if vulnerable based on version plugin
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
            # 2.3 scanning
            try:
                print(f"{Color.bold}{Color.green}\n\t[*] Starting recon on : {URL_TARGET}{Color.reset}")
                waf_scanning(URL_TARGET)
                port_scanning(URL_TARGET)
                subdo_scanning(URL_TARGET)
                more_info(URL_TARGET)
                cms_detection(URL_TARGET)
                wp_enum(URL_TARGET)
                scan_dir(URL_TARGET)
            except KeyboardInterrupt:
                print(f"{Color.bold}[!] Keyboard Interupt\n[!] Exit ... {Color.reset}")
        else:
            break_and_help()
    else:
        break_and_help()

if __name__ == "__main__":
    main()
