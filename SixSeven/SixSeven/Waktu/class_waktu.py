class Waktu:
    def __init__(self):
        self._hari = 1
        self._jam = 0
        self._engine = self._time_engine()
        next(self._engine)  # priming, stop di yield pertama
        
        # Tambahan untuk Observer Pattern: Daftar observer
        self._observers = []  # List of observers (e.g., Hotel instances)
 
    def _time_engine(self):
        """Coroutine yang menerima jam dan mengembalikan apakah ganti hari."""
        while True:
            tambah_jam = yield     # ← menunggu input dari send()
 
            if tambah_jam is None:
                continue           # jaga-jaga agar tidak error
 
            self._jam += tambah_jam
            ganti = False
 
            if self._jam >= 24:
                self._jam -= 24
                self._hari += 1
                ganti = True
 
            yield ganti            # ← balikan ke pemanggil
 
    def tambah_jam(self, jumlah):
        """Panggilan API waktu"""
        next(self._engine)           # maju sampai yield pertama (wait for input)
        ganti_hari = self._engine.send(jumlah)
        
        # Notify semua observer setelah waktu berubah
        self._notify_observers(ganti_hari)
        
        return ganti_hari
 
    # Method Observer Pattern
    def attach(self, observer):
        """Tambah observer ke daftar."""
        if observer not in self._observers:
            self._observers.append(observer)
 
    def detach(self, observer):
        """Hapus observer dari daftar."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass  # Jika tidak ada, abaikan
 
    def _notify_observers(self, ganti_hari):
        """Notify semua observer dengan data perubahan (ganti_hari)."""
        for observer in self._observers:
            observer.update(self, ganti_hari)  # Panggil update di observer, kirim self (subject) dan data
 
    def tampilkan_waktu(self):
        print(f"📅 Hari ke-{self._hari} | 🕓 Jam {self._jam:02d}:00")
 
    def get_jam(self):
        return self._jam
 
    def get_hari(self):
        return self._hari