from Kamar.class_turunan_kamar import Standard, Deluxe, Suite, VIP
 
def upgrade_kamar(kamar):
    tipe_upgrade = {
        "Standard": Deluxe,
        "Deluxe": Suite,
        "Suite": VIP
    }
 
    tipe_sekarang = kamar.get_tipe()
 
    if tipe_sekarang not in tipe_upgrade:
        print(f"❌ Kamar {kamar.get_id()} sudah level tertinggi (VIP).")
        return kamar
 
    kelas_baru = tipe_upgrade[tipe_sekarang]
    kamar_baru = kelas_baru(kamar.get_id())
    print(f"✅ Kamar {kamar.get_id()} berhasil di-upgrade ke {kamar_baru.get_tipe()}!")
    return kamar_baru