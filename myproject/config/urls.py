from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import logout
from oscar.app import application
from oscar_accounts.dashboard.app import application as accounts_app
from paypal.express.dashboard.app import application as paypal_app

urlpatterns = [
	url(r'^', include('fyrpresents.urls')),
	url(r'^events/', include('events.urls')),
	url(r'^user/', include('users.urls')),
	url(r'^mingle/', include('mingle.urls')),
	url(r'^accounts/logout/$', logout,{'next_page': '/'}),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^photologue/', include('photologue.urls', namespace='photologue')),
	url(r'^newsletter/', include('newsletter.urls')),
	url(r'^calendar/', include('schedule.urls')),
	url(r'^weblog/', include('zinnia.urls', namespace="zinnia")),
	url(r'^comments/', include('django_comments_xtd.urls')),
	url(r'^i18n/', include('django.conf.urls.i18n')),
	url(r'^market/', include(application.urls)),
	url(r'^checkout/paypal/', include('paypal.express.urls')),
    url(r'^dashboard/paypal/express/', include(paypal_app.urls)),
    url(r'^dashboard/accounts/', include(accounts_app.urls)),
	url(r'^admin_tools/', include('admin_tools.urls')),
	url(r'^admin/', admin.site.urls),
] 

handler400 = 'myproject.views.bad_request'
handler403 = 'myproject.views.permission_denied'
handler404 = 'myproject.views.not_found'
handler500 = 'myproject.views.server_error'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^debug/', include(debug_toolbar.urls)),
        url(r'^explorer/', include('explorer.urls')),
    ]
