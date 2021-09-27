from django.urls import include, path
from django.conf.urls import url, include
from django.contrib import admin


api_urls = [

    path('', include('v2apps.accounts.urls')),
    path('', include('v2apps.departments.urls')),
    path('', include('v2apps.posts.urls')),
]

urlpatterns = [
    path('cconnect-admin/', admin.site.urls),
    path('api/', include(api_urls)),
    url('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
