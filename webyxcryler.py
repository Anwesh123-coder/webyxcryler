import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse

def print_banner():
    # Completely corrected banner: W E B Y X C R Y L E R
    banner = r"""
 __      __      __   ______   ____    __     __ __   __   ______  _____   __     __  _       ______  _____   
 \ \    /  \    / /  |  ____| |  _ \   \ \   / / \ \ / /  / ____/ |  __ \  \ \   / / | |     |  ____||  __ \  
  \ \  / /\ \  / /   | |__    | |_) |   \ \_/ /   \ V /  | |      | |__) |  \ \_/ /  | |     | |__   | |__) | 
   \ \/ /  \ \/ /    |  __|   |  _ <     \   /     > <   | |      |  _  /    \   /   | |     |  __|  |  _  /  
    \  /    \  /     | |____  | |_) |     | |     / . \  | |____  | | \ \     | |    | |____ | |____ | | \ \  
     \/      \/      |______| |____/      |_|    /_/ \_\  \____/  |_|  \_\    |_|    |______||______||_|  \_\ 
    """
    print(banner)
    print("=" * 110)
    print(" " * 41 + "Made by Anwesh123-coder")
    print("=" * 110 + "\n")

def get_base_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def check_robots_txt(base_url):
    print(f"[+] Checking robots.txt rules...")
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base_url + "/robots.txt")
    try:
        rp.read()
        if rp.can_fetch("*", base_url + "/"):
            print("[+] Robots.txt allows crawling this website.")
        else:
            print("[-] Note: Robots.txt requests that automated crawlers stay minimized.")
    except Exception:
        print("[-] Could not find or read robots.txt (Site might not have one).")

def parse_sitemap(base_url):
    print(f"\n[+] Searching for public XML Sitemap...")
    sitemap_url = base_url + "/sitemap.xml"
    headers = {'User-Agent': 'Mozilla/5.0 (Termux; Android)'}
    
    try:
        response = requests.get(sitemap_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'xml')
            urls = soup.find_all('loc')
            if urls:
                print(f"[+] Found {len(urls)} public URLs listed in the sitemap:")
                for i, loc in enumerate(urls[:15], 1): 
                    print(f"    {i}. {loc.text}")
            else:
                print("[-] Sitemap found, but no URLs were parsed inside it.")
        else:
            print(f"[-] No sitemap found at {sitemap_url} (Status: {response.status_code})")
    except Exception as e:
        print(f"[-] Error reading sitemap: {e}")

def crawl_website():
    print_banner()
    
    url = input("Enter website URL (e.g., https://example.com): ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    base_url = get_base_url(url)
    print(f"\n[+] Target Base URL: {base_url}\n")
    
    check_robots_txt(base_url)
    parse_sitemap(base_url)
    
    print(f"\n[+] Fetching homepage HTML structure...")
    headers = {'User-Agent': 'Mozilla/5.0 (Termux; Android)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.title.string if soup.title else "No Title"
            print(f"\n=== Website Title ===")
            print(title)
            
            print(f"\n=== Public Homepage Links ===")
            links = soup.find_all('a', href=True)
            for i, link in enumerate(links[:15], 1):
                print(f"{i}. {link['href']}")
        else:
            print(f"[-] Could not load homepage HTML. Status: {response.status_code}")
    except Exception as e:
        print(f"[-] Error loading homepage: {e}")

if __name__ == "__main__":
    crawl_website()
