from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CUserLoginForm, CUserRegisterForm, CUserChangeForm
from .models import Question, Choice, UserInfo, Product, Category

class CustomUserAdmin(UserAdmin):
    model = UserInfo
    add_form = CUserRegisterForm
    form = CUserChangeForm

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserInfo, CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Category)