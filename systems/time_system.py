from core.interfaces import Subject

class TimeSystem(Subject):
    def __init__(self):
        super().__init__()
        self._day = 1
        self._hour = 0
        self._engine = self._run_clock()
        next(self._engine)  # Prime generator

    @property
    def hour(self):
        return self._hour

    def _run_clock(self):
        while True:
            hours_added = yield
            if hours_added is None: 
                continue
            
            self._hour += hours_added
            new_day = False
            
            if self._hour >= 24:
                self._hour -= 24
                self._day += 1
                new_day = True
            
            yield new_day

    def advance_time(self, hours: int):
        next(self._engine) # Prep
        is_new_day = self._engine.send(hours)
        
        # Notify Observers (Hotel)
        self.notify(is_new_day)
        return is_new_day

    def display(self):
        print(f"📅 Day {self._day} | 🕓 {self._hour:02d}:00")