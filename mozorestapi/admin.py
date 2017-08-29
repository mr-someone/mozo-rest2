# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import MyUser, Transactions, Expenses


from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ('user',)


admin.autodiscover()
admin.site.register(MyUser)
admin.site.register(Transactions)
admin.site.register(Expenses)