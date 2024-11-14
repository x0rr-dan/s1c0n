from core.color import Color
from core.distro import distro
from os import path, system
from core.utility import clean
from core.utility import create_report_folder
import subprocess

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
