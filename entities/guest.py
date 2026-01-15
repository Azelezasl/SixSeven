class Guest:
    """Represents a hotel guest."""

    def __init__(self, name: str, duration: int):
        self._name = name
        self._duration = duration  # in nights
        self._room_id = None
        self._status = 'Pending'
        self._hours_stayed = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def room_id(self):
        return self._room_id

    @property
    def is_checked_out(self) -> bool:
        return self._hours_stayed >= (self._duration * 24)

    def assign_room(self, room_id: int):
        self._room_id = room_id
        self._status = 'Checked In'

    def checkout(self):
        self._room_id = None
        self._status = 'Checked Out'

    def add_stay_hours(self, hours: int):
        self._hours_stayed += hours

    def __str__(self):
        return f"Guest(Name={self._name}, Status={self._status})"