from bs4 import BeautifulSoup
from requests_html import HTMLSession
from curl_cffi import requests as req_curl
from selenium import webdriver
from selenium_stealth import stealth
from playwright.sync_api import sync_playwright

import time
import cloudscraper
import hrequests
import requests as reqs
import httpx


def save_to(content,filename):
    with open(filename,"w") as file:
        file.write(content)
    #print(f"saved to {filename}")

def find_title(html):
    soup = BeautifulSoup(html,"html.parser")
    title = soup.find("title").text.strip()
    print(title)

def using_requests(url):
    r = reqs.get(url)
    print(f"get {r.status_code} using requests")
    if r.status_code == 200:
        find_title(r.text)
        save_to(r.text,"requests.html")
    return r.text

def using_requests_html(url):
    # first run will do
    # [INFO] Starting Chromium download.
    # there is issue for Chromium version as mentioned here per Apr, 2023 :
    # https://github.com/psf/requests-html/issues/540
    # read requests-html_error.MD

    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1,scrolldown=15)
    html = r.html.html
    print(f"get {r.status_code} using requests-html")
    if r.status_code == 200:
        find_title(html)
        save_to(html,"requests-html.html")
    return html

def using_httpx(url):
    r = httpx.get(url)
    print(f"get {r.status_code} using httpx")
    if r.status_code == 200:
        find_title(r.text)
        save_to(r.text,"httpx.html")
    return r.text

def using_hrequests(url):
    # headless browsing should false if want to bypass zillow
    session = hrequests.BrowserSession(browser="firefox",mock_human=True)
    resp = session.get(url)
    print(f"get {resp.status_code} using hrequests")
    if resp.status_code == 200:
        html = resp.html.html
        find_title(html)
        save_to(html,"hrequests.html")
    return html

def using_curl(url,impersonate):
    # Use the latest impersonate versions, findout here:
    # https://github.com/yifeikong/curl-impersonate?tab=readme-ov-file#supported-browsers
    
    r = req_curl.get(url,impersonate=impersonate)
    print(f"get {r} using curl")
    if r.status_code == 200:
        find_title(f"{r.text} using curl")
        save_to(r.text,"curl.html")
    return r.text

def using_cloudscraper(url):
    scraper = cloudscraper.create_scraper()
    r = scraper.get(url)
    print(f"get {r.status_code} using cloudscraper")
    if r.status_code == 200:
        find_title(f"{r.text} using cloudscraper")
        save_to(r.text,"cloudscraper.html")
    return r.text

def using_stealth(url):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.get(url)
    html = driver.page_source
    time.sleep(5)
    driver.quit()
    print("get html using selenium stealth")
    if html:
        find_title(f"{html} using selenium stealth")
        save_to(html,"selenium_stealth.html")
    return html

def using_playwright(url):
    pw = sync_playwright().start()
    brows = pw.chromium.launch()
    page = brows.new_page()
    page.goto(url)
    print(f"get html using playwright")
    time.sleep(5)
    if page.content():
        html = page.content()
        find_title(html)
        save_to(html,"playwright.html")
    brows.close()
    pw.stop()
    return html
    

if __name__=="__main__":
    # url = "https://www.amazon.com/"   # protected by text captcha
    # url = "https://www.zillow.com/"   # protected by human click&hold verification
    # url = "https://bookoutlet.com/"   # protected by cloudflare

    url = "https://www.nrl.com/players/?competition=111"

    #functions = [using_requests,using_requests_html, using_httpx, using_cloudscraper, using_hrequests, using_curl, using_stealth]

    # update : requests-html is often bugging, httpx is better than requests
    #using_requests(url)
    #using_requests_html(url)
    using_httpx(url)
    using_curl(url,"chrome120")
    using_cloudscraper(url)
    using_hrequests(url)
    using_stealth(url)
    using_playwright(url)