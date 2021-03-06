from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<pk>/', views.UserDetail.as_view()),
    path('cycles/', views.CycleList.as_view()),
    path('cycles/<pk>', views.CycleDetail.as_view()),
    path('boosts/<int:mainCycle>/', views.BoostList.as_view()),
    path('click/', views.call_click, name="click"),
    path('buyBoost/', views.buy_boost, name="buyBoost"),
    path('set_main_cycle/', views.set_main_cycle),
]
