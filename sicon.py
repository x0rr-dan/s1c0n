# importing dependencies
import sys
from core.color import Color
from core.check import check
from core.utility import logo
from core.utility import break_and_help
from scan.wafscan import waf_scanning
from scan.portscan import port_scanning
from scan.subscan import subdo_scanning
from scan.cmsscan import cms_detection
from scan.scandir import scan_dir
from scan.techscan import more_info
from scan.wp.wp_enum import wp_enum

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
