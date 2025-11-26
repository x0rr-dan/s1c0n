from core.color import Color
from core.random_ag import rangent
from scan.bhttprobe import better_httprobe
import requests, builtwith, subprocess
from requests.exceptions import Timeout, RequestException

def more_info(target, user_agent=None, proxy=None):
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        with open(f"report_{target}/subdomain.txt", 'r', encoding='utf-8') as r:
            read_subdo = r.readlines()

        print(f"{Color.bold}{Color.green}\n\t  [+] WEB TECHNOLOGY: {len(read_subdo)} sites{Color.reset}")

        output_file_path = f"report_{target}/subdomain_with_tech.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for url in read_subdo:
                url_mentah = url.strip()
                # print(f"{url_mentah}") #debug
                url = better_httprobe(url_mentah)
                technologies_str = ""

                try:
                    if user_agent:
                        headers = {"User-Agent": user_agent}
                    else:
                        headers = {"User-Agent": rangent()}
                    # Permintaan HTTP dengan User-Agent kustom
                    r = requests.get(url, headers=headers, timeout=20, proxies=proxies)
                    if r.status_code == 200:
                        data = builtwith.builtwith(url)
                        keys_of_interest = ['programming-language', 'cms', 'web-servers', 'javascript-frameworks',
                                            'web-frameworks']
                        technologies = [tech for key in keys_of_interest if key in data for tech in data[key]]
                        technologies_str = " | ".join(
                            technologies) if technologies else f"{Color.red}No technology detected{Color.reset}"

                        if 'XSRF-TOKEN' in r.cookies or 'laravel_session' in r.cookies:
                            technologies_str += " | Laravel"
                    else:
                        technologies_str = f"{Color.red}Error code: {r.status_code}{Color.reset}"

                except Timeout:
                    technologies_str = f"{Color.red}Timeout{Color.reset}"
                except ConnectionError as e:
                    technologies_str = f"{Color.red}Network error: {str(e)}{Color.reset}"
                except RequestException as e:
                    technologies_str = f"{Color.red}Host Offline{Color.reset}"

                print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} {Color.reset}| {Color.bold}{Color.green}[ {technologies_str}{Color.green} ]{Color.reset}")

                # Write to file
                output_file.write(f"{url} | {technologies_str}\n")

    except FileNotFoundError:
        print(f"{Color.red}File report_{target}/subdomain.txt not found.{Color.reset}")
    except KeyboardInterrupt:
        print(f"{Color.bold}[!] Keyboard Interrupt\n[!] Exit ... {Color.reset}")
