from django.urls import path
from . import views


urlpatterns = [
    path('/', views.check_pesel_view, name='check_pesel'),
]