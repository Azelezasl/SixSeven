class ActionBar:
    def __init__(self, max_actions=2):
        self._max = max_actions
        self._current = max_actions

    @property
    def remaining(self):
        return self._current

    def use_action(self, cost=1) -> bool:
        if self._current >= cost:
            self._current -= cost
            print(f"🛠️ Action used. Remaining: {self._current}")
            return True
        print("⚠️ Not enough action points!")
        return False

    def reset(self):
        self._current = self._max
        print("🌅 Energy restored.")