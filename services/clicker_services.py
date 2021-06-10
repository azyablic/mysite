from django.contrib.auth.models import User
from django.db.models import Prefetch

from user_profile.models import MainCycle, Boost
from user_profile.serializers import BoostSerializer


def main_page(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) != 0:
        mainCycle = MainCycle.objects.get(user=request.user)
        return False, 'index.html', {'user': user[0], 'mainCycle': mainCycle}
    else:
        return True, 'login', {}


def call_click(request):
    mainCycle = MainCycle.objects.get(user=request.user)
    isLevelUp = mainCycle.Click()
    boostsQuery = Boost.objects.filter(mainCycle=mainCycle)
    boosts = BoostSerializer(boostsQuery, many=True).data
    mainCycle.save()
    if isLevelUp:
        return {"coinsCount": mainCycle.coinsCount, "boosts": boosts}
    return {"coinsCount": mainCycle.coinsCount, "boosts": None}


def buy_boost(request):
    boostLevel = request.data['boost_level']
    cycle =  MainCycle.objects.prefetch_related(
    Prefetch('boosts',
              queryset=Boost.objects.filter(level=boostLevel),
              to_attr='current_boost'
              )).get(user=request.user)
    boost = cycle.current_boost[0]
    main_cycle, level, coins_count, price = boost.upgrade()
    boost.save()
    return main_cycle, level, coins_count, price