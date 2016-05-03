from .                      import views
from django.conf.urls       import url, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'productImage', views.ProductImagesViewset)
router.register(r'category', views.CategoryViewset)
router.register(r'user', views.UserViewset)
router.register(r'shoppingCartProduct', views.ShoppingCartProductViewset)
router.register(r'order', views.OrderViewSet)
router.register(r'adress', views.AdressViewSet)
router.register(r'tag', views.TaggitViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.HomeView, name='home'),
    url(r'^about/$', views.AboutView, name='about'),
    url(r'^productos/$', views.CategoryListView, name='categories'),
    url(r'^productos/(?P<category_name>[\w-]+)/$', views.ProductsListView, name='products'),
    url(r'^productos/(?P<category_name>[\w-]+)/(?P<product_name>[\w-]+)/(?P<variant_name>[\w-]+)/$', views.ProductsSingleView, name='product'),
    url(r'^colabs/$', views.CategoryListView, name='colabs'),
    url(r'^prensa/$', views.PressListView, name='press'),
    url(r'^prensa/(?P<press_name>[\w-]+)/$$', views.PressSingleView, name='press_single'),
    url(r'^contact/$', views.ContactView, name='contact'),
]
