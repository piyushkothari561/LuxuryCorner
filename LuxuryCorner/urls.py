
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from LuxuryCorner import settings

from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
