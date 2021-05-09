from django.db import models
import uuid

class Car(models.Model):
    YEAR_IN_CHOICES = [(str(x), str(x)) for x in range(2000, 2022)]
    CONDITION_IN_CHOICES = [
        ('POOR', 'Poor'),
        ('FAIR', 'Fair'),
        ('GOOD', 'Good'),
        ('EXCELLENT', 'Excellent'),
    ]
    CURRENCY_IN_CHOICES = [
        ('$', 'USD'),
        # ('₹', 'INR'),
    ]
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) 
    seller_name = models.CharField(max_length=255)
    seller_mobile = models.CharField(max_length=16)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.CharField(
        max_length=4,
        choices=YEAR_IN_CHOICES,
        default=YEAR_IN_CHOICES[0][0],
    )
    condition = models.CharField(
        max_length=9,
        choices=CONDITION_IN_CHOICES,
        default=CONDITION_IN_CHOICES[2][0],
    )
    currency = models.CharField(
        max_length=1,
        choices=CURRENCY_IN_CHOICES,
        default=CURRENCY_IN_CHOICES[0][0],
    )
    asking_price = models.IntegerField()
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BuyersRequest(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) 
    buyer_name = models.CharField(max_length=255)
    buyer_mobile = models.CharField(max_length=16)
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

