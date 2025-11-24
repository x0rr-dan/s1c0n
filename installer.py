#!/usr/bin/python3
import platform
import subprocess
from os import path, getuid

def banner():
    print("""
             _       ___        
         ___/ | ___ / _ \\ _ __  
        / __| |/ __| | | | '_ \\ 
        \\__ \\ | (__| |_| | | | |
        |___/_|\\___|\\___/|_| |_|
     ===============================
     [+]        Installer        [+]             
     ===============================                   
    """)

def check_package_debian(package):
    home_user = get_home()
    try:
        result = subprocess.run(["dpkg", "-l", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if package in result.stdout:
            return True
        
        paths = [f"/usr/bin/{package}", f"/usr/local/bin/{package}", f"{home_user}/go/bin/{package}"]
        for pathpler in paths:
            if path.exists(pathpler):
                return True
        
        return False
    except FileNotFoundError:
        return False


def check_package_arch(package):
    try:
        result = subprocess.run(["pacman", "-Q", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True
        
        paths = [f"/usr/bin/{package}", f"/usr/local/bin/{package}", f"{get_home()}/go/bin/{package}"]
        for pathpler in paths:
            if path.exists(pathpler):
                return True
        
        return False
    except FileNotFoundError:
        return False


def detect_distro():
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"')
    except Exception:
        return None

def get_home():
    home = path.expanduser("~")
    return home

def installtool(package, distro):
    print(f"[+] Installing {package} ..")
    home_user = get_home()
    if distro in ["debian", "ubuntu"]:
        if package == "subfinder":
            if not check_package_debian("golang"):
                print("[!] Golang not found, installing golang first ..")
                subprocess.run(["apt", "install", "-y", "golang"])
            subprocess.run(["go", "install", "-v", "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"], shell=True)
            subprocess.run(["chmod", "+x", f"{home_user}/go/bin/{package}"])
            subprocess.run(["mv", f"{home_user}/go/bin/{package}", "/usr/bin/"])
        elif package == "assetfinder":
            if not check_package_debian("golang"):
                print("[!] Golang not found, installing golang first ..")
                subprocess.run(["apt", "install", "-y", "golang"])
            subprocess.run(["go", "install", "-v", "github.com/tomnomnom/assetfinder@latest"], shell=True)
            subprocess.run(["chmod", "+x", f"{home_user}/go/bin/{package}"])
            subprocess.run(["mv", f"{home_user}/go/bin/{package}", "/usr/bin/"])
        else:
            subprocess.run(["apt", "install", "-y", package])
    elif distro in ["kali", "parrot"]:
        subprocess.run(["apt", "install", "-y", package])
    elif distro in ["arch"]:
        if package == "wafw00f" or package == "dirsearch":
            subprocess.run(["yay", "-S", "--noconfirm", package])
        elif package == "sublist3r":
            subprocess.run(["yay", "-S", "--noconfirm", "sublist3r-git"])
        elif package == "assetfinder":
            subprocess.run(["yay", "-S", "--noconfirm", "assetfinder-git"])
        else:
            subprocess.run(["pacman", "-S", "--noconfirm", package])

    
def installs1c0n():
    print(f"[+] Installing s1c0n to your system ..")
    install_dir = "/opt/s1c0n"
    if not path.exists(install_dir):
        subprocess.run(["git", "clone", "https://github.com/x0rr-dan/s1c0n.git", install_dir], check=True)
    else:
        print("[*] s1c0n was cloning before")

    print("[+] Installing python librarry ..")
    subprocess.run(["pip3", "install", "-r", path.join(install_dir, "requirements.txt"), "--break-system-packages"], check=True)
    desktop_file = path.join(install_dir, "s1c0n-cli.desktop")
    desktop_file2 = path.join(install_dir, "s1c0n-gui.desktop")
    if path.exists(desktop_file):
        subprocess.run(["cp", desktop_file, desktop_file2, "/usr/share/applications/"], check=True)
        subprocess.run(["chmod", "777", install_dir])
        subprocess.run(["chmod", "+x", f"{install_dir}/sicon.py", f"{install_dir}/sicon-gui.py", f"{install_dir}/sicon", f"{install_dir}/exec-in-shell"])
        subprocess.run(["cp", f"{install_dir}/sicon", f"{install_dir}/exec-in-shell", "/usr/bin"])


    print("[+] s1c0n was successfully installed ..")



def main():
    banner()
    user = getuid()
    if user == 0:
        packages = {
            "nmap": "all",
            "wafw00f": "all",
            "sublist3r": "all",
            "subfinder": "kali_parrot_arch",
            "assetfinder": "kali_parrot_arch",
            "dirsearch": "all",
        }
        distro = detect_distro()

        if distro in ["kali", "parrot"]:
            check_package = check_package_debian
        elif distro in ["debian", "ubuntu"]:
            check_package = check_package_debian
        elif distro in ["arch"]:
            check_package = check_package_arch
        else:
            print("Unsupported distribution detected.")
            return
        
        print(f"[+] {distro} detected ..")
        print(f"[*] Checking installed packages:")
        for package, supported in packages.items():
            if supported == "all" or distro in supported.split("_"):
                if check_package(package):
                    print(f"[+] {package} installed ..")
                else:
                    print(f"[-] {package} not installed ..")
                    installtool(package, distro)

        installs1c0n()
    else:
        print("[-] must run with sudo privileges")

if __name__ == "__main__":
    main()
