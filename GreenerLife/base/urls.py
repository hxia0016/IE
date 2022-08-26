from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = "home"),
    path('e_waste/', views.e_waste, name = "e_waste"),
    path('clothing/', views.clothing, name = "clothing")
]