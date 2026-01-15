import random

class MaintenanceSystem:
    PROBLEMS = {
        "Leaky Bathtub": 30_000,
        "Broken AC": 50_000,
        "Broken Lights": 20_000,
        "Door Jammed": 25_000,
        "TV Malfunction": 35_000
    }

    def generate_issues(self, rooms):
        """Randomly breaks things in rooms."""
        for room in rooms:
            if not room.has_issue and random.random() < 0.10: # 10% chance
                issue = random.choice(list(self.PROBLEMS.keys()))
                room.report_issue(issue)
                print(f"⚠️ ALERT: Room {room.id} has {issue}!")

    def get_repair_cost(self, issue_name):
        return self.PROBLEMS.get(issue_name, 30_000)