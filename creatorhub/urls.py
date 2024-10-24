from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    path('files/', include('file_management.urls')),
    path('trends/', include('trend_analysis.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
