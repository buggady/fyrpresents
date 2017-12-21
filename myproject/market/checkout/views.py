from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from oscar.apps.checkout import views
from oscar.apps.payment import forms, models
from djstripe.models import Customer

class PaymentDetailsView(views.PaymentDetailsView):

    def get_context_data(self, **kwargs):

        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)

        ctx['stripe_total'] = ctx['order_total'].incl_tax * Decimal('100.00')
        ctx['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        customer, created = Customer.get_or_create(subscriber=self.request.user)
        ctx['customer'] = customer
        return ctx

    def post(self, request, *args, **kwargs):

        if request.POST.get('action', '') == 'use_default_payment_card':
            token = self.request.POST.get('stripeToken','')
            customer, created = Customer.get_or_create(subscriber=self.request.user)
            customer.update_card(token)
            return self.render_preview(request)

        if request.POST.get('action', '') == 'use_new_payment_card':
            
            customer = self.get_object()
            try:
                customer.update_card(
                    request.POST.get("stripe_token")
                )
            except stripe.StripeError as exc:
                messages.info(request, "Stripe Error")
                return render(
                    request,
                    self.template_name,
                    {
                        "customer": self.get_object(),
                        "stripe_error": str(exc)
                    }
                )
            messages.info(request, "Your card is now updated.")
            return redirect(self.get_post_success_url())
            
        if request.POST.get('action', '') == 'place_order':
            return self.handle_place_order_submission(request)


        return self.render_preview(request)

    def handle_payment(self, order_number, total, **kwargs):
        
        customer, created = Customer.get_or_create(subscriber=self.request.user)
        customer.charge(total.incl_tax)

        # Record payment source and event
        source_type, is_created = models.SourceType.objects.get_or_create(
            name='Stripe')
        source = source_type.sources.model(
            source_type=source_type,
            amount_allocated=total.incl_tax, currency=total.currency)
        self.add_payment_source(source)
        self.add_payment_event('Submitted', total.incl_tax)