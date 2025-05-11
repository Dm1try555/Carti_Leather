from decimal import Decimal
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt



import asyncio
import stripe
from telegram import Bot
from django.conf import settings

import requests
import telegram

from cart.views import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem, ShippingAddress


@login_required
def checkout(request):
    """
    Представлення сторінки оформлення замовлення.
    """
    cart = Cart.objects.get(user=request.user)
    form = OrderCreateForm()
    context = {'cart': cart, 'form': form}
    return render(request, 'checkout/checkout.html', context)


@login_required
def thank_you(request, order_id):
    """
    Сторінка подяки після оформлення замовлення.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'checkout/thank_you.html', {'order': order})

@login_required
def popup(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'checkout/popup.html', {'order': order})


@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)

    if request.method == 'POST' and cart.items.exists():
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                payment_method=form.cleaned_data['payment_method'],
                user=request.user,
            )
            feedback_messengers = request.POST.getlist('feedback_messengers')
            ShippingAddress.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                city=request.POST.get('city'),
                office=request.POST.get('office'),
                order=order,
                feedback_messengers=feedback_messengers,
            )

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price=cart_item.item.price
                )

            cart.clear()

            address = order.shipping_address
            items_text = "\n".join([
                f"{item.quantity} x {item.item.title} — {item.total_price} грн"
                for item in order.items.all()
            ])
            message = (
                f"🛒 НОВЕ ЗАМОВЛЕННЯ #{order.id}\n"
                f"👤 Клієнт: {address.first_name} {address.last_name}\n"
                f"📞 Телефон: {address.phone}\n"
                f"📧 Email: {address.email}\n"
                f"🏙️ Місто: {address.city}\n"
                f"📦 Відділення: {address.office}\n"
                f"💳 Оплата: {order.get_payment_method_display()}\n"
                f"🧾 Товари:\n{items_text}\n"
                f"💰 Сума: {order.total_price} грн"
                f"\n\n💬 Месенджери: {', '.join(feedback_messengers) if feedback_messengers else 'Не вказано'}\n"
            )
            asyncio.run(send_telegram_message(message))
            return redirect('checkout:popup', order_id=order.id)
    else:
        form = OrderCreateForm()  # <-- ЦЕ ВАЖЛИВО! Створення форми для GET-запиту

    messages.warning(request, 'Форма не була коректно заповнена. Спробуйте ще раз.')
    context = {'form': form, 'cart': cart}
    return render(request, 'checkout/popup.html', context)


async def send_telegram_message(message):
    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    chat_id = settings.TELEGRAM_CHAT_ID
    await bot.send_message(chat_id=chat_id, text=message)


# def fake_payment(request):
#     if request.method == 'POST':
#         order = Order.objects.create(
#             user=request.user,
#             total_price=500,  # Введіть суму
#             payment_status='Paid'
#         )
#         messages.success(request, 'Оплата успішна!')
#         return redirect('checkout:thank_you', order_id=order.id)
#     return render(request, 'checkout/thank_you.html')


# stripe.api_key = settings.STRIPE_SECRET_KEY
# stripe.api_version = settings.STRIPE_API_VERSION


# def payment_process(request):
#     order_id = request.session.get('order_id', None)
#     order = get_object_or_404(Order, id=order_id)
    
#     if request.method == 'POST':
#         success_url = request.build_absolute_uri(
#             reverse('checkout:thank_you')
#         )
#         cancel_url = request.build_absolute_uri(
#             reverse('payment:popup')
#         )
#         session_data = {
#             'mode': 'payment',
#             'client_reference_id': order.id,
#             'success_url': success_url,
#             'cancel_url': cancel_url,
#             'line_items': []
#         }
#         for item in order.items.all():
#             discounted_price = item.product.sell_price()
#             session_data['line_items'].append({
#                 'price_data': {
#                     'unit_amount': int(discounted_price * Decimal('100')),
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': item.product.name,
#                     },
#                 },
#                 'quantity': item.quantity,
#             })
#         session = stripe.checkout.Session.create(**session_data)
#         return redirect(session.url, code=303)
#     else:
#         return render(request, 'payment/process.html', locals())
    

# def payment_completed(request):
#     return render(request, 'payment/completed.html')


# def payment_canceled(request):
#     return render(request, 'payment/canceled.html')



# def cities(request):
#     query = request.GET.get('q', '').strip()
#     print(f"Отримано запит: {query}")

#     if not query:
#         return JsonResponse({'cities': []})

#     url = "https://api.novaposhta.ua/v2.0/json/"
#     payload = {
#         "apiKey": settings.NOVAPOSHTA_API_KEY,
#         "modelName": "Address",
#         "calledMethod": "getCities",
#         "methodProperties": {
#             "FindByString": query
#         }
#     }

#     try:
#         response = requests.post(url, json=payload, timeout=5)  # <- Додано timeout
#         response.raise_for_status()
#         cities = []
#         data = response.json()
#         if data.get('success'):
#             cities = [
#                 {'name': city['Description'], 'ref': city['Ref']}
#                 for city in data['data']
#             ]
#         else:
#             print(f"Помилка API: {data.get('errors', 'невідомі помилки')}")
#     except requests.exceptions.ReadTimeout:
#         print("⏱️ Таймаут при зверненні до API Нової Пошти.")
#         cities = []
#     except requests.RequestException as e:
#         print(f"❌ Помилка під час запиту до API: {e}")
#         cities = []

#     return JsonResponse({'cities': cities})



# def get_offices(request, city_ref):
#     url = 'https://api.novaposhta.ua/v2.0/json/'
#     payload = {
#         "apiKey": settings.NOVAPOSHTA_API_KEY,
#         "modelName": "Address",
#         "calledMethod": "getWarehouses",
#         "methodProperties": {
#             "CityRef": city_ref
#         }
#     }

#     try:
#         response = requests.post(url, json=payload, timeout=5)  # <- Додано timeout
#         response.raise_for_status()
#         offices_data = response.json().get('data', [])
#         offices = [{'name': office['Description'], 'ref': office['Ref']} for office in offices_data]
#     except requests.exceptions.ReadTimeout:
#         print("⏱️ Таймаут при отриманні відділень.")
#         offices = []
#     except requests.RequestException as e:
#         print(f"❌ Помилка при отриманні відділень: {e}")
#         offices = []

#     return JsonResponse({'offices': offices})


# cities_data = []

# def update_cities_data():
#     global cities_data
#     url = 'https://api.novaposhta.ua/v2.0/json/'
#     payload = {
#         "apiKey": settings.NOVAPOSHTA_API_KEY,
#         "modelName": "Address",
#         "calledMethod": "getCities",
#         "methodProperties": {}
#     }
#     response = requests.post(url, json=payload)
#     cities_data = response.json().get('data', [])

# def get_city_name_by_ref(ref):
#     # приклад виклику до API Нової пошти
#     response = requests.post("https://api.novaposhta.ua/v2.0/json/", json={
#         "apiKey": settings.NOVAPOSHTA_API_KEY,
#         "modelName": "Address",
#         "calledMethod": "getCities",
#         "methodProperties": {
#             "Ref": ref
#         }
#     })
#     data = response.json()
#     return data['data'][0]['Description'] if data.get('data') else 'Невідомо'


