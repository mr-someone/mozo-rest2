from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from mozorestapi.models import Transactions, Expenses
from .models import MyUser


class FriendsSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'profile_pic')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField()
    friends = FriendsSerializer(many=True, queryset=MyUser.objects.all(), allow_null=True, allow_empty=True, default=[])

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_pic = validated_data['profile_pic'],
            facebook_id = validated_data['facebook_id'],
            google_id = validated_data['google_id']
        )
        user.set_password(validated_data['password'])
        user.friends = validated_data['friends']
        user.save()
        return user

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'facebook_id', 'google_id', 'profile_pic', 'balance', 'friends')


class TransactionsSerializer(serializers.HyperlinkedModelSerializer):
    fromUser = serializers.ReadOnlyField(source='fromUser.username')
    toUser = serializers.ReadOnlyField(source='toUser.username')

    class Meta:
        model = Transactions
        fields = ('transactionType', 'toUser', 'fromUser', 'transactionAmount', 'transactionStatus', 'transactionDetail')


class ExpensesSerializer(serializers.HyperlinkedModelSerializer):
    expenseUser = serializers.ReadOnlyField(source='expenseUser.username')

    class Meta:
        model = Expenses
        fields = ('__all__')

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'first_name', 'last_name', 'email', 'profile_pic')