## fitur should be add
## cms scanner, and maybe auto bruteforce cms with weakpass list
## 1.1: importing dependencies
from turtle import color


try:
	from os import path, system, getcwd
	import os.path
	import subprocess
	import nmap
	import json
	import sys
	import time
except ImportError as error:
	print("\n\t   [!] Error on import", error)

## 1.2: defining classes & functions:
class Colors:
	RESET     = "\33[0m"
	BOLD      = "\33[1m"
	RED       = "\33[31m"
	GREEN     = "\33[32m"
	YELLOW    = "\33[33m"

## 1.4 checking dependecies tools

def check(tool):
  if os.path.exists("/usr/bin/" + tool) == True:
	  print(Colors.GREEN + Colors.BOLD + "[*] " + tool +  " exist" + Colors.RESET)
	  time.sleep(0.2)
	  pass

  elif os.path.exists("/usr/bin" + tool) == False:
	  # checking user privileges
	  user = os.getuid()
	  
	  if user == 0:
		  pass

	  else:
		  print(Colors.RED + Colors.BOLD + "[!] " + tool + " is missing, Please run me with sudo to install " + tool + Colors.RESET)
		  exit()
	  # installing missing requirements
	  print(Colors.RED + Colors.BOLD + "[!] " + tool + " missing" + Colors.RESET)
	  print(Colors.RED + Colors.BOLD + "[!] installing " + tool + Colors.RESET)
	  time.sleep(0.2)
	  system("apt install "+ tool + " -y")

# requirements
list_tool = ['nmap','wafw00f','sublist3r','subfinder','assetfinder','amass','dirsearch','httprobe']
for tool in list_tool:
  check(tool)
  pass

def break_and_help():
	print("\n\t   [?] Usage example: sicon -u target.com")
	exit()

def remove_list_files(extension):
	system("rm -rf .list*.%s" % extension)



## 1.4: preparing everything
saving_path = getcwd() + "/"
port_scan = nmap.PortScanner()

## 1.5: "welcome" screen
system("clear")
print(Colors.GREEN + Colors.BOLD + """
\t          ┏━┓╺┓ ┏━╸┏━┓┏┓╻
\t          ┗━┓ ┃ ┃  ┃┃┃┃┗┫
\t          ┗━┛╺┻╸┗━╸┗━┛╹ ╹
                
                    Simple Recon
                Coded by """ + Colors.RESET + Colors.RED + Colors.BOLD + """UnknownSec666""" + Colors.RESET + Colors.GREEN + Colors.BOLD + """
		   Thanks to:""" + Colors.RED + Colors.BOLD + """ Jeager""" +
Colors.RESET)

## 1.6: getting started
command_arguments = sys.argv[1:]

if (len(command_arguments) > 0):
	flag = command_arguments[0].upper()

	if flag == "-U" or flag == "--URL":
		URL_TARGET = command_arguments[1]

	else:
		break_and_help()

else:
	break_and_help()



## 2.0: Starting recon phase:
print(Colors.BOLD + Colors.GREEN + "\n\t[*] Starting recon on %s:" % URL_TARGET + Colors.RESET)

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

	print(Colors.BOLD + Colors.GREEN + "\n\t  [+] WAF: DETECTED [ %s ]" % which_waf + Colors.RESET)

elif ("No WAF detected" in detect_waf):
	print(Colors.BOLD + Colors.YELLOW + "\n\t  [+] WAF: NOT DETECTED" + Colors.RESET)

else:
	print(Colors.BOLD + Colors.RED  + "\n\t  [!] FAIL TO DETECT WAF" + Colors.RESET)

### 2.2: Scanning ports using nmap
# run NMAP and filter results using GREP 
system("nmap %s -o .list_NMAP.txt > /dev/null" % URL_TARGET)
system("cat .list_NMAP.txt | grep open > .list_PORTS.txt")

# open file we just created
with open(".list_PORTS.txt", encoding="utf-8") as file:
	ports_list = file.read().splitlines()

# remove files we just created
remove_list_files("txt")

print(Colors.BOLD + Colors.GREEN + "\n\t  [+] OPENED PORTS: %s" % len(ports_list) + Colors.RESET)

for p in ports_list:
	print(Colors.RESET + "\t    " + Colors.GREEN + "-> " + Colors.RESET + Colors.BOLD + p)

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

remove_list_files("txt")

print(Colors.BOLD + Colors.GREEN + "\n\t  [+] SUBDOMAINS DETECTED: %s" % len(subdomain_list) + Colors.RESET)

for s in subdomain_list:

	# perform quick port scan using nmap
	quick_scan = port_scan.scan(hosts=s, arguments="-F")
	host = list(quick_scan["scan"].keys())
	
	if (len(host) > 0):
		# tcp ports were found
		tcp_open = str(list(quick_scan["scan"][host[0]]["tcp"].keys()))
		print(Colors.RESET + Colors.GREEN + "\t    -> " + Colors.RESET + Colors.BOLD + s +
										" | " +  Colors.GREEN + tcp_open + Colors.RESET)
	else:
		# port scan failed
		print(Colors.RESET + Colors.GREEN + "\t    -> " + Colors.RESET + Colors.BOLD + s +
										" | " +  Colors.RED + "FAIL MAYBE HOST DIED" + Colors.RESET)

### 2.4: Bruteforcing json_directory:
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

print(Colors.BOLD + Colors.GREEN + "\n\t  [+] DIRECTORIES: %s" % len(sorted_directories) + Colors.RESET)

for d in sorted_directories:

	format_host = get_host.replace("\n", "")

	if (d[0] == 200):
		# green alert
		print(Colors.GREEN + "\t    -> " + Colors.RESET + Colors.GREEN
				+ str(d[0]) + Colors.RESET + " | " +  Colors.BOLD + format_host + d[1] + Colors.RESET)
	
	elif (d[0] == 403):
		print(Colors.GREEN + "\t    -> " + Colors.RESET + Colors.YELLOW 
				+ str(d[0]) + Colors.RESET + " | " +  Colors.BOLD + format_host + d[1] + Colors.RESET)