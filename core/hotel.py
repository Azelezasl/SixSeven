from core.interfaces import Observer
from core.factories import RoomFactory
from entities.room import Room
from entities.guest import Guest

class Hotel(Observer):
    """
    Central Controller for the Hotel Simulation.
    Facades over Room management, Guests, and interactions.
    """

    def __init__(self, name: str, finance_system, maintenance_system):
        self.name = name
        self._finance = finance_system
        self._maintenance = maintenance_system
        self._rooms = []
        self._guests = []
        self._room_id_counter = 101

    def _next_id(self):
        self._room_id_counter += 1
        return self._room_id_counter

    # --- Observer Implementation ---
    def update(self, subject, is_new_day: bool):
        """Called by TimeSystem when time advances."""
        # 1. Process Income & Guest Stays
        self._process_hourly_updates()

        # 2. Daily Deductions
        if subject.hour in [0, 12]:
            self._finance.record_expense(20_000, "Utilities (Electricity/Water)")

        # 3. Random Maintenance Events
        self._maintenance.generate_issues(self._rooms)

        if is_new_day:
            print("\n🧾 Daily Report:")
            self._finance.print_report()

    def _process_hourly_updates(self):
        total_income = 0
        leaving_guests = []

        for room in self._rooms:
            if room.is_occupied:
                # Revenue Calculation (4-hour block logic preserved)
                income = room.price / 6 
                total_income += income
                
                # Update Guest
                guest = room._guest
                guest.add_stay_hours(4)

                self._finance.record_income(income, f"Room {room.id} Stay")

                if guest.is_checked_out:
                    leaving_guests.append(room)

        # Process Checkouts
        for room in leaving_guests:
            self.checkout_guest(room.id, auto=True)

    # --- Room Management ---
    def add_room(self, room: Room):
        self._rooms.append(room)

    def build_new_room(self, type_choice: str, action_bar):
        try:
            # 1. Validate Action
            if not action_bar.use_action(): 
                return

            # 2. Factory Creation (Dry Run to get cost)
            options = RoomFactory.get_options()
            if type_choice not in options:
                print("❌ Invalid selection.")
                return
            _, _, cost = options[type_choice]

            # 3. Validate Finance
            if not self._finance.can_afford(cost):
                print(f"❌ Insufficient funds. Need Rp{cost:,.0f}")
                return

            # 4. Execute
            self._finance.record_expense(cost, "New Room Construction")
            new_room, _, _ = RoomFactory.create_room(type_choice, self._next_id())
            self._rooms.append(new_room)
            print(f"✅ Built {new_room.type} Room {new_room.id}")

        except ValueError as e:
            print(f"Error: {e}")

    def upgrade_room(self, room_id: int, action_bar):
        room = self._find_room(room_id)
        if not room: 
            print("❌ Room not found.")
            return

        if room.is_occupied:
            print("❌ Cannot upgrade occupied room.")
            return
        
        upgrade_map = RoomFactory.get_upgrade_map()
        if room.type not in upgrade_map:
            print("❌ Room is already max level.")
            return

        target_class = upgrade_map[room.type]
        # Calculate cost difference or static cost (Simulated logic)
        cost = 1_000_000 # Simplified for refactor example

        if self._finance.can_afford(cost) and action_bar.use_action():
            self._finance.record_expense(cost, f"Upgrade Room {room_id}")
            # Replace room instance logic
            new_room = target_class(room.id)
            index = self._rooms.index(room)
            self._rooms[index] = new_room
            print(f"✅ Upgraded Room {room_id} to {new_room.type}")

    # --- Guest Operations ---
    def check_in(self, name: str, nights: int, room_id: int, action_bar):
        room = self._find_room(room_id)
        if not room:
            print("❌ Room not found.")
            return
            
        if not action_bar.use_action():
            return

        guest = Guest(name, nights)
        if room.check_in(guest):
            guest.assign_room(room.id)
            self._guests.append(guest)
            # Initial Deposit
            self._finance.record_income(room.price, f"Deposit {guest.name}")
            print(f"✅ {name} checked into Room {room.id}")
        else:
            print(f"❌ Room {room_id} is unavailable (Occupied or Maintenance).")

    def checkout_guest(self, room_id: int, auto=False):
        room = self._find_room(room_id)
        if room and room.is_occupied:
            guest = room.check_out()
            if guest in self._guests:
                self._guests.remove(guest)
            guest.checkout()
            prefix = "🕓 Auto-Checkout" if auto else "✅ Checkout"
            print(f"{prefix}: {guest.name} left Room {room.id}")

    # --- Maintenance Operations ---
    def resolve_issue(self, room_id: int, action_bar):
        room = self._find_room(room_id)
        if not room or not room.has_issue:
            print("❌ No issues found in this room.")
            return

        cost = self._maintenance.get_repair_cost(room.issue_description)
        
        if self._finance.can_afford(cost) and action_bar.use_action():
            self._finance.record_expense(cost, f"Repair Room {room_id}")
            room.fix_issue()
            print(f"✅ Fixed Room {room_id}")

    # --- Helpers ---
    def _find_room(self, r_id):
        return next((r for r in self._rooms if r.id == r_id), None)

    def get_issues(self):
        return [r for r in self._rooms if r.has_issue]

    def print_status(self):
        print(f"\n🏨 {self.name} Status")
        print(f"💰 Balance: {self._finance.formatted_balance}")
        print(f"🛏️ Rooms: {len(self._rooms)} | Guests: {len(self._guests)}")