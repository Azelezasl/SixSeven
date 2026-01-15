import random

class Kamar:
    def __init__(self, id_kamar: int, tipe: str, harga_per_malam: float):
        # Atribut private untuk menjaga enkapsulasi
        self.__id_kamar = id_kamar
        self.__tipe = tipe
        self.__harga_per_malam = harga_per_malam
        self.__terisi = False
        self.__tamu = None
        self.status_masalah = False
        self.jenis_masalah = None
        self.__masalah = None
 
    # ====== Bagian Getter ======
    def get_id(self):
        return self.__id_kamar
 
    def get_tipe(self):
        return self.__tipe
 
    def get_harga(self):
        return self.__harga_per_malam
 
    def apakah_terisi(self):
        """Mengembalikan True jika kamar sedang ditempati"""
        return self.__terisi
 
    def get_tamu(self):
        """Mengembalikan objek tamu yang sedang menginap (jika ada)"""
        return self.__tamu
 
    # ====== Bagian Operasi ======
    def tetapkan_tamu(self, tamu):
        """Menetapkan tamu ke kamar ini"""
        if not self.__terisi:
            self.__tamu = tamu
            self.__terisi = True
            print(f"Kamar {self.__id_kamar} kini ditempati oleh {tamu.get_nama()}.")
        else:
            print(f"❌ Kamar {self.__id_kamar} sudah terisi.")
 

    def hapus_tamu(self):
        """Mengosongkan kamar setelah tamu check-out"""
        if self.__terisi:
            print(f"Kamar {self.__id_kamar} kini dikosongkan.")
            self.__tamu = None
            self.__terisi = False
        else:
            print(f"Kamar {self.__id_kamar} memang sudah kosong.")
 

    def buat_masalah_random(self):
        """Kemungkinan kecil muncul masalah baru di kamar."""
        if self.__masalah is not None:
            return None  # sudah ada masalah aktif, jangan tumpuk
 
        # daftar kemungkinan masalah
        daftar_masalah = [
            "Kebocoran di Bathtub",
            "AC rusak",
            "Lampu tidak menyala",
            "Air panas tidak keluar",
            "Kunci pintu macet",
            "TV tidak berfungsi",
            "Kasur tersiram kopi",
            "Kaca Rias Retak"
        ]
 
        # peluang muncul masalah (misal 10%)
        if random.random() < 0.10:
            self.__masalah = random.choice(daftar_masalah)
            return self.__masalah
        return None
 
    def perbaiki_masalah(self):
        """Memperbaiki masalah di kamar"""
        if self.__masalah:
            print(f"✅ Masalah di kamar {self.get_id()} telah diperbaiki ({self.__masalah})")
            self.__masalah = None
        else:
            print(f"ℹ️ Tidak ada masalah di kamar {self.nomor}.")

    def tampilkan_info(self):
        """Menampilkan informasi singkat tentang kamar"""
        status = "Terisi" if self.__terisi else "Kosong"
        print(f"🏠 ID Kamar  : {self.__id_kamar}")
        print(f"🛏️ Tipe      : {self.__tipe}")
        print(f"💵 Harga     : Rp{self.__harga_per_malam} / malam")
        print(f"📋 Status    : {status}")



        