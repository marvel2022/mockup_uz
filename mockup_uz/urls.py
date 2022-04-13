from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('mockup.uz/admin/page/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),

    path('', include('core.urls', namespace="core")),
    path('product/', include('product.urls', namespace="product")),
    path('accounts/', include('users.urls', namespace='users')),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
