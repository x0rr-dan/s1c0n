## 1.1: importing dependencies
from os import path, system, getcwd
import os.path, subprocess, json, requests,json, sys, time, re


#lireq = ['python-nmap','requests','json']

### ADD IMPROVEMENT U DUMP SHIT

try:
	import nmap
	#import requests
	#import json
except ImportError as error:
    print("\n\t   [!] Error on import", error)
    system("pip3 install python-nmap")

## 1.2: defining classes & functions:
class co:
    re = "\33[0m"
    bo = "\33[1m"
    r = "\33[31m"
    g = "\33[32m"
    ye = "\33[33m"


## 1.3 detect distro for install tools
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
     

## 1.4 checking dependencies tools
def check(tool):
    if os.path.exists(f"/usr/bin/{tool}"):
        print(f"{co.g}{co.bo}[*] {tool} exist{co.re}")
        time.sleep(0.2)
    else:
        # checking user privileges
        user = os.getuid()

         # installing missing requirements
        print(f"{co.r}{co.bo}[!] {tool} missing{co.re}")
        print(f"{co.r}{co.bo}[!] installing {tool}{co.re}")
        time.sleep(0.2)
        dis = distro()
        if dis == 'arch':
            if tool == 'httprobe':
                aur = f"{tool}-bin"
            else:
                aur = tool
            system(f"yay -S --noconfirm {aur}")
        elif dis == 'debian':
             if user == 0:
                  system(f"apt install {tool} -y")
             else:
                  print(f"{co.r}{co.bo}[!] {tool} is missing, Please run me with sudo to install {tool}{co.re}")
                  exit()
        elif dis == 'kali':
             if user == 0:
                  system(f"apt install {tool} -y")
             else:
                  print(f"{co.r}{co.bo}[!] {tool} is missing, Please run me with sudo to install {tool}{co.re}")
                  exit()
        elif dis == 'parrot':
             if user == 0:
                  system(f"apt install {tool} -y")
             else:
                  print(f"{co.r}{co.bo}[!] {tool} is missing, Please run me with sudo to install {tool}{co.re}")
                  exit()
        else:
             print("[!] ur not using linux ...")

# requirements
list_tool = ['nmap','wafw00f','sublist3r','subfinder','assetfinder','amass','dirsearch','httprobe']
for tool in list_tool:
    check(tool)


def break_and_help():
    print("\n\t   [?] Usage example: sicon -u target.com")
    exit()


def remove_list_files(extension):
    system(f"rm -rf .list*.{extension}")


## 1.5: preparing everything
saving_path = getcwd() + "/"
port_scan = nmap.PortScanner()


## 1.6: "welcome" screen
system("clear")
print(co.g + co.bo + """
\t          ┏━┓╺┓ ┏━╸┏━┓┏┓╻
\t          ┗━┓ ┃ ┃  ┃┃┃┃┗┫
\t          ┗━┛╺┻╸┗━╸┗━┛╹ ╹ v1.5 (not finish yet)
                
                    Simple Recon
          Coded by """ + co.re+ co.r + co.bo + """root@x-krypt0n-x A.K.A x0r""" + co.r + co.bo + """\n\t          System of Pekalongan""" +
co.re)

## 1.7: getting started
command_arguments = sys.argv[1:]

if (len(command_arguments) > 0):
	flag = command_arguments[0].upper()

	if flag == "-U" or flag == "--URL":
		URL_TARGET = command_arguments[1]

	else:
		break_and_help()

else:
	break_and_help()


os.mkdir("report_"+URL_TARGET)
## 2.0: Starting recon phase:
print(co.bo + co.g + "\n\t[*] Starting recon on %s:" % URL_TARGET + co.re)

## 2.1: Detect WAF using wafw00f:
# convert to domain using httprobe
get_host   = subprocess.check_output(("echo %s | httprobe -prefer-https" % URL_TARGET), shell=True, text=True)
detect_waf = subprocess.check_output(("wafw00f %s > /dev/null" % get_host), shell=True, text=True)

if ("is behind" in detect_waf):
	## has some WAF
	processed_string = detect_waf[detect_waf.find("is behind"):]
	pre_parser  = processed_string.find("\x1b[1;96m") # process to get valuable results only
	post_parser = processed_string.find("\x1b[0m")
	which_waf   = processed_string[pre_parser:post_parser] # don't include color codes

	print(co.bo + co.g + "\n\t  [+] WAF: DETECTED [ %s ]" % which_waf + co.re)

elif ("No WAF detected" in detect_waf):
	print(co.bo + co.ye + "\n\t  [+] WAF: NOT DETECTED" + co.re)

else:
	print(co.bo + co.r  + "\n\t  [!] FAIL TO DETECT WAF" + co.re)

### 2.2: Scanning ports using nmap
# run NMAP and filter results using GREP 
system("nmap %s -o .list_NMAP.txt > /dev/null" % URL_TARGET)
system("cat .list_NMAP.txt | grep open > .list_PORTS.txt")

# open file we just created
with open(".list_PORTS.txt", encoding="utf-8") as file:
	ports_list = file.read().splitlines()

# remove files we just created
remove_list_files("txt")

print(co.bo + co.g + "\n\t  [+] OPENED PORTS: %s" % len(ports_list) + co.re)

for p in ports_list:
	print(co.re+ "\t    " + co.g + "-> " + co.re+ co.bo + p)

### 2.3: Getting subdomains
# this process might take a while, we'll use different scripts for that
system("subfinder -d %s -o .list_subfinder.txt -silent > /dev/null" % URL_TARGET)
system("sublist3r -d %s -o .list_sublist3r.txt > /dev/null" % URL_TARGET)
system("assetfinder %s > .list_assetfinder.txt" % URL_TARGET)
system("amass enum -d %s -o .list_amass.txt -silent" % URL_TARGET)

# concat every output into one file
system("cat .list*.txt > .list_subdomains.txt")

# open "general" file
with open(".list_subdomains.txt", encoding="utf-8") as file:
	subdomain_raw_list = file.read().splitlines()

# drop duplicates
subdomain_list = set(subdomain_raw_list)

cpanel_subdomain = [subdomain_list for subdomain_list in subdomain_list if subdomain_list.startswith(("cpanel.", "webdisk.", "webmail.", "cpcontacts.", "whm.", "autoconfig.", "mail.", "cpcalendars.", "autodiscover."))]

not_cpanel_subdomain = [subdomain_list for subdomain_list in subdomain_list if not subdomain_list.startswith(("cpanel.", "webdisk.", "webmail.", "cpcontacts.", "whm.", "autoconfig.", "mail.", "cpcalendars.", "autodiscover."))]

# Save cpanel subdomains to file
with open(os.path.join("report_"+URL_TARGET, "cpanel_subdomain.txt"), "w") as f:
    f.write("\n".join(cpanel_subdomain))

# Save other subdomains to file, creating the file if it does not exist
with open(os.path.join("report_"+URL_TARGET, "subdomain.txt"), "w") as f:
    if not_cpanel_subdomain:
        f.write("\n".join(not_cpanel_subdomain))
    else:
        f.write("")

remove_list_files("txt")

print(co.bo + co.g + "\n\t  [+] SUBDOMAINS DETECTED: %s" % len(subdomain_list) + co.re)

for s in subdomain_list:
    # Perform quick port scan using nmap
    quick_scan = port_scan.scan(hosts=s, arguments="-F")
    
    # Check if 'scan' key exists in quick_scan
    if "scan" in quick_scan:
        host = list(quick_scan["scan"].keys())
        if len(host) > 0:
            # Check if 'tcp' key exists in quick_scan["scan"][host[0]]
            if "tcp" in quick_scan["scan"][host[0]]:
                tcp_open = str(list(quick_scan["scan"][host[0]]["tcp"].keys()))
                print(co.re + co.g + "\t    -> " + co.re + co.bo + s + " | " + co.g + tcp_open + co.re)
            else:
                # 'tcp' key not found
                print(co.re + co.g + "\t    -> " + co.re + co.bo + s + " | " + co.r + "No TCP ports found" + co.re)
        else:
            # Port scan failed
            print(co.re + co.g + "\t    -> " + co.re + co.bo + s + " | " + co.r + "HOST OFFLINE" + co.re)
    else:
        # 'scan' key not found
        print(co.re + co.g + "\t    -> " + co.re + co.bo + s + " | " + co.r + "Scan data not available" + co.re)


### checking cms 2.4:
wp_regex = re.compile(r'wp-')
joomla_regex = re.compile(r'joomla')

print(co.bo + co.g + "\n\t  [+] CMS DETECTEION: " + co.re)

for url in not_cpanel_subdomain:
    try:
        response = requests.get('http://'+url, timeout=5)
        if response.status_code == 200:
            text = response.text
            if wp_regex.search(text):
                print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | Wordpress" + co.re)
                with open(os.path.join("report_"+URL_TARGET, "wp.txt"), "a") as f:
                    f.write("http://"+ url + "\n")
            elif joomla_regex.search(text):
                print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | Joomla" + co.re)
                with open(os.path.join("report_"+URL_TARGET, "joomla.txt"), "a") as f:
                    f.write("http://"+ url + "\n")
            else:
                print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | " +  co.r + "FAIL DETECT CMS" + co.re)
        else:
            print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | " +  co.r + "HOST OFFLINE WITH CODE "+ str(response.status_code) + co.re)
    except requests.exceptions.RequestException as e:
        print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | " +  co.r + "COULD NOT BE REACHED " + co.re)

### 2.5 checking if any missconfiguration in wordpress site
wp_install = re.compile(r'Welcome to WordPress. Before getting started, you will need to know the following items.')
print(co.bo + co.g + "\n\t  [+] WP INSTALL DETECTION: " + co.re)
# read all wordpress
# Bug give a logic to check if there have a wp.txt
with open("report_"+URL_TARGET, "wp.txt", encoding="utf-8") as file:
    subdomain_wp = file.read().splitlines()
# list path wp install
list_install = ['/BACKUP','/BAK','/wordpress','/wordpress1']
for wppp in subdomain_wp:
    for ins in list_install:
        try:
            response = requests.get(wppp +ins, timeout=60)
            if response.status_code == 200:
                text = response.text
                if wp_install.search(text):
                    print(co.re + co.g + "\t    -> " + co.re+ co.bo + wppp + ins +" | Must be vulnerable with wp install"+ co.re)
                    with open(os.path.join("report_"+URL_TARGET, "wp-install.txt"), "a") as f:
                        f.write("http://"+ wppp + ins + "\n")
                elif response.status_code == 404:
                    print(co.re + co.g + "\t    -> " + co.re + co.bo + wppp + ins + " | " + co.r + "Not Found"+co.re)    
                else:
                    print(co.re + co.g + "\t    -> " + co.re+ co.bo + wppp + ins +" | " + co.r + "Not vuln"+ co.re)
            else:
                print(co.re + co.g + "\t    -> " + co.re+ co.bo + wppp +" | " + co.r + "Something wrong"+ co.re)
        except requests.exceptions.ConnectionError:
            print(co.re + co.g + "\t    -> "+ co.re + co.bo + wppp + ins + " | " + co.r + "Cant be reached host is offline" + co.re)

### 2.6: Bruteforcing json_directory:
system("dirsearch -u {} -o {} --format=json > /dev/null".format(URL_TARGET, (saving_path + ".list_json_directory.json")))

with open(".list_json_directory.json", encoding="utf-8") as file:
	json_directory = json.load(file)
	
remove_list_files("json")

host      = str( list(json_directory["results"][0].keys())[0] )
directory = json_directory["results"][0][host]

dir_list = []
for d in directory:
	path = d["path"]
	status = d["status"]

	# drop other codes
	if (status == 200 or status == 403):
		dir_list.append([status, path])

sorted_directories = sorted(dir_list)

print(co.bo + co.g + "\n\t  [+] DIRECTORIES: %s" % len(sorted_directories) + co.re)

for d in sorted_directories:

	format_host = get_host.replace("\n", "")

	if (d[0] == 200):
		# g alert
		print(co.g + "\t    -> " + co.re+ co.g
				+ str(d[0]) + co.re+ " | " +  co.bo + format_host + d[1] + co.re)
	
	elif (d[0] == 403):
		print(co.g + "\t    -> " + co.re+ co.ye 
				+ str(d[0]) + co.re+ " | " +  co.bo + format_host + d[1] + co.re)
