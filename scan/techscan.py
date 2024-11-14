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
                technologies_str = ""  # Initialize the variable at the start of each loop

                try:
                    # detected technology target using builtwith
                    try:
                        r = requests.get(url, timeout=10)
                        if r.status_code == 200:
                            data = builtwith.builtwith(url)
                            keys_of_interest = ['programming-language', 'cms', 'web-servers', 'javascript-frameworks', 'web-frameworks']
                            technologies = []
                            for key in keys_of_interest:
                                if key in data:
                                    technologies.extend(data[key])
                            technologies_str = " | ".join(technologies) if technologies else f"{Color.red}No technology detected{Color.reset}"
                        else:
                            technologies_str += f"{Color.red}Error code: {r.status_code}{Color.reset}"
                    except Timeout:
                        pass
                    except RequestException:
                        pass

                    try:
                        response = requests.get(url, timeout=10)  # Timeout 10 sec
                        cookies = response.cookies
                        if 'XSRF-TOKEN' in cookies or 'laravel_session' in cookies:
                            technologies_str += " | Laravel"
                    except Timeout:
                        technologies_str += f" | {Color.red}Timeout{Color.reset}"
                    except RequestException:
                        technologies_str += f" | {Color.red}Failed to retrieve data{Color.reset}"

                    # Print to console
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} {Color.reset}| {Color.bold}{Color.green}[ {technologies_str}{Color.green} ]{Color.reset}")
                    
                    # Write to file
                    output_file.write(f"{url} | {technologies_str}\n")

                except KeyboardInterrupt:
                    print(f"{Color.bold}[!] Keyboard Interupt\n[!] Exit ... {Color.reset}")
                    return  # Exit the function on keyboard interrupt

    except FileNotFoundError:
        print(f"{Color.red}File report_{target}/subdomain.txt not found.{Color.reset}")
