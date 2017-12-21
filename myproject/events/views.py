from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import View, DetailView, ListView
from django.contrib.auth.models import User
from users.models import UserProfile
from schedule.models import Event
from events.models import EventUserRel, EventProfile, EventIdeas
from forms import DonatePhotosForm, SubmitEventIdeaForm, SubmitPastEventForm
from django.core.mail import send_mail
from django.utils import timezone
import datetime
import facebook_sdk
from allauth.socialaccount.models import SocialToken
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST

class EventsOverviewView(ListView):
    template_name = 'events/overview.html'

    def get_queryset(self):
        return Event.objects.filter(end__gte=datetime.date.today()).order_by("end")

    def get_context_data(self, **kwargs):
        context = super(EventsOverviewView, self).get_context_data(**kwargs)

        context['past_events_list'] = Event.objects.filter(end__lte=datetime.date.today()).order_by("title")
        context['event_ideas_list'] = EventIdeas.objects.all()
        return context

    def dispatch(self, *args, **kwargs):
       return super(EventsOverviewView, self).dispatch(*args, **kwargs)

class PastEventsListView(ListView):
    template_name = 'events/past-events-list.html'

    def get_queryset(self):
        return Event.objects.filter(end__lte=datetime.date.today()).order_by("title")

    def dispatch(self, *args, **kwargs):
       return super(PastEventsListView, self).dispatch(*args, **kwargs)

class EventDetailsView(DetailView):
    model = EventProfile

    template_name='events/event-details.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetailsView, self).get_context_data(**kwargs)
        tmp_user = get_object_or_404(User, username=self.request.user.username)
        tmp_event_profile = self.get_object()
        
        if EventUserRel.objects.filter(user=tmp_user, event=tmp_event_profile.event).exists():
            context['rsvp_button_value'] = 'Remove Me'
            context['is_current_user_registered'] = True
        else:
            context['rsvp_button_value'] = 'Add Me'
            context['is_current_user_registered'] = False
        
        return context

    @method_decorator(login_required)
    @method_decorator(permission_required('users.fyr_member', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(EventDetailsView, self).dispatch(*args, **kwargs)


class PastEventDetailsView(DetailView):
    model = EventProfile

    template_name='events/past-event-details.html'

    def get_context_data(self, **kwargs):
        context = super(PastEventDetailsView, self).get_context_data(**kwargs)
        tmp_user = get_object_or_404(User, username=self.request.user.username)
        tmp_event_profile = self.get_object()
        if EventUserRel.objects.filter(user=tmp_user, event=tmp_event_profile.event).exists():
            context['rsvp_button_value'] = 'Remove Me'
            context['is_current_user_registered'] = True
        else:
            context['rsvp_button_value'] = 'Add Me'
            context['is_current_user_registered'] = False
        
        return context

    @method_decorator(login_required)
    #@method_decorator(permission_required('users.fyr_member', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(PastEventDetailsView, self).dispatch(*args, **kwargs)

def eventDetailsRedirect(request, pk):
    tmp_event = Event.objects.get(pk=pk)  
    if tmp_event.end < timezone.now():
        return HttpResponseRedirect(reverse('past_event_details', kwargs={'slug': tmp_event.profile.slug}))
    else:
        return HttpResponseRedirect(reverse('event_details', kwargs={'slug': tmp_event.profile.slug}))

class EventIdeaDetailsView(DetailView):
    model = EventIdeas
    template_name = 'events/event-idea-details.html'

    def get_context_data(self, **kwargs):
        context = super(EventIdeaDetailsView, self).get_context_data(**kwargs)
        tmp_user = get_object_or_404(User, username=self.request.user.username)
        tmp_event_idea = self.get_object()
        if tmp_event_idea.slug == 'raver-paradise-2017':
            context['sub_event_ideas'] = EventIdeas.objects.filter(sub_event_idea=True)
        context['is_current_user_interested'] = tmp_event_idea.votes.exists(tmp_user.id)
        context['interested_users'] = User.objects.filter(id__in=tmp_event_idea.votes.user_ids().values('id'))
        return context

    @method_decorator(login_required)
    @method_decorator(permission_required('users.fyr_member', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(EventIdeaDetailsView, self).dispatch(*args, **kwargs)

@login_required
@require_POST
def interested(request):
    if request.method == 'POST':
        tmp_user = request.user
        slug = request.POST.get('slug', None)
        tmp_event_idea = get_object_or_404(EventIdeas, slug=slug)

        if tmp_event_idea.votes.exists(tmp_user.id):
            tmp_event_idea.votes.delete(tmp_user.id)
            message = 'You interest has been removed'
        else:
            tmp_event_idea.votes.up(tmp_user.id)
            message = 'Your interest has been counted'

    ctx = {'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')     

@login_required
@require_POST
def rsvp(request):
    if request.method == 'POST':
        tmp_user = request.user
        slug = request.POST.get('slug', None)
        tmp_event_profile = get_object_or_404(EventProfile, slug=slug)

        if not EventUserRel.objects.filter(user=tmp_user, event=tmp_event_profile.event).exists():
            tmp_user_event = EventUserRel(user=tmp_user, event=tmp_event_profile.event)
            message = 'You signed up for this event'
            tmp_user_event.save()
        else:
            tmp_user_event = EventUserRel.objects.get(user=tmp_user, event=tmp_event_profile.event)
            message = 'You are removed from this event'
            tmp_user_event.delete()

    ctx = {'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')

@login_required
@permission_required('users.fyr_developer', raise_exception=True)
def donate_photos(request):
    
    message = ''

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DonatePhotosForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.user.username
            email = 'info@fyrpresents.com'
            subject = 'Event Idea'
            email_body = form.cleaned_data['facebook_album_id'] + '-' + form.cleaned_data['description'] 

            recipients = ['info@fyrpresents.com']

            send_mail(subject, email_body, email, recipients)
            message = "Woah, this thing actually works!"
    else:
        form = DonatePhotosForm()
      
    return render(request, 'events/donate-photos.html', {'form': form, 'status': message})

@login_required
@permission_required('users.fyr_member', raise_exception=True)
def submit_event_idea(request):
    
    message = ''

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmitEventIdeaForm(request.POST)
        if form.is_valid():
            name = request.user.username
            email = 'info@fyrpresents.com'
            subject = 'Event Idea: ' + form.cleaned_data['title']
            email_body = ' description: ' + form.cleaned_data['description'] + ' username: ' + name + ' user email: ' + request.user.email

            recipients = ['info@fyrpresents.com']

            send_mail(subject, email_body, email, recipients)
            message = "Woah, this thing actually works!"

            return HttpResponseRedirect(reverse('events'))
        else:
            message = "Uh Oh, we messed up somewhere"
            
    else:
        form = SubmitEventIdeaForm()
 
    return render(request, 'events/submit-event-idea.html', {'form': form, 'status': message})

@login_required
@permission_required('users.fyr_member', raise_exception=True)
def submit_past_event(request):
    
    message = ''

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmitPastEventForm(request.POST)
        if form.is_valid():
            name = 'test1'
            email = 'info@fyrpresents.com'
            subject = 'Event Idea'
            email_body = form.cleaned_data['title']

            recipients = ['info@fyrpresents.com']

            send_mail(subject, email_body, email, recipients)
            message = "Woah, this thing actually works!"
        else:
            message = "Uh Oh, we messed up somewhere"
            
    else:
        form = SubmitPastEventForm()

    return render(request, 'events/submit-past-event.html', {'form': form, 'status': message})