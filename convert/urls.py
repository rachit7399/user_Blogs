from django.urls import path
from . import views


urlpatterns = [
    path('',views.ConvertCurrView.as_view(), name = 'register'),
]
