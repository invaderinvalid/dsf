from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('create/', views.create_service, name='create_service'),
    path('orders/', views.order_list, name='order_list'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]
