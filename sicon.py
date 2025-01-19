# importing dependencies
import sys, argparse, sys
from core.color import Color
from core.check import check
from core.utility import logo, break_and_help, make_sure
from scan.wafscan import waf_scanning
from scan.portscan import port_scanning
from scan.subscan import subdo_scanning
from scan.cmsscan import cms_detection
from scan.scandir import scan_dir
from scan.techscan import more_info
from scan.wp.wp_enum import wp_enum

def main():
    parser = argparse.ArgumentParser(description=break_and_help(), usage="""\nsicon -u site.com -o waf subdo     only do waf scanning and subdomain scanning\nsicon -u site.com -o scan_dir      only do waf scanning and subdomain scanning\nsicon -u site.com -o port subdo    only do port scanning and subdomain scanning\nsicon -u site.com                  scan with all options\n\nexample usage:\nsicon -u site.com --proxy='socks5://127.0.0.1:1080' --user-agent='Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X)'      scan with all option and using proxy and custom user-agent""")
    parser.add_argument("-o", "--option", nargs="+", choices=["waf", "port", "subdo", "scan_dir"], default=["all"], help="Choose one scan option, eg: ")
    parser.add_argument("-u", "--url", required=True, help="url target")
    parser.add_argument("-a", "--user-agent", help="custom user-agent in scan dir, cms detection, technology detection")
    parser.add_argument("-t", "--tor", action="store_true", help="scanning with tor network to hide ur ass")
    parser.add_argument("-p", "--proxy", help="set a custom proxy, e.g., http://proxyserver:port or socks5://proxyserver:port")

    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        logo()
        parser.print_help()
        sys.exit(1)

    list_tool = ['nmap','wafw00f','sublist3r','subfinder','assetfinder','dirsearch','httprobe']
    for tool in list_tool:
        check(tool)
    logo()
    command = parser.parse_args()
    url_target = command.url
    options = command.option
    ag = command.user_agent
    tor = command.tor
    proxy = command.proxy

    # Set proxy based on user input or Tor
    if tor:
        torproxy = "socks5://127.0.0.1:9050"
        proxy = torproxy
        if make_sure(proxy) == False:
            print(f"{Color.bold}{Color.red}\n[!] Tor is not active ...{Color.reset}")
            exit(1)


    if "all" in options:
        print(f"{Color.bold}{Color.green}\n\t[*] Starting recon on : {url_target}{Color.reset}")
        waf_scanning(url_target)
        port_scanning(url_target)
        subdo_scanning(url_target)
        more_info(url_target, ag, proxy)
        cms_detection(url_target, ag, proxy)
        wp_enum(url_target, ag, proxy)
        scan_dir(url_target, ag, proxy)
    else:
        print(f"{Color.bold}{Color.green}\n\t[*] Starting recon on : {url_target}{Color.reset}")
        if "waf" in options:
            waf_scanning(url_target)
        if "port" in options:
            port_scanning(url_target)
        if "subdo" in options:
            subdo_scanning(url_target)
            more_info(url_target, ag, proxy)
            cms_detection(url_target, ag, proxy)
            wp_enum(url_target, ag, proxy)
        if "scan_dir" in options:
            scan_dir(url_target ,ag, proxy)
    
if __name__ == "__main__":
    main()
