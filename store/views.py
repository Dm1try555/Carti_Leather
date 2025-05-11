from django.shortcuts import get_object_or_404, render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Item, ItemTag, ItemImage
from .paginator import paginator
from .serializers import ItemSerializer, ItemImageSerializer, ItemTagSerializer



def store(request):
    items = Item.objects.filter(is_available=True)
    context = {
        'page_obj': paginator(request, items, 9),
        'range': [*range(1, 7)],  # For random css styles
    }

    return render(request, 'store/main_page.html', context)
    


def item_details(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    context = {
        'item': item,
    }
    return render(request, 'store/item_details.html', context)



def tag_details(request, slug):
    tag = get_object_or_404(ItemTag, slug=slug)
    items = Item.objects.filter(tags__in=[tag])
    context = {
        'tag': tag,
        'page_obj': paginator(request, items, 3),
    }
    return render(request, 'store/tag_details.html', context)


def tag_list(request):
    tags = ItemTag.objects.all()
    context = {
        'page_obj': paginator(request, tags, 8),
    }
    return render(request, 'store/tag_list.html', context)


# Представление для товаров
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=True, methods=['get'])
    def tags(self, request, pk=None):
        item = self.get_object()
        tags = item.tags.all()
        serializer = ItemTagSerializer(tags, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        item = self.get_object()
        images = item.images.all()
        serializer = ItemImageSerializer(images, many=True)
        return Response(serializer.data)

# Представление для категорий
class ItemTagViewSet(viewsets.ModelViewSet):
    queryset = ItemTag.objects.all()
    serializer_class = ItemTagSerializer
    

# Представление для изображений товаров
class ItemImageViewSet(viewsets.ModelViewSet):
    queryset = ItemImage.objects.all()
    serializer_class = ItemImageSerializer

    