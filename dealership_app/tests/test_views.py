from django.test import TestCase
from django.urls import resolve
from django.contrib.auth.models import User
from dealership_app.models import Car, BuyersRequest
from dealership_app.management.commands.initadmin import Command

class HomeViewTest(TestCase):

    def setup(self):
        cars = [('Phoebe', '9876543210', 'Ford', 'Falcon', '2019', 'POOR', 20000),
        ('Joey', '9876543211', 'Ford', 'Falcon', '2021', 'EXCELLENT', 40000),
        ('Chandler', '9876543212', 'Tata', 'Nano', '2018', 'GOOD', 22000),
        ('Monica', '9876543213', 'Tata', 'Sumo', '2004', 'GOOD', 3000),
        ('Rachel', '9876543214', 'Holden', 'Commodore', '2017', 'POOR', 5000)]
        for car in cars:
            c = Car(seller_name=car[0], seller_mobile=car[1], make=car[2], model=car[3], year=car[4], condition=car[5], asking_price=car[6])
            c.save()

    def test_invalid_list_car(self):
        data = {"seller_name":'Akshay', "seller_mobile":'9876543210', "make":'Ford', "model":'Falcon', "year":'2021', "condition":'POOR', "currency":'$', "asking_price": 200}
        resolver = resolve('/')
        response = self.client.post('/', data)
        self.assertEqual(resolver.view_name, 'home')
        self.assertContains(response, 'Dodgy Brothers | Home')
        self.assertContains(response, 'Invalid range of Asking Price. Please enter between $1000-$100000.')
        
    def test_valid_list_car(self):
        data = {"seller_name":'Akshay', "seller_mobile":'9876543210', "make":'Ford', "model":'Falcon', "year":'2021', "condition":'POOR', "currency":'$', "asking_price": 2000}
        resolver = resolve('/')
        response = self.client.post('/', data, follow=True)
        self.assertEqual(resolver.view_name, 'home')
        self.assertContains(response, 'Success! Thank you for listing a car.')
        
    def test_home_view(self):
        self.setup()    
        resolver = resolve('/')
        response = self.client.get('/')
        self.assertEqual(resolver.view_name, 'home')
        self.assertContains(response, 'List Car')
        self.assertContains(response, 'Listed Cars')
        self.assertContains(response, 'Dodgy Brothers | Home')
        self.assertContains(response, 'Holden')

    def test_make_available(self):
        Command().handle()
        car = Car(seller_name='Akshay', seller_mobile='9876543210', make='Ford', model='Falcon', year='2021', condition='POOR', asking_price=20000, is_sold=True)
        car.save()
        data = {"username": "mike@example.org", "password": "mikeymike123"}
        response = self.client.post('/login/', data, follow=True)

        resolver = resolve('/')
        response = self.client.get('/?cid=%s' % car.unique_id)
        self.assertEqual(resolver.view_name, 'home')
        self.assertContains(response, 'List Car')
        self.assertContains(response, 'Listed Cars')
        self.assertContains(response, 'Dodgy Brothers | Home')
        self.assertContains(response, 'BUY')

    def test_invalid_filter(self):
        resolver = resolve('/')
        response = self.client.get('/?filter=test')
        self.assertEqual(resolver.view_name, 'home')
        self.assertContains(response, 'Request data is invalid')


class LoginViewTest(TestCase):
        
    def test_login_get_view(self):
        
        resolver = resolve('/login/')
        response = self.client.get('/login/')
        self.assertEqual(resolver.view_name, 'login')
        self.assertContains(response, 'Dodgy Brothers | Login')
        self.assertContains(response, 'Username')

    def test_invalid_login_post_view(self):
        
        data = {"username": "test@example.org", "password": "errorpassword"}
        Command().handle()
        resolver = resolve('/login/')
        response = self.client.post('/login/', data)
        self.assertEqual(resolver.view_name, 'login')
        self.assertContains(response, 'Invalid login. Please check username &amp; password.')

    def test_valid_login_post_view(self):
        
        data = {"username": "mike@example.org", "password": "mikeymike123"}
        Command().handle()
        Command().handle()
        resolver = resolve('/login/')
        response = self.client.post('/login/', data, follow=True)
        self.assertEqual(resolver.view_name, 'login')
        self.assertContains(response, 'Hello, Mike')
        self.assertContains(response, 'Logout')

class LogoutViewTest(TestCase):
        
    def setup(self):
        data = {"username": "mike@example.org", "password": "mikeymike123"}
        Command().handle()
        resolver = resolve('/login/')
        response = self.client.post('/login/', data, follow=True)
        
    def test_logout_view(self):
        self.setup()
        resolver = resolve('/logout/')
        response = self.client.get('/logout/', follow=True)
        self.assertEqual(resolver.view_name, 'logout')
        self.assertContains(response, 'Dodgy Brothers | Home')
        self.assertContains(response, 'Login')


class BuyViewTest(TestCase):

    def setup(self):
        car = Car(seller_name='Akshay', seller_mobile='9876543210', make='Ford', model='Falcon', year='2021', condition='POOR', asking_price=20000)
        car.save()
        return car.unique_id

    def test_buy_view(self):
        cid = self.setup()
        url = '/buy/?cid={}'.format(cid)
        resolver = resolve('/buy/')
        response = self.client.get(url)
        self.assertEqual(resolver.view_name, 'buy')
        self.assertContains(response, 'Dodgy Brothers | Buy')
        self.assertContains(response, 'Buyer name')
        
    def test_invalid_buy_view(self):
        url = '/buy/?cid=db90fa6b-b1dc-4328-ad66-dc813dc5bf7a'
        resolver = resolve('/buy/')
        response = self.client.get(url)
        self.assertEqual(resolver.view_name, 'buy')
        self.assertContains(response, 'Invalid car')

    def test_valid_buy_post_view(self):
        cid = self.setup()
        url = '/buy/?cid={}'.format(cid)
        data = {"buyer_name": "Akshay", "buyer_mobile": "9876543210"}
        resolver = resolve('/buy/')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(resolver.view_name, 'buy')
        self.assertContains(response, 'Success! Seller will be in touch with you soon.')

    def test_invalid_data(self):
        url = '/buy/?cid={}'
        resolver = resolve('/buy/')
        response = self.client.post(url, data={}, follow=True)
        self.assertEqual(resolver.view_name, 'buy')
        self.assertContains(response, 'There is some error in service, please try again later')