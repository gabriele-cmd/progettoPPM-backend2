from django.contrib import admin
from django.urls import path, include
from products.views import index_view

urlpatterns = [
    path('', index_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/users/', include('users.urls')),
]
