from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from products.views import (main_page_view,
                            products_view,
                            products_detail_view,
                            product_create_view,)

from users.views import register_view, auth_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page_view),
    path('products/', products_view),
    path('products/<int:id>/', products_detail_view),
    path('products/create/', product_create_view),
    path('products/create/', products_detail_view),

    path('users/register/', register_view),
    path('users/login/', auth_view),
    path('users/logout/', logout_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
