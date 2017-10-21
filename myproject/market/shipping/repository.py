from oscar.apps.shipping import repository
from . import methods

class Repository(repository.Repository):

    def get_available_shipping_methods(
            self, basket, user=None, shipping_addr=None,
            request=None, **kwargs):
        shipping_methods = (methods.Standard(), methods.Pickup())

        return shipping_methods