from requests_html import HTMLSession


import requests


def using_requests(url):
    r = requests.get(url)
    print(f"get {r.status_code} using requests")
    if r.status_code == 200:
        with open("requests.html","w") as file:
            file.write(r.text)


if __name__=="__main__":
    url_lvl_1 = "https://books.toscrape.com/"


    using_requests(url_lvl_1)