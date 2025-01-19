## s1c0n
![Python](https://img.shields.io/badge/Python-3.9.2-blue)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

![Terkey](https://github-readme-stats.vercel.app/api/pin?username=x0rr-dan&repo=s1c0n&title_color=fff&icon_color=fff&text_color=ffffff&bg_color=000000)

```
    	             ┏━┓╺┓ ┏━╸┏━┓┏┓╻
    	             ┗━┓ ┃ ┃  ┃┃┃┃┗┫
    	             ┗━┛╺┻╸┗━╸┗━┛╹ ╹ v1.8

	      https://github.com/x0rr-dan/s1c0n
	          Dinus Open Source Community
usage: 
sicon -u site.com -o waf subdo     only do waf scanning and subdomain scanning
sicon -u site.com -o scan_dir      only do waf scanning and subdomain scanning
sicon -u site.com -o port subdo    only do port scanning and subdomain scanning
sicon -u site.com                  scan with all options

example usage:
sicon -u site.com --proxy='socks5://127.0.0.1:1080' --user-agent='Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X)'      scan with all option and using proxy and custom user-agent

options:
  -h, --help            show this help message and exit
  -o, --option {waf,port,subdo,scan_dir} [{waf,port,subdo,scan_dir} ...]
                        Choose one scan option, eg:
  -u, --url URL         url target
  -a, --user-agent USER_AGENT
                        custom user-agent in scan dir, cms detection, technology detection
  -t, --tor             scanning with tor network to hide ur ass
  -p, --proxy PROXY     set a custom proxy, e.g., http://proxyserver:port or socks5://proxyserver:port
```

## last update:
so far no errors, testing on arch linux 6.12.9-arch1-1

## About:
simple recon tool to help you searching vulnerability on web server. maybe xD

## Features:
1. Auto scan WAF
2. Auto scan port
3. Auto scan subdomain
4. Auto scan dir on web server
5. wordpress plugin enumeration
6. Auto detect cms (wordpress, joomla. drupal, moodle)
7. Auto detect technology (like the server are use, framework, javascript framework, etc. thanks to builtwith librarry :) )

## Tested on:
- Othros linux
- Kali Linux
- Debian Linux
- Parrot Linux
- Arch Linux

## tools that must be installed:
well this tool have function to auto install if some tools is not installed, so just run it with sudo if u using debian based
```
nmap
wafw00f
sublist3r
subfinder
assetfinder
dirsearch
httprobe
```

## How to install:
```
pip3 install -r requirements.txt
```

## How to use:
```
python3 sicon.py -u <target>
```

## screenshoot
![image](https://github.com/user-attachments/assets/6fac3792-c545-43a0-b9e6-bec3764ccdb3)
![250119_14h23m02s_screenshot](https://github.com/user-attachments/assets/68dee4a0-c975-40e9-be92-df427d0a830a)
![250119_14h58m32s_screenshot](https://github.com/user-attachments/assets/9dd2bd64-0f90-401e-bf43-06bc0f1e5f94)
![250119_14h59m52s_screenshot](https://github.com/user-attachments/assets/c59430d5-c6f5-41fc-a36e-f5d64dbdd3e4)
![250119_14h59m19s_screenshot](https://github.com/user-attachments/assets/9842c9da-ad7a-4dcb-bc18-9d9819a5b71f)
![250119_14h59m04s_screenshot](https://github.com/user-attachments/assets/9ffab5a1-2864-46af-b45b-850c1d1dec7a)




## next features
# general
- [ ] make installer for all distro, so every distro can run
# GUI
- [x] subdomain scanner
- [x] direcrory scanner
- [x] wafscan
- [x] portscan
- [x] save output scan
- [x] cms scanner
# CLI
- [ ] wordpress user enumeration
- [ ] report scan in html or json output
- [x] option to use proxy
- [x] user agent customization (random & user can choose)
- [x] custom scan option
# need improvemenr
- [ ] detection wordpress (its suck)
