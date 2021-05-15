from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics
from . import serializers
from .models import MainCycle, Boost


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializerDetails


class CycleList(generics.ListAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = serializers.CycleSerializer


class CycleDetail(generics.RetrieveAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = serializers.CycleSerializerDetails


class BoostList(generics.ListAPIView):
    queryset = Boost.objects.all()
    serializer_class = serializers.BoostSerializer


class BoostDetail(generics.RetrieveAPIView):
    queryset = Boost.objects.all()
    serializer_class = serializers.BoostSerializerDetails


def callClick(request):
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    mainCycle.Click()
    mainCycle.save()
    return HttpResponse(mainCycle.coinsCount)


def buyBoost(request):
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    boosts = Boost.objects.filter(mainCycle=mainCycle)
    if boosts.count() == 0:
        if mainCycle.coinsCount < 10:
            return HttpResponse(mainCycle.clickPower)
        boost = Boost()
        boost.mainCycle = mainCycle
        boost.save()
        boost.Upgrade()
        mainCycle.save()
        return HttpResponse(mainCycle.clickPower)
    boost = boosts[0]
    if mainCycle.coinsCount < boost.price:
        return HttpResponse(mainCycle.clickPower)
    boost.mainCycle = mainCycle
    boost.Upgrade()
    mainCycle.save()
    boost.save()
    return HttpResponse(mainCycle.clickPower)
