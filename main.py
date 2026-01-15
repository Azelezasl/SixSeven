import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from entities.room_types import Standard, Deluxe
from systems.time_system import TimeSystem
from systems.economy import FinanceSystem
from systems.maintenance import MaintenanceSystem
from systems.action_bar import ActionBar
from core.hotel import Hotel
from core.factories import RoomFactory

def main():
    time_sys = TimeSystem()
    finance_sys = FinanceSystem(5_000_000)
    maint_sys = MaintenanceSystem()
    action_bar = ActionBar(max_actions=5)
    
    hotel = Hotel("Python Paradise", finance_sys, maint_sys)
    
    time_sys.attach(hotel)

    hotel.add_room(Standard(101))
    hotel.add_room(Deluxe(102))

    print("=== Hotel Simulation Started ===")

    while True:
        print("\n" + "="*40)
        time_sys.display()
        print(f"⚡ Actions Left: {action_bar.remaining}")
        print("="*40)
        print("1. Wait (4 Hours)")
        print("2. Hotel Status")
        print("3. Check In Guest")
        print("4. Build New Room")
        print("5. Upgrade Room")
        print("6. Fix Problems")
        print("0. Exit")
        
        choice = input("Select: ").strip()

        if choice == "1":
            new_day = time_sys.advance_time(4)
            if new_day:
                action_bar.reset()

        elif choice == "2":
            hotel.print_status()

        elif choice == "3":
            try:
                name = input("Guest Name: ")
                days = int(input("Nights: "))
                room_id = int(input("Room ID: "))
                hotel.check_in(name, days, room_id, action_bar)
            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            print("\nOptions:")
            for k, v in RoomFactory.get_options().items():
                print(f"{k}. {v[0]} - Rp{v[2]:,.0f}")
            sel = input("Choice: ")
            hotel.build_new_room(sel, action_bar)

        elif choice == "5":
            try:
                rid = int(input("Room ID to Upgrade: "))
                hotel.upgrade_room(rid, action_bar)
            except ValueError:
                print("Invalid ID.")

        elif choice == "6":
            issues = hotel.get_issues()
            if not issues:
                print("No issues pending.")
            else:
                for r in issues:
                    print(f"- Room {r.id}: {r.issue_description}")
                try:
                    rid = int(input("Enter Room ID to fix: "))
                    hotel.resolve_issue(rid, action_bar)
                except ValueError:
                    print("Invalid ID.")

        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Unknown Command.")

if __name__ == "__main__":
    main()