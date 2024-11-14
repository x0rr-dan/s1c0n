from core.color import Color
import requests
import builtwith
from requests.exceptions import Timeout, RequestException

def more_info(target):
    try:
        with open(f"report_{target}/subdomain.txt", 'r', encoding='utf-8') as r:
            read_subdo = r.readlines()

        print(f"{Color.bold}{Color.green}\n\t  [+] WEB TECHNOLOGY: {len(read_subdo)} sites{Color.reset}")

        output_file_path = f"report_{target}/subdomain_with_tech.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for url in read_subdo:
                url = f"https://{url.strip()}"
                technologies_str = ""

                try:
                    r = requests.get(url, timeout=10)
                    if r.status_code == 200:
                        data = builtwith.builtwith(url)
                        keys_of_interest = ['programming-language', 'cms', 'web-servers', 'javascript-frameworks', 'web-frameworks']
                        technologies = [tech for key in keys_of_interest if key in data for tech in data[key]]
                        technologies_str = " | ".join(technologies) if technologies else f"{Color.red}No technology detected{Color.reset}"

                        if 'XSRF-TOKEN' in r.cookies or 'laravel_session' in r.cookies:
                            technologies_str += " | Laravel"
                    else:
                        technologies_str = f"{Color.red}Error code: {r.status_code}{Color.reset}"

                except Timeout:
                    technologies_str = f"{Color.red}Timeout{Color.reset}"
                except RequestException:
                    technologies_str = f"{Color.red}Failed to retrieve data{Color.reset}"

                print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} {Color.reset}| {Color.bold}{Color.green}[ {technologies_str}{Color.green} ]{Color.reset}")
                output_file.write(f"{url} | {technologies_str}\n")

    except FileNotFoundError:
        print(f"{Color.red}File report_{target}/subdomain.txt not found.{Color.reset}")
    except KeyboardInterrupt:
        print(f"{Color.bold}[!] Keyboard Interupt\n[!] Exit ... {Color.reset}")
