## s1c0n
![Python](https://img.shields.io/badge/Python-3.9.2-blue)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

![Terkey](https://github-readme-stats.vercel.app/api/pin?username=x0rr-dan&repo=s1c0n&title_color=fff&icon_color=fff&text_color=ffffff&bg_color=000000)

```


	         ┏━┓╺┓ ┏━╸┏━┓┏┓╻
	         ┗━┓ ┃ ┃  ┃┃┃┃┗┫
	         ┗━┛╺┻╸┗━╸┗━┛╹ ╹ v1.8
                
                    Simple Recon
		    Coded by x0r
	https://github.com/x0rr-dan/s1c0n

	  [?] Usage example: sicon -u target.com

```

## last update:
so far no errors, testing on arch linux 2024.07.01

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
![241114_22h10m05s_screenshot](https://github.com/user-attachments/assets/9ea9ed46-c513-4313-911f-be44d1a78881)
![241114_22h10m15s_screenshot](https://github.com/user-attachments/assets/b8897318-9fea-4d59-bd3f-52d9fb3158d8)
![241114_22h10m25s_screenshot](https://github.com/user-attachments/assets/b308f15f-c6e9-4597-b083-f43eba3c9e7c)


## next features
# general
- [ ] make installer for all distro, so every distro can run
# GUI
- [x] subdomain scanner
- [x] direcrory scanner
- [x] wafscan
- [x] portscan
- [x] save output scan
- [ ] cms scanner
# CLI
- [ ] wordpress user enumeration
- [ ] report scan in html or json output
- [ ] option to use proxy
- [ ] user agent customization
- [ ] custom scan option (maybe with argparse or just simple input)
# need improvemenr
- [ ] detection wordpress (its suck)
