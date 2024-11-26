import subprocess
import os
import re
from core.utility import clean  

def port_scanning(target):
    """Scan the target for open ports and return results in a structured format."""
    try:
        # Buat direktori sementara untuk output
        output_dir = "temp_output"
        os.makedirs(output_dir, exist_ok=True)  # Buat direktori jika belum ada
        nmap_output_file = os.path.join(output_dir, ".list_nmap.txt")

        # Jalankan perintah nmap
        command = f"nmap -sV {target} -oN {nmap_output_file}"
        subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Parsing hasil
        with open(nmap_output_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        results = []
        parsing = False
        for line in lines:
            if line.strip().startswith("PORT"):
                parsing = True
                continue

            if parsing:
                match = re.match(r"(\d+/[a-z]+)\s+(\w+)\s+(.+)", line.strip())
                if match:
                    port = match.group(1)
                    state = match.group(2)
                    service = match.group(3)
                    results.append({"Port": port, "State": state, "Service": service})

        
        if os.path.exists(nmap_output_file):
            os.remove(nmap_output_file)

        return results

    except subprocess.CalledProcessError as e:
        return [{"Port": "N/A", "State": "Error", "Service": f"Nmap error: {e.stderr.strip()}"}]
    except Exception as e:
        return [{"Port": "N/A", "State": "Error", "Service": f"Unexpected error: {str(e)}"}]
