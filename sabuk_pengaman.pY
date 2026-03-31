print("=== KALKULATOR RISIKO ROBOT ===")

# Anggap saja kita punya modal awal $10.000 (sekitar 150 juta Rupiah)
modal_awal = 10000  

# Aturan Emas Wall Street: Maksimal risiko adalah 2% per transaksi
batas_risiko_persen = 2.0

print(f"💵 Modal Awal Kita: ${modal_awal}")
print(f"⚠️ Batas Risiko: {batas_risiko_persen}% per transaksi")

# Komputer menghitung berapa Dolar maksimal yang Boleh Hilang (jika AI salah tebak)
# Rumusnya: Modal * (2 / 100)
maksimal_kerugian = modal_awal * (batas_risiko_persen / 100)

print("\n--------------------------------------------------")
print(f"🛡️ SABUK PENGAMAN AKTIF!")
print(f"Jika robot memutuskan BELI, dan ternyata harga malah turun (AI salah)...")
print(f"Robot akan otomatis memotong kerugian (Stop Loss) di batas maksimal: ${maksimal_kerugian}")
print(f"Sisa uang kita masih ada ${modal_awal - maksimal_kerugian}, sangat aman untuk lanjut trading besok!")
print("--------------------------------------------------")