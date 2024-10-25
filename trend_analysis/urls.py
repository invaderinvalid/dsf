from django.urls import path
from . import views

urlpatterns = [
    path('', views.trend_analysis_list, name='trend_analysis_list'),
    path('<str:topic>/', views.trend_analysis_detail, name='trend_analysis_detail'),
]
