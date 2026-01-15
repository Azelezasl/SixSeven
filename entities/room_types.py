from .room import Room

class Standard(Room):
    def __init__(self, room_id: int):
        super().__init__(room_id, "Standard", 100_000)

class Deluxe(Room):
    def __init__(self, room_id: int):
        super().__init__(room_id, "Deluxe", 200_000)

class Suite(Room):
    def __init__(self, room_id: int):
        super().__init__(room_id, "Suite", 400_000)

class VIP(Room):
    def __init__(self, room_id: int):
        super().__init__(room_id, "VIP", 800_000)