# Generated by Django 5.2 on 2025-05-17 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0015_order_feedback_messengers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='payment_method',
            field=models.CharField(blank=True, help_text='Вибраний спосіб оплати', verbose_name='Спосіб оплати'),
        ),
        migrations.AlterField(
            model_name='order',
            name='feedback_messengers',
            field=models.CharField(choices=[('empty', 'Немає'), ('telegram', 'Telegram'), ('viber', 'Viber'), ('whatsapp', 'WhatsApp')], max_length=20, verbose_name='Месенджери для звʼязку'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='feedback_messengers',
            field=models.CharField(blank=True, help_text='Вибрані месенджери', verbose_name='Месенджери для звʼязку'),
        ),
    ]
