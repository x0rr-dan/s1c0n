import subprocess
import re

def waf_scanning(target):
    """Scan the target for Web Application Firewall (WAF) and return results in a structured format."""
    try:
        # Resolve the target using httprobe
        host = subprocess.check_output(f"echo {target} | httprobe -prefer-https", shell=True, text=True).strip()

        # Run wafw00f against the target
        waf_output = subprocess.check_output(f"wafw00f {host}", shell=True, text=True)

        # Check if a WAF is detected
        if "is behind" in waf_output:
            match = re.search(r'is behind\s(.+?)\s\(', waf_output)
            wafname = match.group(1).strip() if match else "Unknown WAF"
            result = {
                "Target": target,
                "Status": "Detected",
                "WAF Name": wafname
            }
        else:
            result = {
                "Target": target,
                "Status": "Not Detected",
                "WAF Name": "N/A"
            }

        return [result]

    except subprocess.CalledProcessError as e:
        return [{"Target": target, "Status": "Error", "WAF Name": str(e)}]

    except Exception as e:
        return [{"Target": target, "Status": "Error", "WAF Name": f"Unexpected error: {str(e)}"}]
