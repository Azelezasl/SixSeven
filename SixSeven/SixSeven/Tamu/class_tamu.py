class Tamu:
    def __init__(self, nama: str, lama_menginap: int):
        self.__nama = nama
        self.__lama_menginap = lama_menginap  # dalam malam (1 malam = 24 jam)
        self.__kamar = None
        self.__status = 'Belum Check-in'
        self.__jam_terhitung = 0  # total jam sejak check-in

    # ===== Getter =====
    def get_nama(self):
        return self.__nama

    def get_lama_menginap(self):
        return self.__lama_menginap

    def get_status(self):
        return self.__status

    def get_kamar(self):
        return self.__kamar

    # ===== Operasi =====
    def set_kamar(self, kamar):
        self.__kamar = kamar
        self.__status = 'Sedang Menginap'

    def keluar_dari_kamar(self):
        self.__kamar = None
        self.__status = 'Sudah Check-out'

    def tambah_jam(self, jam):
        """Menambah waktu menginap berjalan (jam demi jam)."""
        self.__jam_terhitung += jam

    def sudah_selesai(self):
        """True jika jam menginap >= target (lama_menginap * 24 jam)."""
        return self.__jam_terhitung >= self.__lama_menginap * 24

    def tampilkan_info(self):
        nama_kamar = self.__kamar.get_id() if self.__kamar else '-'
        print(f'👤 Nama Tamu       : {self.__nama}')
        print(f'🕓 Lama Menginap   : {self.__lama_menginap} malam')
        print(f'🏠 Kamar Saat Ini  : {nama_kamar}')
        print(f'📋 Status          : {self.__status}')
