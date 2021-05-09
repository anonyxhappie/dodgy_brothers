from django.test import TestCase
from dealership_app.models import Car, BuyersRequest
  
class CarModelTest(TestCase):
  
    def add_car(self):
        return Car.objects.create(seller_name='Akshay', seller_mobile='9876543210', make='Ford', model='Falcon', year='2021', condition='POOR', asking_price='20000')
  
    def test_add_car(self):
        car = self.add_car()
        self.assertTrue(isinstance(car, Car))
        self.assertEqual('Falcon', car.model)
  
class BuyersRequestModelTest(TestCase):
      
    def add_car(self):
        return Car.objects.create(seller_name='Akshay', seller_mobile='9876543210', make='Ford', model='Falcon', year='2021', condition='POOR', asking_price='20000')
  
    def add_buyers_request(self):
        car = self.add_car()
        return BuyersRequest.objects.create(buyer_name='Saini', buyer_mobile='9876543211', car=car)
  
    def test_add_buyers_request(self):
        buyreq = self.add_buyers_request()
        self.assertTrue(isinstance(buyreq, BuyersRequest))
        self.assertTrue(isinstance(buyreq.car, Car))
        self.assertEqual('Saini', buyreq.buyer_name)
