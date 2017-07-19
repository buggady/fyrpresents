from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$', views.home, name='index'),
	url(r'^home', views.home, name='home'),
	url(r'^contact', views.contact, name='contact'),
	url(r'^about', views.about, name='about'),
	url(r'^heat-map', views.heat_map, name='heat_map'),
	url(r'^register', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
