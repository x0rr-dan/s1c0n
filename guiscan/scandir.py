from os import getcwd, system, path
import json
from core.utility import clean
from PyQt5.QtCore import QObject, pyqtSignal

class DirectoryScanner(QObject):
    # Sinyal untuk mengirim data hasil scan ke GUI
    update_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def scan_dir(self, target):
        """Scan directories and emit results to GUI."""
        try:
            p = f"{getcwd()}/"
            # Menjalankan dirsearch dan menyimpan hasil dalam file JSON
            system(f"dirsearch -u {target} -o {p}.list_dir.json --format=json > /dev/null")

            # Memeriksa apakah file hasil scan ada
            if path.exists(f"{p}/.list_dir.json"):
                with open(".list_dir.json", encoding="utf-8") as dir_file:
                    jdir = json.load(dir_file)
                    if jdir:
                        # Membersihkan file JSON setelah diproses
                        clean("json")
                        dir_found = jdir["results"]
                        list_dir_found = []
                        
                        for d in dir_found:
                            p_dir = d["url"]
                            status_dir = d["status"]
                            if status_dir in [200, 403, 500, 404,502]:
                                list_dir_found.append({
                                    "Status": status_dir,
                                    "Directory": p_dir
                                })

                        sorted_dir = sorted(list_dir_found, key=lambda x: x["Status"])

                        # Mengirimkan hasil melalui sinyal ke GUI
                        for d in sorted_dir:
                            self.update_signal.emit(d)
                    else:
                        self.error_signal.emit("Directory scanner tidak menemukan hasil yang berguna bjir.")
            else:
                self.error_signal.emit("Kesalahan saat menjalankan dirsearch untuk scanner direktori hehe.")
        except Exception as e:
            self.error_signal.emit(str(e))
