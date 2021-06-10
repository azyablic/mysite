from rest_framework import serializers
from django.contrib.auth.models import User

from .models import MainCycle, Boost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class UserSerializerDetails(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'cycle']


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCycle
        fields = ['id']


class CycleSerializerDetails(serializers.ModelSerializer):
    class Meta:
        model = MainCycle
        fields = ['id', 'user', 'coinsCount', 'clickPower', 'boosts']


class BoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boost
        fields = ['level', 'power', 'price', 'boost_type']
