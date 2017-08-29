# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import status, viewsets, permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mozorestapi.serializers import UserSerializer, FriendsSerializer, TransactionsSerializer, ExpensesSerializer, \
    AccountSerializer
from rest_framework.authtoken.models import Token
from .models import MyUser, Transactions, Expenses, Account


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class FriendsViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = FriendsSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(accountUser=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(expenseUser=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(fromUser=self.request.user)


class getUserAndAuth(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(getUserAndAuth, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = MyUser.objects.get(id=token.user_id)
        userSerializer = UserSerializer(user)
        return Response({'token': token.key, 'user': userSerializer.data})

@api_view(['POST'])
def SearchFriends(request):
    if request.method == 'POST':
        if 'last_name' in request.data:
            user = MyUser.objects.filter(first_name__contains=request.data['first_name']).filter(last_name__contains=request.data['lastname'])
        else:
            user = MyUser.objects.filter(first_name__contains=request.data['first_name'])
        friendsList = FriendsSerializer(user, many=True)
        return Response(friendsList.data)


@api_view(['POST'])
def SocialAuthFacebook(request):
    if request.method == 'POST':
        token = request.data['token']
        url = 'https://graph.facebook.com/me?fields=id,name,email,first_name,last_name,picture&access_token=' + token
        r = requests.get(url)
        data = json.loads(r.text)
        if 'error' in data:
            resData = {'error': 'Invalid Auth Token ! Beware this incident will be reported !'}
        else:
            try:
                user = MyUser.objects.get(username=data['email'])
                if user.facebook_id == 'null':
                    user.facebook_id = data['id']
                    user.profile_pic = data['picture']['data']['url']
                    user.save()
                serializer = UserSerializer(user)
                token = Token.objects.get(user=user)
                resData = {'token': token.key, 'userData': serializer.data}
            except MyUser.DoesNotExist:
                newUser = {'username': data['email'],
                           'email': data['email'],
                           'first_name': data['first_name'],
                           'last_name': data['last_name'],
                           'password': 'shotu123',
                           'profile_pic': data['picture']['data']['url'],
                           'facebook_id': data['id'],
                           'google_id': 'null'
                           }
                serializer = UserSerializer(data = newUser)
                if serializer.is_valid():
                    serializer.save()
                    user = MyUser.objects.get(username=data['email'])
                    token, created = Token.objects.get_or_create(user=user)
                    resData = {'token': token.key, 'userData': serializer.data}
                else:
                    resData = {'error': serializer.errors}
        return Response(resData)


@api_view(['POST'])
def SocialAuthGoogle(request):
    if request.method == 'POST':
        token = request.data['token']
        url = 'https://www.googleapis.com/userinfo/v2/me'
        header = {'Authorization': 'Bearer ' + token}
        r = requests.get(url, headers=header)
        data = json.loads(r.text)
        if 'error' in data:
            resData = {'error': 'Invalid Auth Token ! Beware this incident will be reported !'}
        else:
            try:
                user = MyUser.objects.get(username=data['email'])
                if user.google_id == 'null':
                    user.google_id = data['id']
                    user.save()
                if user.profile_pic == 'null':
                    user.profile_pic = data['picture']
                    user.save()
                serializer = UserSerializer(user)
                token = Token.objects.get(user=user)
                resData = {'token': token.key, 'userData': serializer.data}
            except MyUser.DoesNotExist:
                newUser = {'username': data['email'],
                           'email': data['email'],
                           'first_name': data['given_name'],
                           'last_name': data['family_name'],
                           'password': 'shotu123',
                           'profile_pic': data['picture'],
                           'facebook_id': 'null',
                           'google_id': data['id']
                           }
                serializer = UserSerializer(data = newUser)
                if serializer.is_valid():
                    serializer.save()
                    user = MyUser.objects.get(username=data['email'])
                    token, created = Token.objects.get_or_create(user=user)
                    resData = {'token': token.key, 'userData': serializer.data}
                else:
                    resData = {'error': serializer.errors}
        return Response(resData)