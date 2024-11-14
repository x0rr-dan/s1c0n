# 1.1 checking distro, to install tools
def distro():
    try:
        ## read os-release to check the distro
        with open('/etc/os-release', 'r') as file:
             lines = file.readlines()
             for line in lines:
                  if line.startswith('ID='):
                       return line.split('=')[1].strip().strip('"')
    except FileNotFoundError:
         print("[-] /etc/os-release not found ...")
         print("[*] Your not using linux ... if u using mac or other opratation system u should install tools manually")
         pass
    return None