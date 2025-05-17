from django.contrib.auth.models import User
from django.db import models
from store.models import Item


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash_pay', 'По передоплаті онлайн'),
        ('cash_online', 'Повна оплата онлайн'),
    ]
    FEEDBACK_MESSENGER_CHOICES = [
        ('empty', 'Немає'),
        ('telegram', 'Telegram'),
        ('viber', 'Viber'),
        ('whatsapp', 'WhatsApp'),
    ]
    STATUS_CHOICES = [
        ('created', 'Створений'),
        ('processing', 'У процесі'),
        ('shipped', 'Відправлений'),
        ('delivered', 'Доставлений'),
        ('canceled', 'Відмінений'),
    ]
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Спосіб оплати',
    )
    feedback_messengers = models.CharField(
        max_length=20,
        choices=FEEDBACK_MESSENGER_CHOICES,
        verbose_name='Месенджери для звʼязку',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Покупець',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус',
    )

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    @property
    def total_price(self):
        total_price = sum(
            order_item.total_price for order_item in self.items.all())
        return total_price

    def __str__(self):
        return f"Замовлення номер {self.id} для {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Замовлення',
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name='Товар',)
    quantity = models.PositiveIntegerField(
        default=1, verbose_name='Кількість',)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Ціна',)

    class Meta:
        verbose_name = 'Товар в замовленні'
        verbose_name_plural = 'Товари в замовленні'

    @property
    def total_price(self):
        total_price = self.quantity * self.item.price
        return total_price

    def __str__(self):
        return f"{self.quantity} x {self.item.title} in Order {self.order.id}"

class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    email = models.EmailField(verbose_name='Почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    city = models.CharField(max_length=255, verbose_name='Місто')
    office = models.CharField(max_length=100, verbose_name='Відділення')
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='shipping_address',
        verbose_name='Замовлення'
    )
    feedback_messengers = models.CharField(
        verbose_name='Месенджери для звʼязку',
        blank=True,
        help_text='Вибрані месенджери'
    )
    payment_method = models.CharField(
        verbose_name='Спосіб оплати',
        blank=True,
        help_text='Вибраний спосіб оплати'
    )

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return f"{self.city} | Відділення НП: №{self.office} | {self.first_name} {self.last_name} | {self.phone} | {self.email}"

    

