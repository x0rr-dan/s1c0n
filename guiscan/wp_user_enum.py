from PyQt5.QtCore import QObject, pyqtSignal
import requests
import re
import random
import os

class WPUserEnumScanner(QObject):
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
            return []

    def check_rest_api(self, url, headers):
        users = []
        try:
            api_url = f"{url}/wp-json/wp/v2/users"
            response = requests.get(api_url, headers=headers, timeout=15, verify=False)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    for user in data:
                        if 'slug' in user:
                            users.append(user['slug'])
                            self.update_signal.emit({
                                "URL": url,
                                "Username": user['slug'],
                                "Method": "REST API",
                                "Status": "Found"
                            })
        except Exception:
            pass
        return users

    def check_author_archives(self, url, headers):
        users = []
        try:
            for i in range(1, 11):
                author_url = f"{url}/?author={i}"
                response = requests.get(author_url, headers=headers, timeout=10, allow_redirects=False, verify=False)
                
                if response.status_code in [301, 302]:
                    location = response.headers.get('Location', '')
                    if '/author/' in location:
                        match = re.search(r'/author/([^/]+)/?', location)
                        if match:
                            user = match.group(1)
                            users.append(user)
                            self.update_signal.emit({
                                "URL": url,
                                "Username": user,
                                "Method": f"Author Archive (ID {i})",
                                "Status": "Found"
                            })
                elif response.status_code == 200:
                    if f"author-{i}" in response.text or 'body class="archive author' in response.text:
                        match = re.search(r'/author/([^/"\']+)/?', response.text)
                        if match:
                            user = match.group(1)
                            users.append(user)
                            self.update_signal.emit({
                                "URL": url,
                                "Username": user,
                                "Method": f"Author Archive Page (ID {i})",
                                "Status": "Found"
                            })
        except Exception:
            pass
        return users

    def check_page_source(self, url, headers):
        users = []
        try:
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            if response.status_code == 200:
                matches = re.findall(r'/author/([^/"\']+)/?', response.text)
                for user in matches:
                    if user not in users:
                        users.append(user)
                        self.update_signal.emit({
                            "URL": url,
                            "Username": user,
                            "Method": "Page Source",
                            "Status": "Found"
                        })
        except Exception:
            pass
        return users

    def check_login_errors(self, url, headers, usernames):
        valid_users = []
        if not usernames:
            usernames = ['admin', 'administrator', 'root', 'user']
            
        login_url = f"{url}/wp-login.php"
        try:
            res = requests.get(login_url, headers=headers, timeout=10, verify=False)
            if res.status_code != 200 or 'log' not in res.text:
                return valid_users

            for user in usernames:
                data = {
                    'log': user,
                    'pwd': 'S1C0N_FAKE_PASSWORD_123!@#',
                    'wp-submit': 'Log In'
                }
                response = requests.post(login_url, data=data, headers=headers, timeout=10, verify=False)
                
                if "The password you entered for the username" in response.text or "Error: The password you entered" in response.text or "is incorrect" in response.text:
                    valid_users.append(user)
                    self.update_signal.emit({
                        "URL": url,
                        "Username": user,
                        "Method": "Login Error Verify",
                        "Status": "Confirmed"
                    })
        except Exception:
            pass
        return valid_users

    def wp_user_enum_scanning(self, target):
        try:
            user_agents = self.load_user_agents("core/user_agents.txt")
            if not user_agents:
                user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]

            try:
                with open(f"report_{target}/wp.txt", 'r', encoding='utf-8') as r:
                    wp_sites = [line.strip() for line in r.readlines() if line.strip()]
            except FileNotFoundError:
                self.error_signal.emit("WP file not found. Please run CMS scan first to detect WordPress sites.")
                return

            if not wp_sites:
                self.update_signal.emit({
                    "URL": "-",
                    "Username": "-",
                    "Method": "-",
                    "Status": "No WP sites found"
                })
                return

            any_user_found = False

            for url in wp_sites:
                headers = {"User-Agent": random.choice(user_agents)}
                site_users = []
                
                # Check 1: REST API
                site_users.extend(self.check_rest_api(url, headers))
                # Check 2: Author Archives
                site_users.extend(self.check_author_archives(url, headers))
                # Check 3: Page Source
                site_users.extend(self.check_page_source(url, headers))
                
                # Deduplicate
                unique_users = list(set(site_users))
                
                # Check 4: Verify/Discover via Login Errors
                login_verified = self.check_login_errors(url, headers, unique_users)
                
                final_users = list(set(unique_users + login_verified))
                
                if final_users:
                    any_user_found = True
                    # Log them to a file just like CLI
                    with open(f"report_{target}/wp_users.txt", "a") as f:
                        for u in final_users:
                            f.write(f"{url} | {u}\n")

            if not any_user_found:
                 self.update_signal.emit({
                    "URL": target,
                    "Username": "None",
                    "Method": "All",
                    "Status": "No users found"
                })

        except Exception as e:
            self.error_signal.emit(f"Unexpected error: {str(e)}")
