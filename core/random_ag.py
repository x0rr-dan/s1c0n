from core.color import Color
import random
from os import path

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

def rangent(): 
    USER_AGENTS_FILE = path.join(path.dirname(__file__), "user_agents.txt")
    USER_AGENTS = load_user_agents(USER_AGENTS_FILE)
    if not USER_AGENTS:
        print(f"{Color.red}No User-Agent data available. Exiting...{Color.reset}")
        exit()
    random_agent = random.choice(USER_AGENTS)
    return random_agent