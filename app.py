from flask import Flask
from bs4 import BeautifulSoup
from flask import request
import requests
import json

app = Flask(__name__)


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    r = requests.get(url, headers=headers)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_proxies_list(url):
    result = []
    html = get_html(url)
    if html.status_code == 200:
        items = get_content(html.text).find_all('tr')[1:]
        for item in items:
            item = item.find_all('td')
            ip = item[0].get_text()
            port = item[1].get_text()
            result.append(ip + ':' + port)
        return result
    else:
        return []


def get_https_proxies_list():
    url = 'https://hidemy.name/ua/proxy-list/?country=ARAMAUBDBZBRKHCACLCNCOCWCYCZECFRDEHKHUINIDIRNLPHPTRORSSGESCHTHTRUAGBUSVG&maxtime=1500&type=s#list'
    return get_proxies_list(url)


def get_socks4_proxies_list():
    url = 'https://hidemy.name/ua/proxy-list/?country=ARAMAUBDBZBRKHCACLCNCOCWCYCZECFRDEHKHUINIDIRNLPHPTRORSSGESCHTHTRUAGBUSVG&maxtime=1500&type=4#list'
    return get_proxies_list(url)


def get_socks5_proxies_list():
    url = 'https://hidemy.name/ua/proxy-list/?country=ARAMAUBDBZBRKHCACLCNCOCWCYCZECFRDEHKHUINIDIRNLPTRORSSGESCHTHTRUAGBUSVG&maxtime=1500&type=5#list'
    return get_proxies_list(url)


@app.route('/proxies')
def get_https_proxies():  # put application's code here
    result = []
    if request.args.getlist('type'):
        for type in request.args.getlist('type'):
            if type == "https":
                result = result + get_https_proxies_list()
            if type == "socks4":
                result = result + get_socks4_proxies_list()
            if type == "socks5":
                result = result + get_socks5_proxies_list()
    else:
        result = get_https_proxies_list() + get_socks4_proxies_list() + get_socks5_proxies_list()

    return json.dumps(result)


if __name__ == '__main__':
    app.run()
    get_https_proxies_list()
