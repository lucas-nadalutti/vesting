from decimal import Decimal


class NegativeVestedSharesException(Exception):
    pass


class EquityAward:

    def __init__(self, award_id, employee, vested_shares):
        self.id = award_id
        self.employee = employee
        self.vested_shares = Decimal(vested_shares)

    def vest_shares(self, quantity):
        self.vested_shares += Decimal(quantity)

    def cancel_shares(self, quantity):
        vested_shares = self.vested_shares - Decimal(quantity)
        if vested_shares < Decimal('0'):
            raise NegativeVestedSharesException

        self.vested_shares = vested_shares
