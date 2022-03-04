from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

handler404 = 'Handlers.views.handler404'
handler500 = 'Handlers.views.handler500'

urlpatterns = [
    path('', include('website.urls')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
