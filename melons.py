from random import randint
import datetime

"""Classes for melon orders."""


class AbstractMelonOrder(object):
    """An abstract base class that other Melon Orders inherit from."""

    def __init__(self, species, qty, order_type, tax):
        """Initialize melon order attributes."""

        if qty > 100:
            raise TooManyMelonsError

        self.species = species
        self.qty = qty
        self.shipped = False
        self.order_type = order_type
        self.tax = tax

    def get_total(self):
        """Calculate price, including tax."""

        base_price = self.get_base_price()
        fee = 0

        if self.species == 'Christmas':
            base_price = 1.5 * base_price

        total = (1 + self.tax) * self.qty * base_price + fee

        return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True

    def get_base_price(self):
        """Calculate base price based on Splurge pricing, rush hour."""

        base_price = randint(5, 9)

        if datetime.time.hour >= 8 and datetime.time.hour < 11 \
           and datetime.date.weekday() <= 4:
            return 4 + base_price
        else:
            return base_price


class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    def __init__(self, species, qty):
        """Initialize melon order attributes."""

        super(DomesticMelonOrder, self).__init__(species, qty, 'domestic', 0.08)


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes."""

        super(InternationalMelonOrder, self).__init__(species, qty,
                                                      'international', 0.17)

        self.country_code = country_code

    def get_total(self):
        """Calculate price including tax and international fees."""

        subtotal = super(InternationalMelonOrder, self).get_total()

        if self.qty < 10:
            return subtotal + 3
        else:
            return subtotal

    def get_country_code(self):
        """Return the country code."""

        return self.country_code


class GovernmentMelonOrder(AbstractMelonOrder):
    """A US government melon order that goes through a security inspection."""

    def __init__(self, species, qty):
        """Initialize melon order attributes."""

        super(GovernmentMelonOrder, self).__init__(species, qty, 'domestic', 0)

        self.passed_inspection = False

    def mark_inspection(self, passed):
        """Record whether the order passed its inspection."""

        self.passed_inspection = passed


class TooManyMelonsError(ValueError):
    """Raise an error for orders of more than 100 melons."""

    def __init__(self):
        super(TooManyMelonsError, self).__init__("No more than 100 melons!")

order0 = InternationalMelonOrder("Christmas", 105, "AUS")
