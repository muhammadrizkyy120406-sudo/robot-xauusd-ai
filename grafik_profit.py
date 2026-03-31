import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt # Ini alat gambar kita

print("📈 SEDANG MENGGAMBAR PERJALANAN UANGMU...")

# 1. Ambil data & Siapkan AI (Sama seperti sebelumnya)
emas = yf.Ticker("GC=F")
data = emas.history(period="1y")
data['SMA_10'] = data['Close'].rolling(window=10).mean()
data['Harga_Besok'] = data['Close'].shift(-1)
data['Target'] = (data['Harga_Besok'] > data['Close']).astype(int)
data = data.dropna()

split = int(len(data) * 0.8)
data_belajar = data.iloc[:split].copy()
data_ujian = data.iloc[split:].copy()

ai = RandomForestClassifier(n_estimators=100, random_state=42)
ai.fit(data_belajar[['Close', 'SMA_10']], data_belajar['Target'])

# 2. Hitung Profit (Sama seperti sebelumnya)
data_ujian['Prediksi'] = ai.predict(data_ujian[['Close', 'SMA_10']])
data_ujian['Profit_Harian'] = data_ujian['Close'].pct_change()
data_ujian['Profit_Strategi'] = data_ujian['Prediksi'].shift(1) * data_ujian['Profit_Harian']

# 3. HITUNG PERTUMBUHAN UANG KUMULATIF (Ditambah terus)
# Anggap modal awal kita adalah 1 (atau 100%)
data_ujian['Pertumbuhan_Uang'] = (1 + data_ujian['Profit_Strategi']).cumprod()

print("✅ Selesai! Menampilkan grafik di layar...")

# 4. MEMBUAT GRAFIK
plt.figure(figsize=(10, 6))
plt.plot(data_ujian['Pertumbuhan_Uang'], label='Strategi Robot AI', color='green', linewidth=2)
plt.axhline(y=1, color='red', linestyle='--', label='Modal Awal (Titik Nol)')
plt.title('Grafik Pertumbuhan Uang (Backtest XAUUSD)')
plt.xlabel('Tanggal')
plt.ylabel('Kelipatan Modal')
plt.legend()
plt.grid()
plt.show() # Perintah untuk memunculkan jendela grafik