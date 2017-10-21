from decimal import Decimal as D
from oscar.apps.shipping import methods
from oscar.core import prices

class Standard(methods.Base):
    code = 'standard'
    name = 'Standard shipping'

    charge_excl_tax = D('5.00')
    charge_incl_tax = D('5.10')
	
    def calculate(self, basket):
        return prices.Price(
            currency=basket.currency,
            excl_tax=self.charge_excl_tax,
            incl_tax=self.charge_incl_tax)
			
class Pickup(methods.Base):
    code = 'pickup'
    name = 'Pick Up'
    description = 'You will pick up item in person'
	
    def calculate(self, basket):
        return prices.Price(
            currency=basket.currency,
            excl_tax=D('0.00'), incl_tax=D('0.00'))