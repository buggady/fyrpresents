from django.conf.urls import url, include
from django.views.generic import View, ListView, DetailView
from events import views as events_views

urlpatterns = [
	url(r'^$', events_views.EventsOverviewView.as_view(), name='events'),
	url(r'^submit-event-idea', events_views.submit_event_idea, name='submit_event_idea'),
	url(r'^submit-past-event', events_views.submit_past_event, name='submit_past_event'),
	url(r'^past-events-list', events_views.PastEventsListView.as_view(), name='past_events_list'),
	url(r'^(?P<pk>[0-9]+)/$', events_views.eventDetailsRedirect, name='event_details_pk'),
	url(r'^(?P<slug>[\w-]+)/$', events_views.EventDetailsView.as_view(), name='event_details'),
	url(r'^(?P<slug>[\w-]+)/past-event-details', events_views.PastEventDetailsView.as_view(), name='past_event_details'),
	url(r'^(?P<slug>[\w-]+)/event-idea-details', events_views.EventIdeaDetailsView.as_view(), name='event_idea_details'),
	url(r'^rsvp', events_views.rsvp, name='rsvp_to_event'),
	url(r'^interested', events_views.interested, name='interested'),
	url(r'^(?P<slug>[\w-]+)/donate-photos', events_views.donate_photos, name='donate_photos'),
]
