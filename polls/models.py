import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class CustomUserManager(UserManager):
    pass

class UserInfo(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=50, default='Mexico')
    #date = models.DateField('Fecha de nacimiento')

    def __str__(self):
        return self.email

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=75)
    product_price = models.DecimalField(decimal_places=2, max_digits=9)
    product_pub = models.DateTimeField('date published')
    product_image = models.ImageField(upload_to = 'pic_folder')
    product_description = models.CharField(max_length=150)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


