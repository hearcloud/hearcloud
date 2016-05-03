from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('home.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^box/', include('box.urls')),
    url(r'^', include('users.urls')),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include  API urls
urlpatterns += [
    url(r'^api/', include('hearcloud.apiurls', namespace='api')),
]
