import csv
import requests
from bs4 import BeautifulSoup
from .config import URL, HEADERS, PATH
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseParser:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(options=options)

    def get(self, url):
        self.browser.get(url)

    def get_html_by_selenium(self, url):
        self.browser.get(url)
        page = self.browser.page_source
        return page

    def page_source(self):
        return self.browser.page_source

    @staticmethod
    def get_html_by_request(url, params=None):
        r = requests.get(url, headers=HEADERS, params=params)
        return r
