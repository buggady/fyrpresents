from __future__ import absolute_import

from django import template
from django.contrib.auth.models import User
from events.models import EventIdeas
from vote.models import UP

register = template.Library()

@register.assignment_tag(takes_context=True)
def vote_idea(context, eventidea, action=UP):
    try:
        request = context['request']
        tmp_user = User.objects.get(username=request.user.username)
        tmp_event_idea = EventIdeas.objects.get(slug=eventidea.slug)
    	return tmp_event_idea.votes.exists(tmp_user.id)
    except Exception as e:
        return False
