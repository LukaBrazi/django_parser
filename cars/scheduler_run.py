import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parser_dj.settings")
django.setup()
from cars.models import Brand
from apscheduler.schedulers.blocking import BlockingScheduler


def parse_them_all():
    brands = Brand.objects.all()
    os.chdir(r'/Users/Dimas130790.gmail.com/PycharmProjects/Parser_dj')
    for brand in brands:
        print('start parsing')
        os.system(f"python3 manage.py autoria_parser --brand={brand.name} --base_url={brand.base_url}")
        print(f"Brand {brand.name} was parsed")


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(parse_them_all, 'interval', seconds=100, max_instances=5)
    scheduler.start()
