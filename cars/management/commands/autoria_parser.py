import csv

from django.core.management.base import BaseCommand
from Parser_dj.base_parser import BaseParser
from bs4 import BeautifulSoup
from cars.models import Car, Brand


class Command(BaseCommand):
    help = 'Autoria parsing'



    @staticmethod
    def add_arguments(parser):
        """ arguments config """
        parser.add_argument('--brand', type=str, required=True)
        parser.add_argument('--base_url', type=str, required=True)


    @staticmethod
    def get_content(html):
        soup = BeautifulSoup(str(html), 'html.parser')
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

    @staticmethod
    def save_file(items, path):
        with open(path, 'w+', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['title', 'price in $', 'price in UAH', 'location', 'range', 'link for car'])
            for item in items:
                writer.writerow([item['title'], item['price in $'],
                                 item['price in UAH'], item['location'],
                                 item['range'], item['link for car']])

    @staticmethod
    def get_page_count(html):
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find_all('span', class_='page-item mhide')
        if pagination:
            print(int(pagination[-1].get_text(strip=True)))
            return int(pagination[-1].get_text(strip=True))
        else:
            return 1

    def handle(self, *args, **options):
        pars = BaseParser()
        page = pars.get_html_by_selenium(options['base_url'])
        count = self.get_page_count(page)
        cars = []
        Brand(
            name=options['brand'],
            base_url=options['base_url']
        ).save()
        print(f'{options["brand"]} was added to brands')
        for page in range(1, count + 1):
            print(f'Get all cars on page {page} from {count}')
            pars.get(options['base_url'] + f'/?page={page}')
            cars.extend(self.get_content(pars.get_html_by_selenium(options['base_url'] + f'/?page={page}')))
        for car in cars:
            Car(
                brand=Brand.objects.get(name=options['brand']),
                title=car['title'],
                price_in_usd=car['price in $'],
                price_in_uah=car['price in UAH'],
                location=car['location'],
                range=car['range'],
                link=car['link for car'],
            ).save()
        print(f'There was parsed {len(cars)} cars for {options["brand"]} brand')