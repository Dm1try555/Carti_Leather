from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('create/', views.create_order, name='create_order'),
    path('thank-you/<int:order_id>/', views.thank_you, name='thank_you'),

]
