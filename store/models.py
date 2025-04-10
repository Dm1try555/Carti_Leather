from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase


class ItemTag(TagBase):
    image = models.ImageField(
        upload_to='categories/',
        verbose_name='Зображення',
        blank=True
    )
    description = models.TextField(
        blank=True,
        verbose_name='Опис',
        )

    class Meta:
        verbose_name = _("Категорія")
        verbose_name_plural = _("Категорії")


class TaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ItemTag,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name='Категорія',
    )


class Item(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва',)
    description = models.TextField(verbose_name='Опис',)
    slug = models.CharField(
        unique=True,
        max_length=50,
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання',)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Нова ціна',
    )
    old_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Стара ціна',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name='Зображення',
        upload_to='items/',
        blank=True,
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступно',
    )
    tags = TaggableManager(through=TaggedItem, related_name="tagged_items", verbose_name='Категорії',)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-price']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='item_images/',
        verbose_name='Додаткове зображення'
    )

    class Meta:
        verbose_name = 'Додаткове зображення'
        verbose_name_plural = 'Додаткові зображення'

    def __str__(self):
        return f'Зображення для {self.item.title}'