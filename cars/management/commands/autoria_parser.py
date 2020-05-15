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
        parser.add_argument('--debug', type=bool, default=False)
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
            print(f'Found number of pages {int(pagination[-1].get_text(strip=True))}')
            return int(pagination[-1].get_text(strip=True))
        else:
            return 1

    @staticmethod
    def remove_old_cars(cars, brand):
        web_links = ['link for car']
        for link in cars:
            web_links.append(link['link for car'])
        old_car = Car.objects.filter(brand=brand).exclude(link__in=web_links)
        print(f'There is a number of cars what was delete {old_car.count()}')
        old_car.delete()

    def handle(self, *args, **options):
        pars = BaseParser()
        page = pars.get_html_by_selenium(options['base_url'])
        count = self.get_page_count(page)
        cars = []
        brand, created = Brand.objects.get_or_create(
            name=options['brand'],
            base_url=options['base_url']
        )
        if created:
            brand.save()
            print(f"Brand {options['brand']} was created")
        else:
            print(f"{options['brand']} already exists")

        for page in range(1, count + 1):
            print(f'Get all cars on page {page} from {count}')
            pars.get(options['base_url'] + f'/?page={page}')
            cars.extend(self.get_content(pars.get_html_by_selenium(options['base_url'] + f'/?page={page}')))
        self.remove_old_cars(cars, options['brand'])

        # save cars to db
        if options['debug']:
            print(f'Parsing is complete total number of cars is {len(cars)} there is a list of parsed cars : \n {cars}')
        else:
            for car in cars:
                auto, created = Car.objects.get_or_create(
                    brand=Brand.objects.get(name=options['brand']),
                    title=car['title'],
                    price_in_usd=car['price in $'],
                    price_in_uah=car['price in UAH'],
                    location=car['location'],
                    range=car['range'],
                    link=car['link for car'],
                )
                if created:
                    auto.save()
                else:
                    print(f'This car {car["title"]} : {car["link for car"]} already exists')
            print(f'There was parsed {len(cars)} cars for {options["brand"]} brand')
