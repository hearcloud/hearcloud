from django.conf.urls import url
from . import views

# to make namespaces reference only this app (this way we can have 
# the same name in different apps)
app_name = 'home'

urlpatterns = [
    # /
    url(r'^$', views.IndexView.as_view(), name='index'),
]
