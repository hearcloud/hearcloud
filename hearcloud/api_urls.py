from django.conf.urls import include, url

urlpatterns = [
    # Auth
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/register/', include('rest_auth.registration.urls')),

    # Aplications
    url(r'^', include('applications.box.urls_api')),
]
