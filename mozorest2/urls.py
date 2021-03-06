"""mozorest2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from mozorestapi.views import UsersViewSet, getUserAndAuth, TransactionViewSet, ExpenseViewSet, \
    SocialAuthFacebook, SocialAuthGoogle, SearchFriends, GetFriendDetail
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register('user', UsersViewSet)
router.register('transactions', TransactionViewSet)
router.register('expenses', ExpenseViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get-user-and-auth/', getUserAndAuth.as_view()),
    url(r'^social-fb/', SocialAuthFacebook),
    url(r'^social-google/', SocialAuthGoogle),
    url(r'^auth-user-token/', views.obtain_auth_token),
    url(r'^search-friends/', SearchFriends),
    url(r'^get-friends/', GetFriendDetail)
]
urlpatterns += [

]