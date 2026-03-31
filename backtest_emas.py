import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

print("🚀 MEMULAI PROSES BACKTESTING (SIMULASI MASA LALU)...")

# 1. Ambil data 1 tahun
emas = yf.Ticker("GC=F")
data = emas.history(period="1y")

# 2. Siapkan indikator dan kunci jawaban (seperti di Phase 3)
data['SMA_10'] = data['Close'].rolling(window=10).mean()
data['Harga_Besok'] = data['Close'].shift(-1)
data['Target'] = (data['Harga_Besok'] > data['Close']).astype(int)
data = data.dropna()

# 3. Bagi data: 80% untuk AI Belajar, 20% untuk Ujian (Backtest)
split = int(len(data) * 0.8)
data_belajar = data.iloc[:split].copy()
data_ujian = data.iloc[split:].copy()

# 4. AI Belajar dari masa lalu
ai = RandomForestClassifier(n_estimators=100, random_state=42)
ai.fit(data_belajar[['Close', 'SMA_10']], data_belajar['Target'])

print("✅ AI Selesai Belajar. Sekarang mencoba bertransaksi di data ujian...")

# 5. SIMULASI TRANSAKSI
# Robot menebak di data ujian
data_ujian['Prediksi'] = ai.predict(data_ujian[['Close', 'SMA_10']])

# Menghitung keuntungan harian (dalam persen)
data_ujian['Profit_Harian'] = data_ujian['Close'].pct_change()

# Jika robot prediksi NAIK (1), kita dapat profit harian besoknya.
# Jika robot prediksi TURUN (0), kita diam saja (profit = 0).
data_ujian['Profit_Strategi'] = data_ujian['Prediksi'].shift(1) * data_ujian['Profit_Harian']

# 6. HITUNG TOTAL KEUNTUNGAN AKHIR
total_profit = (data_ujian['Profit_Strategi'].sum()) * 100

print("\n==============================================")
print(f"📊 HASIL BACKTEST (20% DATA TERAKHIR):")
print(f"💰 Total Keuntungan/Kerugian: {total_profit:.2f}%")
print("==============================================")

if total_profit > 0:
    print("🎊 SELAMAT! Robotmu menghasilkan uang di masa lalu!")
else:
    print("📉 WADUH! Robotmu rugi. Mungkin perlu strategi tambahan.")