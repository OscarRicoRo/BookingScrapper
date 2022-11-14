from itertools import cycle
import requests
import pandas as pd

resp = requests.get('https://free-proxy-list.net/')
df = pd.read_html(resp.text)[0]
print(df[df.Https == 'yes'])

# Enter proxy ip's and ports in a list.
proxies = {
    'http://176.56.107.84:51528',
    'http://94.45.137.34:8080',
    'http://133.242.171.216:3128',
    'http://85.60.193.39:55443',
    'http://47.254.153.78:443'
}

proxy_pool = cycle(proxies)

# Initialize a URL.

url = 'https://httpbin.org/ip'  # Iterate through the proxies and check if it is working.
for i in range(1, 6):
    proxy = next(proxy_pool)
    print("Request #%d" % i)
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=30)
        print(response.json())
    except:
        print("Skipping. Connection error")
