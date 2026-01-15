from entities.room_types import Standard, Deluxe, Suite, VIP

class RoomFactory:
    """Factory for creating Room instances."""
    
    _REGISTRY = {
        "1": ("Standard", Standard, 500_000),
        "2": ("Deluxe", Deluxe, 1_000_000),
        "3": ("Suite", Suite, 2_000_000),
        "4": ("VIP", VIP, 4_000_000)
    }

    @classmethod
    def create_room(cls, choice: str, room_id: int):
        if choice not in cls._REGISTRY:
            raise ValueError("Invalid room type choice.")
        
        type_name, class_ref, build_cost = cls._REGISTRY[choice]
        return class_ref(room_id), build_cost, type_name

    @classmethod
    def get_options(cls):
        return cls._REGISTRY
    
    @classmethod
    def get_upgrade_map(cls):
        return {
            "Standard": Deluxe,
            "Deluxe": Suite,
            "Suite": VIP
        }