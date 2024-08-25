## s1c0n
![Python](https://img.shields.io/badge/Python-3.9.2-blue)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

![Terkey](https://github-readme-stats.vercel.app/api/pin?username=x0rr-dan&repo=s1c0n&title_color=fff&icon_color=fff&text_color=ffffff&bg_color=000000)

```


	         ┏━┓╺┓ ┏━╸┏━┓┏┓╻
	         ┗━┓ ┃ ┃  ┃┃┃┃┗┫
	         ┗━┛╺┻╸┗━╸┗━┛╹ ╹ v1.7
                
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
5. Auto detect cms (only wordpress and joomla, i will add another cms if i have time to update this tool :) )
6. Auto detect technology (like the server are use, framework, javascript framework, etc. thanks to builtwith librarry :) )

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

![fakme](https://user-images.githubusercontent.com/51450260/162648377-f453e31b-e75d-43af-96f7-5b8c4a5afb27.png)

![Screenshot from 2024-07-14 21-27-04](https://github.com/user-attachments/assets/4c15a5a6-d34f-4ce8-9ce8-16c09e5783a5)


## note
So far I have tried to eliminate the error output from the webserver which is offline when detecting the technology used, the error comes from the builtwith library which requires urllib, and I don't know how to eliminate the error, if you find a way please pull request to contribute :)
