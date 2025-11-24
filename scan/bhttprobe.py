import requests

def better_httprobe(target):
    for protocol in ['http', 'https']:
        url = f"{protocol}://{target}"
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code < 400:
                return url
        except:
            continue
    return f"http://{target}"
