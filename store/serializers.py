
from rest_framework import serializers
from taggit.models import Tag
from .models import Item, ItemImage, ItemTag

# Сериализатор для тега
class ItemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTag
        fields = '__all__'

# Сериализатор для товара
class ItemSerializer(serializers.ModelSerializer):
    tags = ItemTagSerializer(many=True, read_only=True)  # Теги товара

    class Meta:
        model = Item
        fields = '__all__'

# Сериализатор для изображения товара
class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = '__all__'
