from Kamar.upgrade_manager import upgrade_kamar
from Kamar.class_turunan_kamar import Standard, Deluxe, Suite, VIP

class Hotel:
    def __init__(self, nama: str, saldo_awal: float = 0,keuangan=None):
        # Atribut private untuk enkapsulasi
        self.__nama = nama
        self.__saldo = saldo_awal
        self.__keuangan = keuangan

        # Koleksi internal
        self.__daftar_kamar = []          # list berisi objek Kamar
        self.__daftar_pegawai = []        # list berisi objek Staff
        self.__daftar_tamu = []           # list berisi objek Tamu (rekaman)
        self.__daftar_masalah = []        # list berisi tuple (id_kamar, deskripsi)
        self.__reputasi = 50              # reputasi awal (0-100)

        # Iterator khusus untuk ID kamar baru
        self.__id_iterator = self._id_generator()

    # ===============================
    # Iterator Generator untuk ID Kamar
    # ===============================
    def _id_generator(self):
        """Menghasilkan ID kamar baru secara otomatis (mulai dari 102)."""
        id_awal = 102
        while True:
            id_awal += 1
            yield id_awal

    def __iter__(self):
        """Memungkinkan: for kamar in hotel: ... (iterasi atas daftar kamar)."""
        return iter(self.__daftar_kamar)

    # ===============================
    # Fitur Tambah Kamar Baru
    # ===============================
    def tambah_kamar_baru(self, keuangan, action_bar):
        print('\n🏗️  Tambah Kamar Baru')
        tipe_kamar_dict = {
            '1': ('Standard', Standard, 500_000),
            '2': ('Deluxe', Deluxe, 1_000_000),
            '3': ('Suite', Suite, 2_000_000),
            '4': ('VIP', VIP, 4_000_000)
        }

        # Tampilkan tipe kamar
        [print(f'{key}. {value[0]} (Rp{value[2]:,})') for key, value in tipe_kamar_dict.items()]

        pilihan = input('Masukkan pilihan (1-4): ')
        if pilihan not in tipe_kamar_dict:
            print('❌ Pilihan tidak valid.')
            return

        tipe, kelas, biaya = tipe_kamar_dict[pilihan]

        # 🔒 Cek action bar dulu
        if not hasattr(action_bar, 'action_left'):
            print('⚠️ Action bar tidak valid.')
            return

        if action_bar.action_left <= 0:
            print('⚠️ Action kamu sudah habis! Tidak bisa membangun kamar baru sekarang.')
            return

        # Cek saldo
        if hasattr(keuangan, 'get_saldo'):
            saldo_sekarang = keuangan.get_saldo()
        else:
            saldo_sekarang = self.__saldo

        if saldo_sekarang < biaya:
            print('❌ Saldo tidak cukup untuk membangun kamar ini.')
            return

        # 🔧 Gunakan action bar terlebih dahulu
        if hasattr(action_bar, 'gunakan_action'):
            success = action_bar.gunakan_action(1)
            if not success:
                print('⚠️ Gagal menggunakan action untuk pembangunan kamar.')
                return
            print('⚙️  Action bar berkurang 1 karena pembangunan kamar.')

        # 💰 Potong saldo
        if hasattr(keuangan, 'kurangi_pengeluaran'):
            keuangan.kurangi_pengeluaran(biaya, tujuan=f'Pembangunan kamar baru ({tipe})')
        else:
            self.__saldo -= biaya

        # 🏨 Buat ID kamar baru dari iterator
        id_baru = next(self.__id_iterator)
        kamar_baru = kelas(id_baru)
        self.__daftar_kamar.append(kamar_baru)

        # ✅ Konfirmasi sukses
        if hasattr(keuangan, 'get_saldo'):
            saldo_fmt = f'{int(keuangan.get_saldo()):,}'.replace(',', '.')
            print(f'✅ Kamar {id_baru} tipe {tipe} berhasil dibangun! Saldo sekarang: Rp{saldo_fmt}')
        else:
            print(f'✅ Kamar {id_baru} tipe {tipe} berhasil dibangun!')


    # ===============================
    # Daftar & Operasi Kamar / Tamu
    # ===============================
    def tampilkan_daftar_tamu(self):
        """Menampilkan daftar tamu yang sedang menginap di setiap kamar."""
        ada_tamu = False
        print('\n👥 Daftar Tamu yang Sedang Menginap:')
        for kamar in self.__daftar_kamar:
            if kamar.apakah_terisi():
                tamu = kamar.get_tamu()
                if tamu:
                    print(f'• Kamar {kamar.get_id()} ({kamar.get_tipe()}) - {tamu.get_nama()}')
                    ada_tamu = True

        if not ada_tamu:
            print('🧳 Belum ada tamu yang menginap di hotel saat ini.')

    def tampilkan_daftar_kamar(self):
        if not self.__daftar_kamar:
            print('🏨 Belum ada kamar di hotel ini.')
            return
        print('\n🛏️ Daftar Kamar Hotel:')
        for kamar in self.__daftar_kamar:
            status = 'Terisi' if kamar.apakah_terisi() else 'Kosong'
            print(f'• ID: {kamar.get_id()} | Tipe: {kamar.get_tipe()} | Harga: Rp{kamar.get_harga()} | Status: {status}')

    def tambah_kamar(self, kamar, tampilkan=True):
        """Menambahkan objek Kamar ke hotel."""
        self.__daftar_kamar.append(kamar)
        kamar_id = kamar.get_id() if hasattr(kamar, 'get_id') else str(kamar)
        if tampilkan:
            print(f"✅ Kamar '{kamar_id}' berhasil ditambahkan ke hotel {self.__nama}.")

    def check_in(self, tamu, id_kamar):
        """Proses check-in tamu ke kamar berdasarkan id_kamar."""
        for kamar in self.__daftar_kamar:
            if hasattr(kamar, 'get_id') and kamar.get_id() == id_kamar:
                if not kamar.apakah_terisi():
                    if hasattr(kamar, 'tetapkan_tamu'):
                        kamar.tetapkan_tamu(tamu)
                    # catat tamu di daftar hotel (rekam)
                    self.__daftar_tamu.append(tamu)
                    nama_tamu = tamu.get_nama() if hasattr(tamu, 'get_nama') else str(tamu)
                    print(f"✅ {nama_tamu} berhasil check-in ke kamar {id_kamar}.")
                    return
                else:
                    print('❌ Kamar sedang terisi, tidak bisa digunakan.')
                    return
        print('❌ Kamar tidak ditemukan.')

    def update_tamu_menginap(self, jam: int):
        """Menambah jam menginap setiap tamu dan melakukan auto check-out jika waktunya habis."""
        tamu_yang_keluar = []

        for kamar in self.__daftar_kamar:
            if kamar.apakah_terisi():
                tamu = kamar.get_tamu()
                if tamu:
                    tamu.tambah_jam(jam)
                    if tamu.sudah_selesai():
                        tamu_yang_keluar.append((kamar, tamu))

        # Proses check-out otomatis
        for kamar, tamu in tamu_yang_keluar:
            id_kamar = kamar.get_id()
            self.check_out(id_kamar)
            print(f'🚪 {tamu.get_nama()} telah otomatis check-out setelah menyelesaikan masa inap.')

    def check_out(self, id_kamar=None, tamu=None, otomatis=False):
        """Proses check-out tamu (manual atau otomatis)."""
        # Jika check-out otomatis berdasarkan objek tamu
        if tamu:
            for kamar in self.__daftar_kamar:
                if kamar.apakah_terisi() and kamar.get_tamu() == tamu:
                    id_kamar = kamar.get_id()
                    break

        # Lanjutkan jika ID kamar ditemukan
        for kamar in self.__daftar_kamar:
            if hasattr(kamar, 'get_id') and kamar.get_id() == id_kamar and kamar.apakah_terisi():
                tamu_dalam = kamar.get_tamu() if hasattr(kamar, 'get_tamu') else None
                if hasattr(kamar, 'hapus_tamu'):
                    kamar.hapus_tamu()
                if tamu_dalam and tamu_dalam in self.__daftar_tamu:
                    self.__daftar_tamu.remove(tamu_dalam)
                    if hasattr(tamu_dalam, 'keluar_dari_kamar'):
                        tamu_dalam.keluar_dari_kamar()

                nama_tamu = tamu_dalam.get_nama() if (tamu_dalam and hasattr(tamu_dalam, 'get_nama')) else '-'
                if otomatis:
                    print(f'🕓 Checkout otomatis: {nama_tamu} telah check-out dari kamar {id_kamar}.')
                else:
                    print(f'✅ {nama_tamu} telah check-out dari kamar {id_kamar}.')
                return

        if not otomatis:
            print('❌ Kamar tidak ditemukan atau belum terisi.')

    # ===============================
    # Sistem masalah & perbaikan
    # ===============================
    def update_masalah(self):
        """
        Cek setiap kamar untuk masalah baru (menggunakan kamar.buat_masalah_random()).
        Tambahkan masalah baru ke daftar tanpa menimpa masalah lama, dan cegah duplikasi.
        """
        for kamar in self.__daftar_kamar:
            masalah = kamar.buat_masalah_random()
            if masalah:
                entri = (kamar.get_id(), masalah)
                # Tambah hanya jika belum ada entri identik
                if entri not in self.__daftar_masalah:
                    self.__daftar_masalah.append(entri)
                    print(f"⚠️ Masalah baru dilaporkan di kamar {kamar.get_id()}: {masalah}")

    def tampilkan_problem_list(self):
        """Menampilkan daftar masalah aktif (tanpa menghapusnya)."""
        if not self.__daftar_masalah:
            print("✅ Tidak ada masalah saat ini.")
            return

        print("🧾 Daftar Masalah Aktif:")
        for i, (nomor, masalah) in enumerate(self.__daftar_masalah, 1):
            print(f"{i}. Kamar {nomor} - {masalah}")

    def perbaiki_masalah(self, index, keuangan=None, waktu=None, action=None):
        """Memperbaiki salah satu masalah dari daftar dan memotong saldo, waktu, serta action."""
        if 0 <= index < len(self.__daftar_masalah):
            nomor, masalah = self.__daftar_masalah[index]  # ⚠️ jangan pop dulu!

            # 🔒 Cek apakah action masih cukup
            if action and hasattr(action, 'action_left') and action.action_left <= 0:
                print('⚠️ Action kamu sudah habis! Tidak bisa memperbaiki masalah saat ini.')
                return

            # Biaya perbaikan tergantung jenis masalah
            biaya_perbaikan = 30_000
            if 'AC' in masalah:
                biaya_perbaikan = 50_000
            elif 'Lampu' in masalah:
                biaya_perbaikan = 20_000
            elif 'Bocor' in masalah or 'Kebocoran' in masalah:
                biaya_perbaikan = 30_000

            # Potong saldo hotel
            if keuangan:
                keuangan.kurangi_pengeluaran(biaya_perbaikan, tujuan=f'Perbaikan kamar {nomor}')
            else:
                print(f'💸 Pengeluaran: Rp{biaya_perbaikan} untuk perbaikan kamar {nomor}.')

            # Panggil fungsi perbaikan kamar (jika ada)
            for kamar in self.__daftar_kamar:
                if kamar.get_id() == nomor:
                    if hasattr(kamar, 'perbaiki_masalah'):
                        kamar.perbaiki_masalah()
                    break

            # Hapus masalah dari daftar setelah berhasil diperbaiki
            self.__daftar_masalah.pop(index)

            # Kurangi action bar
            if action:
                success = action.gunakan_action(1)
                if not success:
                    print('⚠️ Action tidak cukup untuk memperbaiki masalah (perbaikan dibatalkan).')
                    # Kalau kamu mau, bisa kembalikan masalah ke daftar lagi di sini
                    # self.__daftar_masalah.insert(index, (nomor, masalah))
                    return
        else:
            print('❌ Indeks masalah tidak valid.')


    # ===============================
    # Upgrade Kamar
    # ===============================
    def upgrade_kamar_hotel(self, id_kamar, action_bar):
        """Upgrade kamar dan potong biaya dari saldo hotel.
        Menggunakan ActionBar yang sudah ada (ActionBar.gunakan_action)."""
        biaya_upgrade = {
            'Standard': 500_000,
            'Deluxe': 1_000_000,
            'Suite': 2_000_000
        }

        # Cek action tersisa dulu
        if not hasattr(action_bar, 'action_left'):
            print('⚠️ Action bar tidak valid.')
            return

        if action_bar.action_left <= 0:
            print('⚠️ Action kamu sudah habis! Tunggu pergantian hari untuk melanjutkan.')
            return

        # Cari kamar
        for i, kamar in enumerate(self.__daftar_kamar):
            if str(kamar.get_id()) == str(id_kamar):
                tipe = kamar.get_tipe()

                # Cegah upgrade jika kamar sedang ditempati
                if kamar.apakah_terisi():
                    print(f'🚫 Kamar {id_kamar} sedang ditempati oleh tamu. Tidak dapat di-upgrade!')
                    return

                # 🔒 Cek apakah kamar punya masalah aktif
                for nomor, _ in self.__daftar_masalah:
                    if str(nomor) == str(id_kamar):
                        print(f'🚫 Kamar {id_kamar} masih memiliki masalah! Perbaiki dulu sebelum upgrade.')
                        return

                if tipe == 'VIP':
                    print('🚫 Kamar ini sudah level tertinggi (VIP).')
                    return

                biaya = biaya_upgrade.get(tipe, 0)

                # Pastikan objek keuangan terhubung
                if not hasattr(self, '_Hotel__keuangan') and not hasattr(self, '_Hotel__saldo'):
                    saldo_sekarang = getattr(self, '_Hotel__saldo', None)
                else:
                    saldo_sekarang = self.__keuangan.get_saldo() if hasattr(self, '_Hotel__keuangan') else self.__saldo

                # Cek saldo
                if saldo_sekarang is None or saldo_sekarang < biaya:
                    print(f'❌ Saldo tidak cukup untuk upgrade (butuh Rp{biaya:,.0f}).'.replace(',', '.'))
                    return

                # Potong saldo lewat Keuangan jika tersedia, else pakai __saldo
                if hasattr(self, '_Hotel__keuangan'):
                    self.__keuangan.kurangi_pengeluaran(biaya, tujuan=f'Upgrade kamar {id_kamar}')
                else:
                    self.__saldo -= biaya

                # Lakukan upgrade via module yang benar
                from Kamar.upgrade_manager import upgrade_kamar
                kamar_baru = upgrade_kamar(kamar)

                # Ganti di daftar kamar
                self.__daftar_kamar[i] = kamar_baru

                # Kurangi action via ActionBar.gunakan_action
                success = action_bar.gunakan_action(1)
                if not success:
                    print('⚠️ Gagal mengurangi action meskipun sebelumnya cukup. Periksa ActionBar.')
                else:
                    saldo_now = self.__keuangan.get_saldo() if hasattr(self, '_Hotel__keuangan') else self.__saldo
                    print(f'💰 Saldo sekarang: Rp{saldo_now:,.0f}'.replace(',', '.'))
                return

        print('❌ Kamar dengan ID tersebut tidak ditemukan.')


    # ===============================
    # Tampilan Info
    # ===============================
    def tampilkan_info(self, keuangan=None):
        print(f"\n🏨 Hotel: {self.__nama}")
        print(f"💰 Saldo: Rp{keuangan.get_saldo() if keuangan else self.__saldo}")
        print(f"⭐ Reputasi: {self.__reputasi}/100")
        print(f"🛏️  Jumlah Kamar: {len(self.__daftar_kamar)}")
        print(f"👥 Jumlah Pegawai: {len(self.__daftar_pegawai)}")
        print(f"🧳 Jumlah Tamu: {len(self.__daftar_tamu)}\n")

    # ===============================
    # Getter Tambahan
    # ===============================
    def get_daftar_kamar(self):
        return list(self.__daftar_kamar)

    def get_daftar_pegawai(self):
        return list(self.__daftar_pegawai)

    def get_daftar_tamu(self):
        """Kembalikan list objek Tamu yang sedang menginap (menggunakan list comprehension)."""
        return [kamar.get_tamu() for kamar in self.__daftar_kamar if kamar.apakah_terisi() and hasattr(kamar, 'get_tamu')]

    def get_daftar_masalah(self):
        """Kembalikan salinan daftar masalah (tidak mengembalikan referensi langsung)."""
        return list(self.__daftar_masalah)

    #Design Pattern
    # Tambahan untuk Observer Pattern: Hotel sebagai Observer
    def update(self, subject, ganti_hari):
        """Method yang dipanggil saat subject (Waktu) notify perubahan.
        Di sini, handle update masalah, pemasukan, check-out, dll.
        """
        # Update masalah (seperti sebelumnya)
        self.update_masalah()
 
        # Hitung pemasukan dari tamu (pindah dari main.py)
        total_pemasukan = 0
        for kamar in self.__daftar_kamar:
            if kamar.apakah_terisi():
                tamu = kamar.get_tamu()
                if tamu:
                    harga_per_4jam = kamar.get_harga() / 6
                    total_pemasukan += harga_per_4jam
                    self.__keuangan.tambah_pemasukan(
                        harga_per_4jam,
                        sumber=f'Kamar {kamar.get_id()} (tamu {tamu.get_nama()})'
                    )
 
                    tamu.tambah_jam(4)  # Tambah jam ke tamu
                    sisa_jam = tamu.get_lama_menginap() * 24 - tamu._Tamu__jam_terhitung  # Akses private, adjust jika perlu
 
                    if sisa_jam <= 4 and not getattr(tamu, '_sudah_diberitahu', False):
                        print(f'⚠️  Tamu {tamu.get_nama()} akan check-out pada periode berikutnya.')
                        setattr(tamu, '_sudah_diberitahu', True)
 
                    if sisa_jam <= 0:
                        if hasattr(tamu, '_sudah_diberitahu'):
                            delattr(tamu, '_sudah_diberitahu')
                        print(f'🕓 Tamu {tamu.get_nama()} telah selesai menginap dan akan check-out otomatis.')
                        self.check_out(tamu=tamu, otomatis=True)
 
        if total_pemasukan == 0:
            print('💤 Tidak ada tamu yang sedang menginap, tidak ada pemasukan kali ini.')
 
        # Biaya rutin (seperti sebelumnya)
        if subject.get_jam() in (12, 0):  # subject adalah Waktu
            self.__keuangan.kurangi_pengeluaran(20000, tujuan='Biaya listrik dan air')
 
        # Laporan harian jika ganti hari
        if ganti_hari:
            print('\n🧾 Hari berakhir, laporan keuangan:')
            self.__keuangan.tampilkan_laporan()  # Asumsi __keuangan adalah instance Keuangan