import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

print("🤖 ===========================================")
print("   ROBOT TRADING XAUUSD (VERSI 1.0) MENYALA!  ")
print("==============================================")

# --- BAGIAN 1: PERSIAPAN DATA & AI ---
print("\n1. Mengumpulkan data Emas (GC=F) 1 Tahun terakhir...")
emas = yf.Ticker("GC=F")
data = emas.history(period="1y")

data['SMA_10'] = data['Close'].rolling(window=10).mean()
data['Harga_Besok'] = data['Close'].shift(-1)
data['Kunci_Jawaban'] = (data['Harga_Besok'] > data['Close']).astype(int)
data = data.dropna()

soal = data[['Close', 'SMA_10']]
jawaban = data['Kunci_Jawaban']

# --- BAGIAN 2: AI BELAJAR KILAT ---
print("2. AI sedang mempelajari pola masa lalu...")
ai_robot = RandomForestClassifier(n_estimators=100, random_state=42)
ai_robot.fit(soal, jawaban)

# --- BAGIAN 3: AI MENEBAK HARI INI ---
print("3. AI mengamati harga hari ini...")
soal_hari_ini = soal.tail(1)
tebakan = ai_robot.predict(soal_hari_ini)
harga_sekarang = soal_hari_ini['Close'].iloc[0]

# --- BAGIAN 4: SABUK PENGAMAN (MANAJEMEN RISIKO) ---
print("4. Menyiapkan Sabuk Pengaman...")
modal_awal = 10000
batas_risiko_persen = 2.0
maksimal_kerugian = modal_awal * (batas_risiko_persen / 100)

print("\n==============================================")
print("🎯 KEPUTUSAN FINAL ROBOT UNTUK BESOK:")
print("==============================================")
print(f"Harga Emas Saat Ini : ${harga_sekarang:.2f}")

# Jika AI menebak NAIK (1)
if tebakan[0] == 1:
    print("Prediksi AI         : NAIK 🟢🚀")
    print("Rekomendasi         : LAKUKAN PEMBELIAN (BUY)")
    print(f"Sabuk Pengaman      : Jual otomatis (Stop Loss) jika kamu sudah rugi ${maksimal_kerugian}!")
# Jika AI menebak TURUN (0)
else:
    print("Prediksi AI         : TURUN 🔴📉")
    print("Rekomendasi         : JANGAN BELI (TUNGGU / WAIT)")
    print("Sabuk Pengaman      : Uangmu aman. Kita simpan pelurunya untuk besok!")
print("==============================================")