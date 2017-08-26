from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import FormView, View, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from users.models import UserProfile
from schedule.models import Event
from address.models import Address
from events.models import EventUserRel, EventProfile, EventIdeas
from forms import DonatePhotosForm, SubmitEventIdeaForm, SubmitPastEventForm
from fyrpresents.forms import EnterAddressForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
import os, os.path
from django.utils import timezone
import datetime
from django.conf import settings
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
    template_name = 'events/events-overview.html'

    def get_queryset(self):
        return Event.objects.filter(end__gte=datetime.date.today()).order_by("end")

    def get_context_data(self, **kwargs):
        context = super(EventsOverviewView, self).get_context_data(**kwargs)

        context['past_events_list'] = Event.objects.filter(end__lte=datetime.date.today()).order_by("title")
        context['event_ideas_list'] = EventIdeas.objects.all()
        return context

    @method_decorator(permission_required('users.fyr_member', login_url='/accounts/login'))
    def dispatch(self, *args, **kwargs):
       return super(EventsOverviewView, self).dispatch(*args, **kwargs)

class PastEventsListView(ListView):
    template_name = 'events/past-events-list.html'

    def get_queryset(self):
        return Event.objects.filter(end__lte=datetime.date.today()).order_by("title")

    @method_decorator(login_required)
    @method_decorator(permission_required('users.fyr_member', raise_exception=True))
    def dispatch(self, *args, **kwargs):
       return super(PastEventsListView, self).dispatch(*args, **kwargs)

#Sets up the object detail view
class EventDisplay(DetailView):
    model = EventProfile

    template_name='events/event-details.html'

    def get_context_data(self, **kwargs):
        context = super(EventDisplay, self).get_context_data(**kwargs)
        tmp_user = get_object_or_404(User, username=self.request.user.username)
        tmp_event_profile = self.get_object()
        
        context['form'] = EnterAddressForm()

        try:
            token = SocialToken.objects.filter(account__user=tmp_user, account__provider='facebook')
            graph = facebook_sdk.GraphAPI(access_token=token, version='2.7')
            tmp_event_id = str(tmp_event_profile.facebook_event_id)
            facebook_data = graph.get_object(id=tmp_event_id)
            context['facebook_data'] = facebook_data
            context['fb_description'] = facebook_data['description']
            context['fb_photos'] = graph.get_connections(id=tmp_event_id, connection_name='photos', fields='link')
            context['fb_guest_list'] = graph.get_connections(id=tmp_event_id, connection_name='attending', fields='id, picture', limit='100')
        except:
            context['fb_description'] = 'Problem retrieving facebook info'
            context['fb_photos'] = 'Problem retrieving photos'

        if EventUserRel.objects.filter(user=tmp_user, event=tmp_event_profile.event).exists():
            context['rsvp_button_value'] = 'Remove Me'
            context['is_current_user_registered'] = True
        else:
            context['rsvp_button_value'] = 'Add Me'
            context['is_current_user_registered'] = False
        
        return context

#Create form view that also takes in an object from the Mixin
class EventAddress(SingleObjectMixin, FormView):
    template_name = 'events/event-details.html'
    form_class = EnterAddressForm
    model = EventProfile
    message = ' '

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            pre_address = form.cleaned_data['address']
            tmp_address = Address.to_python(pre_address)
            #Refactor this one day, there is bug in django address that creates two addresses for no reason
            address_set = Address.objects.filter(raw=tmp_address)
            for address in address_set:
                if Address.objects.filter(raw=tmp_address).count() > 1:
                    #if not EventProfile.objects.filter(address__id=address.id):
                    Address.objects.get(id=address.id).delete()
                else:
                    if request.user.groups.filter(name="Developers").exists():
                        self.object.address = Address.objects.get(id=address.id)
                        self.object.save()
                        message = "You are an admin so address saved successfully"
                        pass
                    else:
                        #Send us an email if you don't have approval
                        name = 'tim'
                        email = 'info@fyrpresents.com'
                        subject = 'Possible address for event'
                        email_body = 'address' + " added"
                        recipients = ['info@fyrpresents.com']
                        send_mail(subject, email_body, email, recipients)
                        message = "Sent email to website admin"

        return super(EventAddress, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('event_details', kwargs={'slug': self.object.slug, 'status': message})

#Class shows ability to display both form and details of an object with 3 above classes
class EventDetailsView(View):

    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventAddress.as_view()
        return view(request, *args, **kwargs)

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
        try:
            token = SocialToken.objects.filter(account__user=tmp_user, account__provider='facebook')
            graph = facebook_sdk.GraphAPI(access_token=token, version='2.7')
            tmp_event_id = str(tmp_event_profile.facebook_event_id)
            facebook_data = graph.get_object(id=tmp_event_id)
            context['facebook_data'] = facebook_data
            context['fb_description'] = facebook_data['description']
            context['fb_photos'] = graph.get_connections(id=tmp_event_id, connection_name='photos', fields='link, picture')
            context['fb_guest_list'] = graph.get_connections(id=tmp_event_id, connection_name='attending', fields='link, picture.height(140).width(140), name', limit='100')
            context['fb_feed'] = graph.get_connections(id=tmp_event_id, connection_name='feed', fields='id, from, created_time, message, picture, link, type, description, object_id', date_format="U", limit='100')
        except:
            context['fb_description'] = 'Problem retrieving facebook info'
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