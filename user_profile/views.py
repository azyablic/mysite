from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers
from .models import MainCycle, Boost
import services


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

    def get_queryset(self):
        return Boost.objects.filter(mainCycle=self.kwargs['mainCycle'])


@api_view(['GET'])
def call_click(request):
    data = services.clicker_services.call_click(request)
    return Response(data)


@api_view(['POST'])
def buy_boost(request):
    main_cycle, level, price, power = services.clicker_services.buy_boost(request)
    return Response({'clickPower': main_cycle.clickPower,
                     'coinsCount': main_cycle.coinsCount,
                     'autoClickPower': main_cycle.autoClickPower,
                     'level': level,
                     'price': price,
                     'power': power})


@api_view(['POST'])
def set_main_cycle(request):
    user = request.user
    data = request.data
    MainCycle.objects.filter(user=user).update(
        coinsCount=data['coinsCount']
    )
    return Response({'success': 'ok'})
