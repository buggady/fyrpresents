from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from schedule.models import Event
from events.models import Event, EventUserRel
from users.models import UserProfile
from django.views import generic
from datetime import date
from users.forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.utils.decorators import method_decorator

import facebook_sdk
from allauth.socialaccount.models import SocialToken

class UserEventsListView(generic.ListView):
    template_name = 'users/profile.html'

    def get_queryset(self):
        try:
            tmp_user_rel = EventUserRel.objects.filter(user=self.request.user)
            events_attended = Event.objects.filter(id__in=tmp_user_rel.values('event_id'))
        except:
            events_attended = Event.objects.none()
        
        return events_attended

    @method_decorator(permission_required('users.fyr_member', login_url='/home'))
    def dispatch(self, *args, **kwargs):     
        return super(UserEventsListView, self).dispatch(*args, **kwargs)

class UserEventsDetailsView(generic.DetailView):
    model = EventUserRel

    template_name = 'users/usereventsdetails.html'

    @method_decorator(permission_required('users.fyr_member', login_url='/home'))
    def dispatch(self, *args, **kwargs):
        return super(UserEventsDetailsView, self).dispatch(*args, **kwargs)

@login_required
@transaction.atomic
def edit_profile(request):
    message = ' '

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)  
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            message = 'You did something right!'
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
      
    return render(request, 'users/editprofile.html', {'user_form': user_form, 'profile_form': profile_form, 'status': message})