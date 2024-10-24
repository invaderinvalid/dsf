from django.urls import path
from . import views

urlpatterns = [
    path('', views.trend_analysis_list, name='trend_analysis_list'),
    path('new/', views.create_trend_analysis, name='trend_analysis_new'),
    path('<int:analysis_id>/', views.trend_analysis_detail, name='trend_analysis_detail'),
]
