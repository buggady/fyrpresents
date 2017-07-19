from __future__ import absolute_import

from django import template
from django.contrib.auth.models import User
from events.models import EventUserRel
from schedule.models import Event
from vote.models import UP

register = template.Library()

@register.assignment_tag(takes_context=True)
def rsvp_event(context, event, action=UP):
    try:
        request = context['request']
        tmp_user = User.objects.get(username=request.user.username)
        tmp_event = Event.objects.get(id=event.id)
        return EventUserRel.objects.filter(user=tmp_user, event=tmp_event).exists()
    except Exception as e:
        return False
