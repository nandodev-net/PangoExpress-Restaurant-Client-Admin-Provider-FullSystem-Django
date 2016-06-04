
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^', include('menu.urls')),
	url(r'^menu/', include('menu.urls')),
	url(r'^admin/', admin.site.urls),
]
