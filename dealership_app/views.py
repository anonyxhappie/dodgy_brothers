import logging
import traceback

from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Car, BuyersRequest
from .exceptions import CustomException
from .constants import Constants as Const
from .forms import ListCarForm, LoginForm, BuyersRequestForm

logger = logging.getLogger(__name__)

def home(request):
    """
        Home page for Dodgy brothers contains - Car lists, Login, Buy, Add options  
    """
    try:
        # on filter click & pagination
        page = request.GET.get(Const.PAGE, 1)
        filter_by = request.GET.get('filter', '-created_at')
        if filter_by not in ['make', 'year', '-created_at']: raise CustomException('INVALID_REQUEST')
        cars_list = Car.objects.order_by(filter_by)
        paginator = Paginator(cars_list, 10)
        cars = paginator.page(page)

        # on list car submit
        if request.method == 'POST':
            form = ListCarForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'success.html', {Const.MESSAGE: 'Success! Thank you for listing a car.', Const.PAGE: 'home'})
        else:
            # on make available button click
            if request.user.is_authenticated and request.GET.get('cid'):
                car = Car.objects.filter(unique_id=request.GET['cid'])
                if not car: raise CustomException('INVALID_CAR')
                car = car[0]
                car.is_sold = False
                car.save()
            
            # for empty form
            form = ListCarForm()
        
        return render(request, 'home.html', {'form': form, 'cars': cars, 'filter_by': filter_by, 'form_errors': bool(form.errors)})
    except CustomException as e:
        traceback.print_exc()
        return render(request, 'error.html', {Const.ERROR: e.error_message, Const.PAGE: 'home'})
    except Exception as e:
        traceback.print_exc()
        logger.exception(Const.EXCEPTION_CODES['DEFAULT'][1])
        return render(request, 'error.html', {Const.ERROR: Const.EXCEPTION_CODES['DEFAULT'][1], Const.PAGE: 'home'})
        
def buy(request):
    """
        Buy page for buyers - on buy button click
    """
    try:
        car = Car.objects.filter(unique_id=request.GET['cid'])
        if not car: raise CustomException('INVALID_CAR')
        car = car[0]
        # on buy form submit
        if request.method == 'POST':
            form = BuyersRequestForm(request.POST)
            if form.is_valid():
                buyreq = BuyersRequest(buyer_name=form.cleaned_data['buyer_name'], buyer_mobile=form.cleaned_data['buyer_mobile'], car=car)
                buyreq.save()
                car.is_sold = True
                car.save()

                # for sending email
                htmly = get_template('email.html')
                commission = car.asking_price*5/100
                d = { 'car': car, 'buyreq': buyreq, 'commission': commission, 'net_amount': car.asking_price-commission}
                html_content = htmly.render(d)
                send_mail(subject='Dodgy brothers: Car Buy Request', message='Recieved a car buy request', from_email=Const.EMAIL_FROM, recipient_list=[Const.EMAIL_TO], html_message=html_content)
                return render(request, 'success.html', {Const.MESSAGE: 'Success! Seller will be in touch with you soon.', Const.PAGE: 'home'})
        else:
            # for empty form
            form = BuyersRequestForm()

        return render(request, 'buy.html', {'form': form, 'car': car})
    except CustomException as e:
        traceback.print_exc()
        return render(request, 'error.html', {Const.ERROR: e.error_message, Const.PAGE: 'home'})
    except Exception as e:
        traceback.print_exc()
        logger.exception(Const.EXCEPTION_CODES['DEFAULT'][1])
        return render(request, 'error.html', {Const.ERROR: Const.EXCEPTION_CODES['DEFAULT'][1], Const.PAGE: 'home'})
   

def loginView(request):
    """
       Login page - on login button click
    """
    # for already logged in user
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    # on login form submit
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        # for empty form
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def logoutView(request):
    """
       Logout page - on logout button click
    """
    # on logout click
    logout(request)
    return HttpResponseRedirect('/')
