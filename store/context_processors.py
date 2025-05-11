from .models import ItemTag

def category_dropdown(request):
    return {
        'tags': ItemTag.objects.all()
    }
