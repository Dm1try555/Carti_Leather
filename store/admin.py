from django.contrib import admin
from .models import Item, ItemTag, ItemImage
from django.utils.text import slugify



# Транслітерація
def custom_slugify(value):
    TRANSLIT_DICT = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ю': 'iu', 'я': 'ia', 'ь': '', 'ъ': '', '’': '', 'ʼ': '',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G',
        'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z',
        'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K',
        'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
        'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
        'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ю': 'Iu', 'Я': 'Ia'
    }
    # Транслітеруємо
    value = ''.join(TRANSLIT_DICT.get(char, char) for char in value)
    # Робимо slug
    value = slugify(value)
    return value


# ItemImageInline
class ItemImageInline(admin.TabularInline): 
    model = ItemImage
    extra = 3  # скільки порожніх форм буде показано
    max_num = 5  # максимум зображень
    fields = ['image']
    verbose_name = 'Додаткове зображення'
    verbose_name_plural = 'Додаткові зображення'


# ItemAdmin
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'slug', 'price',
                    'old_price', 'is_available', 'tag_list',)
    search_fields = ('title', 'description', 'tags__name',)
    list_filter = ('is_available', 'tags',)
    inlines = [ItemImageInline]
    prepopulated_fields = {"slug": ("title",)}  

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = custom_slugify(obj.title)
        super().save_model(request, obj, form, change)

    def short_description(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        else:
            return obj.description

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    short_description.short_description = 'Опис'
    tag_list.short_description = 'Список категорій'


class ItemTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'short_description', 'item_list',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}  


    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = custom_slugify(obj.name)
        super().save_model(request, obj, form, change)

   

    def short_description(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        else:
            return obj.description

    def item_list(self, obj):
        return [Item.objects.get(pk=o.get('object_id')) for o in obj.items.values()]

    short_description.short_description = 'Опис'
    item_list.short_description = 'Список товарів'

    

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemTag, ItemTagAdmin)

