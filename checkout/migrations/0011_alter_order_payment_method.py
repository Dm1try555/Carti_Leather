# Generated by Django 5.2 on 2025-05-10 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_alter_orderitem_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash_pay', 'По передоплаті онлайн'), ('cash_online', 'Повна оплата онлайн')], max_length=20, verbose_name='Спосіб оплати'),
        ),
    ]
