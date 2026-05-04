from core.color import Color
from core.random_ag import rangent
from os import path
import requests
import re
import time

def check_rest_api(url, headers, proxy_dict):
    """Method 1: Query REST API for users"""
    users = []
    try:
        api_url = f"{url}/wp-json/wp/v2/users"
        response = requests.get(api_url, headers=headers, proxies=proxy_dict, timeout=15, verify=False)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                for user in data:
                    if 'slug' in user:
                        users.append(user['slug'])
                        print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | User found via REST API: {Color.green}{user['slug']}{Color.reset}")
    except Exception as e:
        pass
    return users

def check_author_archives(url, headers, proxy_dict):
    """Method 2: Iterate author IDs to find redirects"""
    users = []
    try:
        for i in range(1, 11): # Cap at 10 to avoid excessive noise
            author_url = f"{url}/?author={i}"
            # Don't allow redirect automatically to catch the Location header
            response = requests.get(author_url, headers=headers, proxies=proxy_dict, timeout=10, allow_redirects=False, verify=False)
            
            if response.status_code in [301, 302]:
                location = response.headers.get('Location', '')
                if '/author/' in location:
                    match = re.search(r'/author/([^/]+)/?', location)
                    if match:
                        user = match.group(1)
                        users.append(user)
                        print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | User found via Author Archive (ID {i}): {Color.green}{user}{Color.reset}")
            elif response.status_code == 200:
                # Sometimes it doesn't redirect but loads the author page directly
                if f"author-{i}" in response.text or 'body class="archive author' in response.text:
                    # Try to extract from page source
                    match = re.search(r'/author/([^/"\']+)/?', response.text)
                    if match:
                        user = match.group(1)
                        users.append(user)
                        print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | User found via Author Archive page (ID {i}): {Color.green}{user}{Color.reset}")
    except Exception as e:
        pass
    return users

def check_page_source(url, headers, proxy_dict):
    """Method 3: Scrape homepage for author links"""
    users = []
    try:
        response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=15, verify=False)
        if response.status_code == 200:
            matches = re.findall(r'/author/([^/"\']+)/?', response.text)
            for user in matches:
                if user not in users:
                    users.append(user)
                    print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | User found in Page Source: {Color.green}{user}{Color.reset}")
    except Exception as e:
        pass
    return users

def check_login_errors(url, headers, proxy_dict, usernames):
    """Method 4: Differential error messages on login form"""
    valid_users = []
    if not usernames:
        usernames = ['admin', 'administrator', 'root', 'user'] # Fallback
        
    login_url = f"{url}/wp-login.php"
    try:
        # First check if wp-login.php exists
        res = requests.get(login_url, headers=headers, proxies=proxy_dict, timeout=10, verify=False)
        if res.status_code != 200 or 'log' not in res.text:
            return valid_users

        for user in usernames:
            data = {
                'log': user,
                'pwd': 'S1C0N_FAKE_PASSWORD_123!@#',
                'wp-submit': 'Log In'
            }
            response = requests.post(login_url, data=data, headers=headers, proxies=proxy_dict, timeout=10, verify=False)
            
            # Differential check
            # "Unknown username" or "Invalid username" vs "password you entered for the username"
            if "The password you entered for the username" in response.text or "Error: The password you entered" in response.text or "is incorrect" in response.text:
                valid_users.append(user)
                print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | User verified via Login Error: {Color.green}{user}{Color.reset}")
    except Exception as e:
        pass
    return valid_users

def wp_user_enum(target, user_agent=None, proxy=None):
    he = rangent()
    if not user_agent:
        user_agent = he
    
    headers = {"User-Agent": user_agent}
    proxy_dict = {"http": proxy, "https": proxy} if proxy else None
    
    if path.exists(f"report_{target}/wp.txt"):
        with open(f"report_{target}/wp.txt", 'r', encoding='utf-8') as r:
            wp_sites = [line.strip() for line in r.readlines() if line.strip()]
            
        if not wp_sites:
            return

        print(f"{Color.bold}{Color.green}\n\t  [+] WORDPRESS USER ENUMERATION: {len(wp_sites)} sites{Color.reset}")
        
        all_found_users = []
        for url in wp_sites:
            site_users = []
            
            # Run checks sequentially
            site_users.extend(check_rest_api(url, headers, proxy_dict))
            site_users.extend(check_author_archives(url, headers, proxy_dict))
            site_users.extend(check_page_source(url, headers, proxy_dict))
            
            # Deduplicate users found so far
            unique_users = list(set(site_users))
            
            # Verify/discover via login form
            # login_verified = check_login_errors(url, headers, proxy_dict, unique_users)
            
            # Merge and dedup again
            # final_users = list(set(unique_users + login_verified))
            final_users = list(set(unique_users))
            
            if not final_users:
                 print(f"{Color.green}\t    -> {Color.reset}{Color.bold}{url} | {Color.red}No users found{Color.reset}")
            else:
                for u in final_users:
                    all_found_users.append(f"{url} | {u}")

            time.sleep(2)
            
        if all_found_users:
            with open(path.join(f"report_{target}", "wp_users.txt"), "a") as f:
                for line in all_found_users:
                    f.write(f"{line}\n")
    else:
        pass
