class Keuangan:
    def __init__(self, saldo_awal: float):
        self._saldo = saldo_awal
        self._pemasukan = 0
        self._pengeluaran = 0
 
    def get_saldo(self):
        return self._saldo
 
    def get_pemasukan(self):
        return self._pemasukan
 
    def get_pengeluaran(self):
        return self._pengeluaran
 
    def tambah_pemasukan(self, jumlah: float, sumber: str = 'Tidak diketahui'):
        self._saldo += jumlah
        self._pemasukan += jumlah
        print(f'💵 Pemasukan: Rp{jumlah:,.0f}'.replace(',', '.') +
              f' dari {sumber}. Saldo sekarang: Rp{self._saldo:,.0f}'.replace(',', '.'))
 
    def kurangi_pengeluaran(self, jumlah: float, tujuan: str = 'Tidak diketahui'):
        if jumlah > self._saldo:
            print('⚠️ Saldo tidak cukup untuk pengeluaran ini!')
        else:
            self._saldo -= jumlah
            self._pengeluaran += jumlah
            print(f'💸 Pengeluaran: Rp{jumlah:,.0f}'.replace(',', '.') +
                  f' untuk {tujuan}. Saldo sekarang: Rp{self._saldo:,.0f}'.replace(',', '.'))
 
    def bayar_gaji(self, daftar_pegawai):
        total_gaji = sum(pegawai.get_gaji() for pegawai in daftar_pegawai)
        if total_gaji > self._saldo:
            print('❌ Gagal membayar gaji! Saldo hotel tidak cukup.')
        else:
            self._saldo -= total_gaji
            self._pengeluaran += total_gaji
            print(f'🧾 Total gaji dibayar: Rp{total_gaji:,.0f}'.replace(',', '.') +
                  f'. Saldo tersisa: Rp{self._saldo:,.0f}'.replace(',', '.'))
 
    def tampilkan_laporan(self):
        print('===== Laporan Keuangan Hotel =====')
        print(f'Saldo Saat Ini    : Rp{self._saldo:,.0f}'.replace(',', '.'))
        print(f'Total Pemasukan   : Rp{self._pemasukan:,.0f}'.replace(',', '.'))
        print(f'Total Pengeluaran : Rp{self._pengeluaran:,.0f}'.replace(',', '.'))
        print('=================================')
