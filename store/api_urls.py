from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, ItemTagViewSet, ItemImageViewSet

router = DefaultRouter()
router.register('items', ItemViewSet)
router.register('tags', ItemTagViewSet)
router.register('images', ItemImageViewSet)




urlpatterns = router.urls
