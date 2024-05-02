# rpg/urls.py
from django.urls import path
from . import views

app_name = 'rpg'

urlpatterns = [
    path('', views.index, name='index'),  # The default view for the RPG app
    path('players/', views.player_list, name='player-list'),
    path('items/', views.item_list, name='item-list'),
    path('shops/', views.shop_list, name='shop-list'),
]