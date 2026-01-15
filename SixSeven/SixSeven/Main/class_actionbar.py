class ActionBar:
    def __init__(self, max_action=2):
        self.max_action = max_action
        self.action_left = max_action
 
    def gunakan_action(self, jumlah=1,tampilkan=True):
        """Kurangi action point"""
        if self.action_left >= jumlah:
            self.action_left -= jumlah
            if tampilkan:
                print(f"🛠️  Menggunakan {jumlah} action. Sisa action: {self.action_left}")
                return True
        else:
            print("⚠️  Tidak cukup action point tersisa!")
            return False
 
    def reset_action(self):
        """Reset action setiap pergantian hari"""
        self.action_left = self.max_action
        print(f"🌅 Hari baru dimulai! Action bar direset ke {self.max_action}.")