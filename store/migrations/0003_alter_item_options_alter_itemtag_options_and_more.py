# Generated by Django 5.2 on 2025-04-10 20:17

import django.db.models.deletion
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_taggeditem_content_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-price'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товари'},
        ),
        migrations.AlterModelOptions(
            name='itemtag',
            options={'verbose_name': 'Категорія', 'verbose_name_plural': 'Категорії'},
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(verbose_name='Опис'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, upload_to='items/', verbose_name='Зображення'),
        ),
        migrations.AlterField(
            model_name='item',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Стара ціна'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Нова ціна'),
        ),
        migrations.AlterField(
            model_name='item',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання'),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='store.TaggedItem', to='store.ItemTag', verbose_name='Категорії'),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Назва'),
        ),
        migrations.AlterField(
            model_name='itemtag',
            name='description',
            field=models.TextField(blank=True, verbose_name='Опис'),
        ),
        migrations.AlterField(
            model_name='itemtag',
            name='image',
            field=models.ImageField(blank=True, upload_to='categories/', verbose_name='Зображення'),
        ),
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.itemtag', verbose_name='Категорія'),
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='item_images/', verbose_name='Додаткове зображення')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.item', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Додаткове зображення',
                'verbose_name_plural': 'Додаткові зображення',
            },
        ),
    ]
