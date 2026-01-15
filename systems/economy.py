class FinanceSystem:
    def __init__(self, initial_balance: float):
        self._balance = initial_balance
        self._income = 0
        self._expenses = 0

    @property
    def balance(self):
        return self._balance

    @property
    def formatted_balance(self):
        return f"Rp{self._balance:,.0f}".replace(",", ".")

    def can_afford(self, amount: float) -> bool:
        return self._balance >= amount

    def record_income(self, amount: float, source: str):
        self._balance += amount
        self._income += amount

    def record_expense(self, amount: float, reason: str):
        self._balance -= amount
        self._expenses += amount
        print(f"  [-] Rp{amount:,.0f} ({reason})")

    def print_report(self):
        print(f"💵 Balance : {self.formatted_balance}")
        print(f"📈 Income  : Rp{self._income:,.0f}")
        print(f"📉 Expense : Rp{self._expenses:,.0f}")