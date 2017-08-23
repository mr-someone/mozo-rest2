# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings
from .models import MyUser, Account, Transactions, Expenses


from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ('user',)


admin.autodiscover()
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Account)
admin.site.register(Transactions)
admin.site.register(Expenses)