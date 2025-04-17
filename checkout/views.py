from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import asyncio
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
def create_order(request):
    """
    Створення замовлення та адреси доставки.
    """
    cart = get_object_or_404(Cart, user=request.user)

    if cart.items.exists() and request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                payment_method=form.cleaned_data['payment_method'],
                user=request.user,
            )
            # Отримуємо список месенджерів з форми
            feedback_messengers = form.cleaned_data.get('feedback_messengers', [])

            ShippingAddress.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                city_ref = request.POST.get('city'),
                warehouse_ref = request.POST.get('address_line_1'),
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
            # Формуємо повідомлення
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
                f"🏙️ Місто: {get_city_name_by_ref(address.city_ref)}\n"  # Отримуємо назву міста
                f"📦 Відділення: {address.warehouse_ref}\n"
                f"💳 Оплата: {order.get_payment_method_display()}\n"
                f"🧾 Товари:\n{items_text}\n"
                f"💰 Сума: {order.total_price} грн"
                f"\n\n💬 Месенджери: {', '.join(feedback_messengers) if feedback_messengers else 'Не вказано'}\n"
            )


            # Надсилання в Telegram
            asyncio.run(send_telegram_message(message))
            return redirect('checkout:thank_you', order_id=order.id)
    else:
        form = OrderCreateForm()

    messages.warning(request, 'Форма не була коректно заповнена. Спробуйте ще раз.')
    context = {'form': form, 'cart': cart}
    return render(request, 'checkout/create_order.html', context)



def get_cities(request):
    """
    Отримання списку міст з API Нової Пошти.
    """
    url = 'https://api.novaposhta.ua/v2.0/json/'
    payload = {
        "apiKey": 'c4357f4a435f6a68cea55f2c278a434a',
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {}
    }

    response = requests.post(url, json=payload)
    cities_data = response.json().get('data', [])
    
    # Популярні міста
    popular_cities = ['Київ', 'Львів', 'Одеса', 'Харків', 'Дніпро', 'Запоріжжя', 'Миколаїв']  # Список популярних міст

    # Розділяємо міста на популярні та інші
    popular = [
        {'name': city['Description'], 'ref': city['Ref']}
        for city in cities_data
        if city['Description'] in popular_cities
    ]
    other = [
        {'name': city['Description'], 'ref': city['Ref']}
        for city in cities_data
        if city['Description'] not in popular_cities
    ]
    
    # Повертаємо спочатку популярні міста, потім решту
    cities = popular + other

    return JsonResponse({'cities': cities})


def get_offices(request, city_ref):
    """
    Отримання списку відділень за містом.
    """
    url = 'https://api.novaposhta.ua/v2.0/json/'
    payload = {
        "apiKey": 'c4357f4a435f6a68cea55f2c278a434a',
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityRef": city_ref
        }
    }

    response = requests.post(url, json=payload)
    offices_data = response.json().get('data', [])
    offices = [{'name': office['Description'], 'ref': office['Ref']} for office in offices_data]

    return JsonResponse({'offices': offices})

cities_data = []

def update_cities_data():
    global cities_data
    url = 'https://api.novaposhta.ua/v2.0/json/'
    payload = {
        "apiKey": 'c4357f4a435f6a68cea55f2c278a434a',
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {}
    }
    response = requests.post(url, json=payload)
    cities_data = response.json().get('data', [])

def get_city_name_by_ref(city_ref):
    """
    Отримуємо назву міста за його референсом з кешованих даних.
    """
    if not cities_data:
        update_cities_data()  # Якщо дані не завантажені, оновлюємо їх

    for city in cities_data:
        if city['Ref'] == city_ref:
            return city['Description']  # Повертаємо назву міста
    return "Невідоме місто"  # Якщо місто не знайдено



async def send_telegram_message(message):
    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    chat_id = settings.TELEGRAM_CHAT_ID
    await bot.send_message(chat_id=chat_id, text=message)
