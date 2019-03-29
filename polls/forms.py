from django import forms
from polls.models import UserInfo, Product, Category
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CUserLoginForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta(UserCreationForm):
        model = UserInfo
        fields = ('email','password')

class CUserRegisterForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserInfo
        fields = ('username','password','email','country')

class CUserChangeForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserInfo
        fields = ('email','username','country')

class ProductForm(forms.Form):
    class Meta:
        model = Product

class CategoryForm(forms.Form):
    class Meta:
        model = Category
