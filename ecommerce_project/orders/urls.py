from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('get_districts/<int:province_id>/', views.get_districts, name='get_districts'),
    path('api/districts/', views.districts_json, name='districts_json'),
    path('api/wards/', views.wards_json, name='wards_json'),
    path('api/order/<int:order_id>/', views.order_detail_api, name='order_detail_api'),
]
