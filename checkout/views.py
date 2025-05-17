from decimal import Decimal
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt



import asyncio
from asgiref.sync import async_to_sync

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
    cart = get_object_or_404(Cart, user=request.user)

    if request.method == 'POST' and cart.items.exists():
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                payment_method=form.cleaned_data['payment_method'],
                feedback_messengers=form.cleaned_data['feedback_messengers'],
                user=request.user,
            )
            ShippingAddress.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                city=form.cleaned_data['city'],
                office=form.cleaned_data['office'],
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
                f"\n\n💬 Месенджери: {order.get_feedback_messengers_display()}\n"
            )
            async_to_sync(send_telegram_message)(message)
            return redirect('checkout:thank_you', order_id=order.id)
    else:
        form = OrderCreateForm()  # <-- ЦЕ ВАЖЛИВО! Створення форми для GET-запиту
        return render(request, 'checkout/checkout.html', {'form': form, 'cart': cart})

    if request.method == 'POST':
        messages.warning(request, 'Форма не була коректно заповнена. Спробуйте ще раз.')
    context = {'form': form, 'cart': cart}
    return render(request, 'checkout/checkout.html', context)


async def send_telegram_message(message):    
    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    chat_id = settings.TELEGRAM_CHAT_ID
    await bot.send_message(chat_id=chat_id, text=message)


