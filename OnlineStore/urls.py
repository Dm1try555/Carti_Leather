from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Carti_Leather",
      default_version='v1',
      description="Документация для API товаров, категорий и изображений",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('cart/', include('cart.urls')),
   path('about/', include('about.urls')),
   path('checkout/', include('checkout.urls')),
   path('users/', include('users.urls')),
   
   path('api/', include('store.api_urls')),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
   




   path('', include('store.urls')),
   path('', include('django.contrib.auth.urls')), 

]



if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
