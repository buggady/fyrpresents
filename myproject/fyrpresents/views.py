import logging
from django.shortcuts import render
from django.core.mail import send_mail
from forms import ContactForm
from django.contrib.auth.models import Group, User

# Get an instance of a logger
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'fyrpresents/home.html')

def about(request):
    logger.debug('Something went wrong!')
    return render(request, 'fyrpresents/about.html')

def contact(request):
    form = ContactForm()
    message = ' '

    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            recipients = ['info@fyrpresents.com']

            send_mail(subject, message, email, recipients)
            message = 'You did something right!'
      
    return render(request, 'fyrpresents/contact.html', {'form': form, 'status': message})

def heat_map(request):
   return render(request, 'fyrpresents/heat-map.html')

def register(request):

    g = Group.objects.get(name='General_User')
    u = User.objects.get(username=request.user.username)
    g.user_set.add(u)
    return render(request, 'fyrpresents/home.html')
