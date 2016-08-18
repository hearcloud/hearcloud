from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    url(r'^admin/', admin.site.urls),

    # Applications
    url(r'^', include('applications.home.urls')),
    url(r'^box/', include('applications.box.urls')),
    url(r'^', include('applications.users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include  API urls
urlpatterns += [
    url(r'^api/v1/', include('hearcloud.api_urls', namespace='api_v1')),
]
