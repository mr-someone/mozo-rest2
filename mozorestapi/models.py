# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from django.db import models

# Create your models here.


class MyUser(AbstractUser):
    facebook_id = models.CharField(max_length=100, default='null', blank=True)
    google_id = models.CharField(max_length=100, default='null', blank=True)
    profile_pic = models.CharField(default='null', max_length=300, blank=True)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    balance = models.FloatField(default=0)


class Transactions(models.Model):
    toUser = models.ForeignKey('mozorestapi.MyUser', related_name='transactionTo', on_delete=models.CASCADE, default=None)
    fromUser = models.ForeignKey('mozorestapi.MyUser', related_name="transactionFrom", on_delete=models.CASCADE, default=None)
    transactionType = models.CharField(choices=(('refund', 'Refundable Transaction'),('nonrefund','Non Refundable Transaction')), max_length=20, default='nonrefund')
    transactionAmount = models.FloatField()
    transactionStatus = models.BooleanField(default=0)
    transactionDetail = models.TextField(default='')


class Expenses(models.Model):
    expenseUser = models.ForeignKey('mozorestapi.MyUser', related_name="Expenses", on_delete=models.CASCADE)
    expenseType = models.CharField(choices=(('food', 'food'), ('education', 'education'), ('travel', 'travel'), ('shopping', 'shopping'), ('extra', 'extra'), ('living', 'living')), default='extra', max_length=20)
    expenseItem = models.CharField(max_length=100)
    expenseAmount = models.FloatField()
    expenseTime = models.DateTimeField(auto_created=True, auto_now=True)

