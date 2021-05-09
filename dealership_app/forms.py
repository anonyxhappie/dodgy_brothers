from django import forms
from .models import Car, BuyersRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class ListCarForm(forms.ModelForm):

    class Meta:
        model = Car
        exclude = ('is_sold', )

    def clean(self, *args, **kwargs):
        asking_price = self.cleaned_data.get("asking_price")
        if asking_price < 1000 or asking_price > 100000:
            raise forms.ValidationError("Invalid range of Asking Price. Please enter between $1000-$100000.")
        
class BuyersRequestForm(forms.ModelForm):

    class Meta:
        model = BuyersRequest
        exclude = ('car',)

class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password and not authenticate(username=username, password=password):
            raise forms.ValidationError("Invalid login. Please check username & password.")
        
        return self.cleaned_data