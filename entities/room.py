class Room:
    """Base Room Entity."""

    def __init__(self, room_id: int, r_type: str, price: float):
        self._id = room_id
        self._type = r_type
        self._price = price
        self._guest = None
        self._issue = None  # String description of issue, None if clean

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def price(self):
        return self._price

    @property
    def is_occupied(self):
        return self._guest is not None

    @property
    def has_issue(self):
        return self._issue is not None

    @property
    def issue_description(self):
        return self._issue

    def check_in(self, guest) -> bool:
        if self.is_occupied or self.has_issue:
            return False
        self._guest = guest
        return True

    def check_out(self):
        removed_guest = self._guest
        self._guest = None
        return removed_guest

    def report_issue(self, description: str):
        self._issue = description

    def fix_issue(self):
        self._issue = None