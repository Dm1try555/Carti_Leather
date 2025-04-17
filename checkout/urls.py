from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('create/', views.create_order, name='create_order'),
    path('thank-you/<int:order_id>/', views.thank_you, name='thank_you'),
    path('cities/', views.get_cities, name='cities'),
    path('offices/<str:city_ref>/', views.get_offices, name='offices'),
]
