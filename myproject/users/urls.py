from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from users import views

urlpatterns = [
	url(r'^$', views.UserEventsListView.as_view(), name='userprofile'),
	url(r'^edit-profile', views.edit_profile, name='edit_profile'),
	url(r'^(?P<slug>[\w-]+)$', views.UserEventsDetailsView.as_view(), name='user_event_details'),
]