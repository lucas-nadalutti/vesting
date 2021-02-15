
class StdoutHandler:

    def generate_vesting_schedule(self, equity_awards):
        ordered_equity_awards = sorted(equity_awards, key=lambda e: (e.employee.id, e.id))
        for award in ordered_equity_awards:
            print("{employee_id},{employee_name},{award_id},{vested_shares}".format(
                employee_id=award.employee.id,
                employee_name=award.employee.name,
                award_id=award.id,
                vested_shares=award.vested_shares,
            ))
