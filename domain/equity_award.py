from decimal import Decimal


class NegativeVestedSharesException(Exception):
    pass


class EquityAward:

    def __init__(self, award_id, employee):
        self.id = award_id
        self.employee = employee
        self.__vested_shares = Decimal("0")


    @property
    def vested_shares(self):
        return max(0, self.__vested_shares)

    def vest_shares(self, quantity):
        self.__vested_shares += Decimal(quantity)

    def cancel_shares(self, quantity):
        self.__vested_shares -= Decimal(quantity)
