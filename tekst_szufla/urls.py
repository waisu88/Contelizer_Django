from django.urls import path
from . import views

urlpatterns = [
    path('/', views.upload_txt_file, name='upload_file'),
]