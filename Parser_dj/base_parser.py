import csv
import requests
from bs4 import BeautifulSoup
from .config import URL, HEADERS, PATH
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=options)


def get_html_by_request(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# todo remove this method to cars module
def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='page-item mhide')
    if pagination:
        print(int(pagination[-1].get_text(strip=True)))
        return int(pagination[-1].get_text(strip=True))
    else:
        return 1


# todo remove this method to cars module
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='content-bar')
    cars = []
    for item in items:
        cars.append({
            "title": item.find('a', class_='address', attrs='title').get_text().strip(),
            'price in $': item.find('span', class_='bold green size22', attrs='data-currency').get_text(),
            'price in UAH': item.find('span', class_='i-block', attrs='data-currency').get_text(),
            'location': item.find('li', class_='item-char view-location').get_text().strip(),
            'range': item.find('li', class_='item-char').get_text(strip=True),
            'link for car': item.find('a', class_='m-link-ticket', href=True).get('href')
        })
    print(len(cars))
    return cars


# todo remove this method to cars module
def save_file(items, path):
    with open(path, 'w+', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['title', 'price in $', 'price in UAH', 'location', 'range', 'link for car'])
        for item in items:
            writer.writerow([item['title'], item['price in $'],
                             item['price in UAH'], item['location'],
                             item['range'], item['link for car']])


# this is not necessary method you can remove it
# def parse():
#     html = get_html(URL)
#     if html.status_code == 200:
#         count = get_page_count(html)
#         cars = []
#         for page in range(1, count + 1):
#             print(f'Get all cars on page {page} from {count}')
#             html = get_html(URL, params={'page': page})
#             cars.extend(get_content(html.text))
#         save_file(cars, PATH)
#     else:
#         print(f'Something went wrong {html.status_code}')
def get_html_by_selenium(web_browser, url):
    web_browser.get(url)
    page = web_browser.page_source
    return page

# todo remove this method to cars module
def parse_with_selenium(browser, url):
    browser.get(url)
    page = browser.page_source
    count = get_page_count(page)
    cars = []
    for page in range(1, count + 1):
        print(f'Get all cars on page {page} from {count}')
        browser.get(url + f'/?page={page}')
        cars.extend(get_content(browser.page_source))
    save_file(cars, PATH)
    browser.close()
