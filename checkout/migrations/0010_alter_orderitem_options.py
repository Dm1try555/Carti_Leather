# Generated by Django 5.2 on 2025-05-10 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_remove_shippingaddress_city_ref_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Товар в замовленні', 'verbose_name_plural': 'Товари в замовленні'},
        ),
    ]
