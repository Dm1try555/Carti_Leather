import asyncio
import logging

import telegram
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings

from OnlineStore.settings import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
from checkout.models import Order
from .forms import CreationForm, FeedbackForm
from .models import Feedback

logger = logging.getLogger(__name__)


@login_required
def user_orders(request):
    """
    Представление списка заказов пользователя.
    """
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'users/user_orders.html', context)


@login_required
def profile(request):
    """
    Представление профиля пользователя.
    """
    return render(request, 'users/profile.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('store:home')
    template_name = 'users/signup.html'


async def send_telegram_message(message):
    """
    Асинхронная функция для отправки сообщения в ТГ.
    """
    bot = telegram.Bot(token='7919397747:AAHPLsnAXhM68PitKNER9bpZuzS0xK-l_S4')
    chat_id = '549353219'
    await bot.send_message(chat_id=chat_id, text=message)


def feedback_processing(request):
    """
    Представление приема и обработки для обратной связи.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback(
                feedback_name=form.cleaned_data['feedback_name'],
                feedback_email=form.cleaned_data['feedback_email'],
                feedback_message=form.cleaned_data['feedback_message'],
                feedback_phone=form.cleaned_data['feedback_phone'],
            )
            feedback.save()

            # Отпрака сообщения
            message = f"Новое сообщение от {feedback.feedback_name} ({feedback.feedback_email}): \nСообщение: {feedback.feedback_message} \nТелефон: {feedback.feedback_phone}"
            asyncio.run(send_telegram_message(message))

            return render(request, 'users/feedback_success.html')
    return render(request, 'users/feedback_failed.html')
