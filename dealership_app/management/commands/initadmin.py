import logging

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from dodgy_brothers.settings import ADMIN_EMAIL, ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_FIRSTNAME
from dealership_app.exceptions import CustomException

class Command(BaseCommand):
    help = 'Create superuser account'
    
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        res = self.create_superuser()
        if res: self.stdout.write(self.style.SUCCESS('Admin User - {} created successfully'.format(ADMIN_USERNAME)))

    def create_superuser(self):
        try:
            if User.objects.filter(email=ADMIN_EMAIL).count() == 0:
                admin = User.objects.create_superuser(email=ADMIN_EMAIL, username=ADMIN_USERNAME, password=ADMIN_PASSWORD, first_name=ADMIN_FIRSTNAME)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
                self.logger.debug('Admin User - {} created'.format(ADMIN_USERNAME))    
                return True
            else:
                err_msg = 'Admin user already exist'
                print(err_msg)
                self.logger.debug(err_msg)
                return False    

        except Exception:
            raise CustomException('DATABASE_WRITE_ERROR')
