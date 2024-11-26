from PyQt5.QtCore import QObject, pyqtSignal
from core.color import Color
from core.distro import distro
from os import path, system
from core.utility import clean
from core.utility import create_report_folder
import subprocess

class SubdomainScanner(QObject):
    update_signal = pyqtSignal(dict)  # Sinyal untuk kirim data  subdomain, type, and ports
    error_signal = pyqtSignal(str)   # Sinyal untuk kirim error messages

    def __init__(self):
        super().__init__()

    def subdo_scanning(self, target):
        try:
            # cek installasi nmap
            try:
                import nmap
            except ImportError as error:
                self.error_signal.emit(f"Error importing nmap: {error}")
                dis = distro()
                if dis == 'arch':
                    system("yay -S python-nmap --noconfirm")
                else:
                    system("pip3 install python-nmap")
                return
            
            
            report_dir = f"{target}"
            create_report_folder(report_dir)

            
            port_scan = nmap.PortScanner()

            # Run subfinder
            subprocess.run(
                ["subfinder", "-d", f"{target}", "-o", ".list_subfinder.txt", "-silent"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

            # Run sublist3r
            subprocess.run(
                ["sublist3r", "-d", f"{target}", "-o", ".list_sublist3r.txt"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

            # Run assetfinder
            subprocess.run(
                ["assetfinder", target],
                stdout=open('.list_assetfinder.txt', 'w'), stderr=subprocess.DEVNULL
            )

            # Gabungan hasil
            system("cat .list*.txt > .list_subdo.txt")

            with open(".list_subdo.txt", encoding="utf-8") as subdo_file:
                subdo_list = subdo_file.read().splitlines()

            # Remove duplicates
            subdoo_list = set(subdo_list)

            # cPanel and non-cPanel domains
            cpanel_subdo = [
                sub for sub in subdoo_list if sub.startswith(
                    ("cpanel.", "webdisk.", "webmail.", "cpcontacts.", "whm.", "autoconfig.", "mail.", "cpcalendars.", "autodiscover.")
                )
            ]
            not_cpanel_subdo = [
                sub for sub in subdoo_list if not sub.startswith(
                    ("cpanel.", "webdisk.", "webmail.", "cpcontacts.", "whm.", "autoconfig.", "mail.", "cpcalendars.", "autodiscover.")
                )
            ]

            
            with open(path.join(f"report_{report_dir}", "cpanel_subdomain.txt"), "w") as f:
                f.write("\n".join(cpanel_subdo))

            with open(path.join(f"report_{report_dir}", "subdomain.txt"), "w") as f:
                if not_cpanel_subdo:
                    f.write("\n".join(not_cpanel_subdo))
                else:
                    f.write("")

            # Cleanup
            clean("txt")

            # Process setiap hasil subdomain dan kirim data to GUI
            for subdomain in subdoo_list:
                domain_type = "cPanel" if subdomain in cpanel_subdo else "Non-cPanel"

                # Run nmap quick port scan
                qscan = port_scan.scan(hosts=subdomain, arguments="-F")
                open_ports = []

                if "scan" in qscan:
                    h = list(qscan["scan"].keys())
                    if len(h) > 0 and "tcp" in qscan["scan"][h[0]]:
                        open_ports = list(qscan["scan"][h[0]]["tcp"].keys())

                # data yang akan dikirim ke GUI
                data = {
                    "Subdomain": subdomain,
                    "Type": domain_type,
                    "Ports": ", ".join(map(str, open_ports)) if open_ports else "No Open Ports",
                }

                # Emit data
                self.update_signal.emit(data)

        except Exception as e:
            # Emit error signal
            self.error_signal.emit(str(e))
