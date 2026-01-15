import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
# ====== Import Semua Class yang Dibutuhkan ======
from Hotel.class_hotel import Hotel
from Kamar.class_kamar import Kamar
from Keuangan.class_keuangan import Keuangan
from Staff.class_staff import Staff
from Tamu.class_tamu import Tamu
from Waktu.class_waktu import Waktu
from class_actionbar import ActionBar
from Kamar.class_turunan_kamar import Standard, Deluxe, VIP, Suite
 
# Jika nanti butuh class lain (Staff, Tamu, dll.) bisa di-import di sini
 
def main():
    print("Selamat datang di Simulasi Game Hotel Python!\n")
 
    # Inisialisasi komponen utama
    waktu = Waktu()
    keuangan = Keuangan(saldo_awal=5_000_000)        # saldo awal lebih besar biar nyaman main
    hotel = Hotel("Hotel Python Paradise", keuangan=keuangan)
    action_bar = ActionBar(max_action=5)
 
    # ====== OBSERVER PATTERN: Hotel mendaftar sebagai observer ke Waktu ======
    waktu.attach(hotel)   # <--- Ini kunci utama Observer Pattern!
 
    # Tambahkan kamar awal (bisa dilewatkan, atau ditambah lewat menu)
    kamar1 = Standard(101)
    kamar2 = Deluxe(102)
    hotel.tambah_kamar(kamar1, tampilkan=False)
    hotel.tambah_kamar(kamar2, tampilkan=False)
 
    # Tampilkan info awal
    hotel.tampilkan_info(keuangan)
 
    print("\nHari Pertama Dimulai...\n")
 
    # ====== Main Game Loop ======
    while True:
        print("=" * 45)
        waktu.tampilkan_waktu()
        print(f"Sisa Action Hari Ini: {action_bar.action_left}")
        print("=" * 45)
        print("1. Next 4 Jam")
        print("2. Lihat Problem List")
        print("3. Lihat Status Hotel")
        print("4. Lihat List Kamar")
        print("5. Lihat List Tamu")
        print("6. Tambah Tamu Baru")
        print("7. Upgrade Kamar")
        print("8. Tambah Kamar Baru")
        print("0. Keluar Game")
        print("=" * 45)
 
        pilihan = input("Pilih menu (1-8): ").strip()
 
        # -------------------------------------------------
        if pilihan == "1":
            print("\nWaktu maju 4 jam...")
            ganti_hari = waktu.tambah_jam(4)
            # SEMUA update (masalah, pemasukan, check-out, biaya, laporan)
            # otomatis dipanggil via Observer Pattern di method Hotel.update()
            
            if ganti_hari:
                action_bar.reset_action()
                print("Action point telah di-reset untuk hari baru!")
 
        # -------------------------------------------------
        elif pilihan == "2":
            print("\nDaftar Masalah Hotel:")
            masalah_list = hotel.get_daftar_masalah()
            if not masalah_list:
                print("Tidak ada masalah saat ini.")
            else:
                for i, (id_kamar, desk) in enumerate(masalah_list, 1):
                    print(f"{i}. Kamar {id_kamar} - {desk}")
                
                if input("\nPerbaiki salah satu? (y/n): ").lower() == 'y':
                    try:
                        idx = int(input("Nomor masalah: ")) - 1
                        hotel.perbaiki_masalah(idx, keuangan, waktu, action_bar)
                    except ValueError:
                        print("Input harus angka!")
 
        # -------------------------------------------------
        elif pilihan == "3":
            hotel.tampilkan_info(keuangan)
 
        # -------------------------------------------------
        elif pilihan == "4":
            hotel.tampilkan_daftar_kamar()
 
        # -------------------------------------------------
        elif pilihan == "5":
            hotel.tampilkan_daftar_tamu()
 
        # -------------------------------------------------
        elif pilihan == "6":
            print("\nTambah Tamu Baru")
            nama = input("Nama tamu: ").strip()
            if not nama:
                print("Nama tidak boleh kosong!")
                continue
 
            try:
                lama = int(input("Lama menginap (malam): "))
                if lama <= 0:
                    raise ValueError
            except ValueError:
                print("Lama menginap harus angka positif!")
                continue
 
            from Tamu.class_tamu import Tamu
            tamu_baru = Tamu(nama, lama)
 
            # Cek kamar kosong
            kamar_kosong = [k for k in hotel.get_daftar_kamar() if not k.apakah_terisi()]
            if not kamar_kosong:
                print("Tidak ada kamar kosong!")
                continue
 
            print("\nKamar yang tersedia:")
            for k in kamar_kosong:
                print(f"  → ID {k.get_id()} | {k.get_tipe()} | Rp{k.get_harga():,} per malam")
 
            try:
                id_dipilih = int(input("Pilih ID kamar: "))
            except ValueError:
                print("ID harus angka!")
                continue
 
            if not action_bar.gunakan_action():
                print("Action point tidak cukup untuk check-in!")
                continue
 
            success = hotel.check_in(tamu_baru, id_dipilih)
            if success:
                # Pemasukan uang muka (opsional)
                kamar_terpilih = next((k for k in kamar_kosong if k.get_id() == id_dipilih), None)
                if kamar_terpilih:
                    keuangan.tambah_pemasukan(
                        kamar_terpilih.get_harga(),
                        sumber=f"Check-in {nama} (Kamar {id_dipilih})"
                    )
 
 
        # -------------------------------------------------
        elif pilihan == "7":
            try:
                id_kamar = int(input('Masukkan ID kamar yang ingin di-upgrade: '))
                hotel.upgrade_kamar_hotel(id_kamar, action_bar)
            except ValueError:
                print('❌ Input tidak valid! Harap masukkan angka untuk ID kamar.')
 
        # -------------------------------------------------
        elif pilihan == "8":
            hotel.tambah_kamar_baru(keuangan, action_bar)
 
        # -------------------------------------------------
        elif pilihan == "0":
            print("\n 👋 Terima kasih telah bermain Simulasi Hotel Python!")
            print("Sampai jumpa lagi!")
            break
 
        # -------------------------------------------------
        else:
            print("❌ Pilihan tidak valid, coba lagi.")
 
# ==============================================
if __name__ == "__main__":
    main()