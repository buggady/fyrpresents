from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField
from django.utils import timezone
import datetime
from schedule.models import Event
from taggit.managers import TaggableManager
from photologue.models import Gallery
from vote.models import VoteModel
from django.core.urlresolvers import reverse

class EventProfile(models.Model):

    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('vacation', 'Vacation'), #a64d79
        ('festival', 'Festival'), #3d85c6
        ('camping', 'Camping'), #6aa84f
        ('entertainment', 'Entertainment'), #cc0000
        ('show', 'Show'), #274e13
    )

    event = AutoOneToOneField(Event, primary_key=True, related_name='profile')
    slug = AutoSlugField(unique=True, editable=True)
    category = models.CharField(max_length=14, choices=CATEGORY_CHOICES, default='general')
    private = models.BooleanField(default=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    facebook_event_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_fyr_event_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_album_id = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    aftermovie_url = models.URLField(max_length=200, null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, blank=True, null=True)
    allow_comments = models.BooleanField('allow comments', default=True)

    #tags = TaggableManager()

    @property
    def in_the_past(self):
        if self.event.end:
            return timezone.now() > self.event.end
        return "No Date Given"   

    def guest_list(self):
        return EventUserRel.objects.filter(event=self.event)

    def guest_count(self):
        return len(EventUserRel.objects.filter(event=self.event))

    def fb_page(self):
        return "https://www.facebook.com/events/{}".format(self.facebook_event_id)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.event.title)
        if not self.host:
            self.host = User.objects.get(username='admin')
        if not self.gallery:
            tmp_slug = slugify(self.event.title)
            self.gallery, created = Gallery.objects.get_or_create(title=self.event.title, slug=tmp_slug)
        super(EventProfile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Event Profile'
        verbose_name_plural = 'Event Profiles'

    def get_absolute_url(self):
        return reverse('event_details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.event.title

class EventUserRel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    fully_paid = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)

class EventIdeas(VoteModel, models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True, editable=True, blank=True)  
    sub_event_idea = models.BooleanField(default=False)  
    description = models.TextField(null=True, blank=True) 
    location = models.CharField(max_length=140, default="Unknown")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    facebook_event_id = models.CharField(max_length=100, null=True, blank=True)
    estimated_cost = models.IntegerField(default="0")
    estimated_date = models.DateField(default=datetime.date.today, null=True, blank=True)
    allow_comments = models.BooleanField('allow comments', default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(EventIdeas, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Event Idea'
        verbose_name_plural = 'Event Ideas'

    def get_absolute_url(self):
        return reverse('event_idea_details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
