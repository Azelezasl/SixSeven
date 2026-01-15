class Staff:
    def __init__(self, nama: str, jabatan: str, gaji: float):
        # Atribut dasar untuk semua pegawai hotel
        self._nama = nama
        self._jabatan = jabatan
        self._gaji = gaji
        self._status = "Aktif"
 
    # ====== Bagian Getter ======
    def get_nama(self):
        return self._nama
 
    def get_jabatan(self):
        return self._jabatan
 
    def get_gaji(self):
        return self._gaji
 
    def get_status(self):
        return self._status