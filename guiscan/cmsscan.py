from PyQt5.QtCore import QObject, pyqtSignal
import requests
import re
import random
import os
from pathlib import Path

class CMSScanner(QObject):
    update_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        # Regular Expressions for CMS detection
        self.cms_patterns = {
            'WordPress': re.compile(r'(?:<meta name="generator" content="WordPress|/wp-content/)'),
            'Joomla': re.compile(r'(?:<meta name="generator" content="Joomla|/media/system/js/)'),
            'Drupal': re.compile(r'(?:<meta name="generator" content="Drupal|/sites/all/)'),
            'Moodle': re.compile(r'(?:<meta name="keywords" content="moodle|/core/)')
        }
        
    def load_user_agents(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                user_agents = [line.strip() for line in file.readlines() if line.strip()]
            return user_agents
        except FileNotFoundError:
            self.error_signal.emit(f"File {file_path} not found.")
            return []

    def cms_scanning(self, target):
        """Scan subdomains for CMS detection"""
        try:
            # Load user agents
            user_agents_file_path = "core/user_agents.txt"
            user_agents = self.load_user_agents(user_agents_file_path)
            
            if not user_agents:
                self.error_signal.emit("No User-Agent data available.")
                return

            # Create report directory if it doesn't exist
            Path(f"report_{target}").mkdir(parents=True, exist_ok=True)

            # Read subdomains from file
            try:
                with open(f"report_{target}/subdomain.txt", 'r', encoding='utf-8') as r:
                    subdomains = [line.strip() for line in r.readlines() if line.strip()]
            except FileNotFoundError:
                self.error_signal.emit(f"Subdomain file not found. Please run subdomain scan first.")
                return

            # Initialize CMS-specific files
            cms_files = {
                'WordPress': open(f"report_{target}/wp.txt", "w"),
                'Joomla': open(f"report_{target}/joomla.txt", "w"),
                'Drupal': open(f"report_{target}/drupal.txt", "w"),
                'Moodle': open(f"report_{target}/moodle.txt", "w")
            }

            # Scan each subdomain
            for url in subdomains:
                if not url:
                    continue

                headers = {
                    "User-Agent": random.choice(user_agents)
                }

                try:
                    # Try both HTTPS and HTTP
                    for protocol in ['https://', 'http://']:
                        try:
                            full_url = f"{protocol}{url}"
                            response = requests.get(full_url, headers=headers, timeout=10, verify=False)
                            
                            if response.status_code == 200:
                                text = response.text
                                cms_detected = False
                                
                                # Check for each CMS
                                for cms_name, pattern in self.cms_patterns.items():
                                    if pattern.search(text):
                                        cms_files[cms_name].write(full_url + "\n")
                                        self.update_signal.emit({
                                            "URL": url,
                                            "CMS": cms_name,
                                            "Status": "Found"
                                        })
                                        cms_detected = True
                                        break
                                
                                if not cms_detected:
                                    self.update_signal.emit({
                                        "URL": url,
                                        "CMS": "Unknown",
                                        "Status": "No CMS detected"
                                    })
                                break  # Break if successful with either protocol
                                
                        except requests.RequestException:
                            continue  # Try next protocol if one fails
                            
                except Exception as e:
                    self.update_signal.emit({
                        "URL": url,
                        "CMS": "Error",
                        "Status": f"Error: {str(e)}"
                    })

            # Close all CMS files
            for f in cms_files.values():
                f.close()
                
        except Exception as e:
            self.error_signal.emit(f"Unexpected error: {str(e)}")
