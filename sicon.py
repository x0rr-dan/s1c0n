# importing dependencies
import sys, argparse, sys
from core.color import Color
from core.check import check
from core.utility import logo, break_and_help
from scan.wafscan import waf_scanning
from scan.portscan import port_scanning
from scan.subscan import subdo_scanning
from scan.cmsscan import cms_detection
from scan.scandir import scan_dir
from scan.techscan import more_info
from scan.wp.wp_enum import wp_enum

def main():
    logo()
    parser = argparse.ArgumentParser(description=break_and_help(), usage="""\nsicon -u site.com -o waf subdo     only do waf scanning and subdomain scanning\nsicon -u site.com -o scan_dir      only do waf scanning and subdomain scanning\nsicon -u site.com -o port subdo    only do port scanning and subdomain scanning\nsicon -u site.com                  scan with all options """)
    parser.add_argument("-o", "--option", nargs="+", choices=["waf", "port", "subdo", "scan_dir"], default=["all"], help="Choose one scan option, eg: ")
    parser.add_argument("-u", "--url", required=True, help="url target")
    parser.add_argument("-a", "--user-agent", help="custom user-agent in scan dir, cms detection, technology detection")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    command = parser.parse_args()
    url_target = command.url
    options = command.option
    ag = command.user_agent
    
    list_tool = ['nmap','wafw00f','sublist3r','subfinder','assetfinder','dirsearch','httprobe']
    for tool in list_tool:
        check(tool)
        

    if "all" in options:
        print(f"{Color.bold}{Color.green}\n\t[*] Starting recon on : {url_target}{Color.reset}")
        waf_scanning(url_target)
        port_scanning(url_target)
        subdo_scanning(url_target)
        more_info(url_target, ag)
        cms_detection(url_target, ag)
        wp_enum(url_target, ag)
        scan_dir(url_target, ag)
    else:
        print(f"{Color.bold}{Color.green}\n\t[*] Starting recon on : {url_target}{Color.reset}")
        if "waf" in options:
            waf_scanning(url_target)
        if "port" in options:
            port_scanning(url_target)
        if "subdo" in options:
            subdo_scanning(url_target)
            more_info(url_target, ag)
            cms_detection(url_target, ag)
            wp_enum(url_target, ag)
        if "scan_dir" in options:
            scan_dir(url_target ,ag)
    
if __name__ == "__main__":
    main()
