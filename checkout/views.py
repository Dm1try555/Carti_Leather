from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from cart.views import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem, ShippingAddress



import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def get_cities(request):
    url = 'https://api.novaposhta.ua/v2.0/json/'

    payload = {
        "apiKey": 'c4357f4a435f6a68cea55f2c278a434a',
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {}
    }

    response = requests.post(url, json=payload)
    cities_data = response.json().get('data', [])

    cities = [{'name': city['Description'], 'ref': city['Ref']} for city in cities_data]
    return JsonResponse({'cities': cities})



def get_offices(request, city_ref):
    """
    Функция для получения списка отделений Новой Почты по городу.
    """
    # URL для API Новой Почты
    url = 'https://api.novaposhta.ua/v2.0/json/'

    # Параметры запроса для получения списка отделений
    payload = {
        "apiKey": 'c4357f4a435f6a68cea55f2c278a434a',  #API-ключ
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityRef": city_ref  # Код города (ref)
        }
    }

    # Отправляем POST-запрос на API Новой Почты
    response = requests.post(url, json=payload)

    # Извлекаем данные из ответа
    offices_data = response.json().get('data', [])
    offices = [{'name': office['Description'], 'ref': office['Ref']} for office in offices_data]

    return JsonResponse({'offices': offices})


@login_required
def checkout(request):
    """
    Представление чекаута.
    """
    cart = Cart.objects.get(user=request.user)
    form = OrderCreateForm()
    context = {'cart': cart, 'form': form}
    return render(request, 'checkout/checkout.html', context)

@login_required
def thank_you(request, order_id):
    """
    Страница благодарности за заказ.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'checkout/thank_you.html', {'order': order})

@login_required
def create_order(request):
    """
    Создание экземпляров Order и ShippingAddress
    из формы и редирект в профиль пользователя,
    либо передаем форму обратно.
    """
    cart = get_object_or_404(Cart, user=request.user)

    if cart.items.exists() and request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                payment_method=form.cleaned_data['payment_method'],
                user=request.user,
                
            )

            ShippingAddress.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address_line_1=form.cleaned_data['address_line_1'],
                address_line_2=form.cleaned_data['address_line_2'],
                order=order,

            )

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price=cart_item.item.price
                )

            cart.clear()
            return redirect('checkout:thank_you', order_id=order.id)
    else:
        form = OrderCreateForm()
    
    messages.warning(
        request, 'Форма не была корректно обработана, введите данные еще раз')
    context = {'form': form, 'cart': cart}
    return render(request, 'checkout/create_order.html', context)
