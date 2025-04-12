from django.contrib.auth.models import User
from django.db import models
import requests
from django.conf import settings
from store.models import Item


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash_courier', 'Наличными курьеру'),
        ('card_courier', 'Картой курьеру'),
        ('card_online', 'Картой онлайн'),
    ]
    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('processing', 'Обрабатывается'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    ]
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Покупатель',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус',
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    @property
    def total_price(self):
        total_price = sum(
            order_item.total_price for order_item in self.items.all())
        return total_price

    def __str__(self):
        return f"Заказ номер {self.id} для {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ',
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name='Товар',)
    quantity = models.PositiveIntegerField(
        default=1, verbose_name='Количество',)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена',)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    @property
    def total_price(self):
        total_price = self.quantity * self.item.price
        return total_price

    def __str__(self):
        return f"{self.quantity} x {self.item.title} in Order {self.order.id}"


class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя',)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия',)
    email = models.EmailField(verbose_name='Почта',)
    phone = models.CharField(max_length=20, verbose_name='Телефон',)
    address_line_1 = models.CharField(max_length=200, verbose_name='Адрес',)
    address_line_2 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Адрес (дополнительно)',)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='shipping_address', verbose_name='Заказ',)

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return f"""
        {self.address_line_1} {self.address_line_2}
        {self.first_name} {self.last_name} {self.phone} {self.email}
        """
    

API_KEY = "c4357f4a435f6a68cea55f2c278a434a"


class NovaPoshtaAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "https://api.novaposhta.ua/v2.0/json/"

    def get_cities(self):
        """Получение списка городов."""
        url = f"{self.base_url}address/generalCities"
        payload = {
            "apiKey": self.api_key,
            "modelName": "Address",
            "calledMethod": "getCities",
            "methodProperties": {}
        }
        response = requests.post(url, json=payload)
        return response.json()

    def get_offices(self, city_name):
        """Получение списка отделений по названию города."""
        url = f"{self.base_url}address/getWarehouses"
        payload = {
            "apiKey": self.api_key,
            "modelName": "Address",
            "calledMethod": "getWarehouses",
            "methodProperties": {"CityName": city_name}
        }
        response = requests.post(url, json=payload)
        return response.json()