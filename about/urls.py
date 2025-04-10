from django.urls import path
from .views import AboutAuthorView, AboutDeliveryView, AboutPaymentView


app_name = 'about'


urlpatterns = [
    path('delivery/', AboutDeliveryView.as_view(), name='about_delivery'),
    path('payment/', AboutPaymentView.as_view(), name='about_payment'),
    path('me/', AboutAuthorView.as_view(), name='about_me'),
]
