from core.color import Color
import requests
import builtwith
import random
from requests.exceptions import Timeout, RequestException


# Fungsi untuk membaca User-Agent dari file
def load_user_agents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Membaca setiap baris dan menghapus spasi kosong
            user_agents = [line.strip() for line in file.readlines() if line.strip()]
        return user_agents
    except FileNotFoundError:
        print(f"{Color.red}File {file_path} not found.{Color.reset}")
        return []


def more_info(target):
    # Menentukan path file user_agents.txt
    user_agents_file_path = "core/user_agents.txt"


    # Memuat User-Agent dari file
    user_agents = load_user_agents(user_agents_file_path)

    if not user_agents:
        print(f"{Color.red}No User-Agent data available. Exiting...{Color.reset}")
        return

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
                    # Pilih User-Agent secara acak dari daftar yang telah dimuat
                    user_agent = random.choice(user_agents)
                    headers = {"User-Agent": user_agent}

                    # Permintaan HTTP dengan User-Agent kustom
                    r = requests.get(url, headers=headers, timeout=10)
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
                except RequestException as e:
                    technologies_str = f"{Color.red}Failed to retrieve data ({str(e)}){Color.reset}"

                # Cetak hasil ke terminal
                print(
                    f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} {Color.reset}| {Color.bold}{Color.green}[ {technologies_str}{Color.green} ]{Color.reset}")

                # Tulis hasil ke file
                output_file.write(f"{url} | {technologies_str}\n")

    except FileNotFoundError:
        print(f"{Color.red}File report_{target}/subdomain.txt not found.{Color.reset}")
    except KeyboardInterrupt:
        print(f"{Color.bold}[!] Keyboard Interrupt\n[!] Exit ... {Color.reset}")