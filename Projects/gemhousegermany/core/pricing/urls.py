# price_engine/urls.py
from django.urls import path
from .views import RegisterView, get_diamond_list_prices, plot_diamond_prices, plot_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('prices/<str:shape>/', get_diamond_list_prices, name='get_diamond_prices'),
    path('plot/<str:shape>/', plot_diamond_prices, name='plot_diamond_prices'),
    path('plot/', plot_view, name='plot_view'),

]
