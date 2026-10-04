import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse

def print_banner():
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

def detect_backend_and_database(headers, html_content):
    print("=" * 45)
    print("       DETECTED BACKEND & TECH STACK       ")
    print("=" * 45)
    
    # 1. Analyze Server Header Tokens
    server = headers.get("Server", "Unknown Server")
    powered_by = headers.get("X-Powered-By", "Hidden/Not Disclosed")
    
    print(f"[+] Primary Web Server:  {server}")
    print(f"[+] Backend Framework:   {powered_by}")
    
    # 2. Check for fingerprint clues in HTTP Headers
    backend_guess = "Unknown Logic Engine"
    database_guess = "Standard Relational SQL or Hidden Backend Instance"
    
    # Check framework headers
    headers_str = str(headers).lower()
    if "phpsessid" in headers_str or "php" in powered_by.lower():
        backend_guess = "PHP (Hypertext Preprocessor)"
        database_guess = "Typically paired with MySQL or MariaDB"
    elif "express" in powered_by.lower() or "io.js" in headers_str:
        backend_guess = "Node.js (Express Framework)"
        database_guess = "Typically paired with MongoDB or PostgreSQL"
    elif "csrftoken" in headers_str or "django" in headers_str:
        backend_guess = "Python (Django Framework)"
        database_guess = "Typically paired with PostgreSQL or SQLite"
    elif "asp.net" in powered_by.lower() or "aspnet" in headers_str:
        backend_guess = "Microsoft .NET Backend"
        database_guess = "Typically paired with Microsoft SQL Server"
        
    # 3. Analyze HTML content for CMS / structural fingerprints
    soup = BeautifulSoup(html_content, 'html.parser')
    html_str = html_content.lower()
    
    # Look for meta generator tags
    meta_generator = soup.find("meta", attrs={"name": "generator"})
    if meta_generator:
        cms = meta_generator.get("content", "")
        print(f"[+] CMS System Engine:   {cms}")
        if "wordpress" in cms.lower():
            backend_guess = "PHP (WordPress Core)"
            database_guess = "MySQL / MariaDB Instance"
            
    if "wp-content" in html_str:
        backend_guess = "PHP (WordPress Framework Detection)"
        database_guess = "MySQL Engine Database"
        
    print(f"[+] Deduced Backend System: {backend_guess}")
    print(f"[+] Deduced Database Type:  {database_guess}")
    print("=" * 45 + "\n")

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
                for i, loc in enumerate(urls[:10], 1): 
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
    
    print(f"[+] Fetching live server headers and structure...")
    headers = {'User-Agent': 'Mozilla/5.0 (Termux; Android)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Run the Tech Stack Fingerprint Scanner
            detect_backend_and_database(response.headers, response.text)
            
            # Run compliance scanners
            check_robots_txt(base_url)
            parse_sitemap(base_url)
        else:
            print(f"[-] Could not connect to site. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"[-] Connection Error: {e}")

if __name__ == "__main__":
    crawl_website()
