from PyQt5.QtCore import QObject, pyqtSignal
import requests
import builtwith
import random
import os

class TechnologyScanner(QObject):
    # Define signals for GUI updates
    update_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
    def load_user_agents(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                user_agents = [line.strip() for line in file.readlines() if line.strip()]
            return user_agents
        except FileNotFoundError:
            self.error_signal.emit(f"File {file_path} not found.")
            return []

    def tech_scanning(self, target):
        # Load user agents
        user_agents_file_path = "core/user_agents.txt"
        user_agents = self.load_user_agents(user_agents_file_path)
        
        if not user_agents:
            self.error_signal.emit("No User-Agent data available.")
            return

        try:
            # Read subdomains from file
            with open(f"report_{target}/subdomain.txt", 'r', encoding='utf-8') as r:
                subdomains = r.readlines()

            # Process each subdomain
            for url in subdomains:
                url = f"https://{url.strip()}"
                try:
                    # Random user agent
                    user_agent = random.choice(user_agents)
                    headers = {"User-Agent": user_agent}
                    
                    # Make HTTP request
                    r = requests.get(url, headers=headers, timeout=10)
                    
                    if r.status_code == 200:
                        # Get technology data
                        data = builtwith.builtwith(url)
                        keys_of_interest = [
                            'programming-language', 
                            'cms', 
                            'web-servers', 
                            'javascript-frameworks',
                            'web-frameworks'
                        ]
                        
                        technologies = [
                            tech for key in keys_of_interest 
                            if key in data 
                            for tech in data[key]
                        ]
                        
                        # Check for Laravel
                        if 'XSRF-TOKEN' in r.cookies or 'laravel_session' in r.cookies:
                            technologies.append('Laravel')
                            
                        tech_str = " | ".join(technologies) if technologies else "No technology detected"
                        
                        # Emit result to GUI
                        self.update_signal.emit({
                            "URL": url,
                            "Technologies": tech_str,
                            "Status": "Success"
                        })
                    else:
                        self.update_signal.emit({
                            "URL": url,
                            "Technologies": f"Error code: {r.status_code}",
                            "Status": "Error"
                        })
                        
                except requests.Timeout:
                    self.update_signal.emit({
                        "URL": url,
                        "Technologies": "Timeout",
                        "Status": "Error"
                    })
                except requests.RequestException as e:
                    self.update_signal.emit({
                        "URL": url,
                        "Technologies": f"Failed to retrieve data ({str(e)})",
                        "Status": "Error"
                    })
                    
        except FileNotFoundError:
            self.error_signal.emit(f"File report_{target}/subdomain.txt not found.")
        except Exception as e:
            self.error_signal.emit(f"Unexpected error: {str(e)}")
