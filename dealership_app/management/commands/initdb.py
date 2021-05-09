import logging

from django.core.management.base import BaseCommand, CommandError
from dealership_app.models import Car
from dealership_app.exceptions import CustomException

class Command(BaseCommand):
    help = 'Create superuser account'
    
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        res = self.create_db()
        if res: self.stdout.write(self.style.SUCCESS('DB Created Successfully'))
        else: self.stdout.write(self.style.SUCCESS('DB Create Skipped'))

    def create_db(self):
        try:
            car_objs = Car.objects.all()
            if len(car_objs) > 0: return
            cars = [('Phoebe', '9876543210', 'Ford', 'Falcon', '2019', 'POOR', 20000),
            ('Joey', '9876543211', 'Ford', 'Falcon', '2021', 'EXCELLENT', 40000),
            ('Chandler', '9876543212', 'Tata', 'Nano', '2018', 'GOOD', 22000),
            ('Monica', '9876543213', 'Tesla', '3', '2018', 'FAIR', 30000),
            ('Rachel', '9876543213', 'Tesla', 'Y', '2020', 'EXCELLENT', 40000),
            ('Janice', '9876543213', 'Tata', 'Sumo', '2004', 'FAIR', 13000),
            ('Gunther', '9876543214', 'Holden', 'Commodore', '2017', 'POOR', 5000)]
            for car in cars:
                c = Car(seller_name=car[0], seller_mobile=car[1], make=car[2], model=car[3], year=car[4], condition=car[5], asking_price=car[6])
                c.save()
            return True
        except Exception:
            raise CustomException('DATABASE_WRITE_ERROR')
