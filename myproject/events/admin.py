from django.contrib import admin
from events.models import EventProfile, EventUserRel, EventIdeas

class EventProfileAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'slug', 'category', 'products_for_sale', 'facebook_event_id', 'host')

    def get_title(self, obj):
        return obj.event.title
    get_title.short_description = 'Title'
    get_title.admin_order_field = 'event__title'

class EventUserRelAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'approved', 'fully_paid', 'amount_paid')

    list_editable = ('approved', 'fully_paid',)

admin.site.register(EventUserRel, EventUserRelAdmin)
admin.site.register(EventProfile, EventProfileAdmin)
admin.site.register(EventIdeas)
