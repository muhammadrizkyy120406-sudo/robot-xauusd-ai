import yfinance as yf
import pandas as pd

print("1. Menarik data Emas (GC=F)...")
emas = yf.Ticker("GC=F")
data_harga = emas.history(period="1mo")

print("2. Menghitung rata-rata harga (SMA 10 Hari)...")
data_harga['SMA_10'] = data_harga['Close'].rolling(window=10).mean()
data_harga = data_harga.dropna()

print("3. Memikirkan keputusan Beli/Jual...")

# Ini adalah fungsi untuk menentukan sinyal
def tentukan_sinyal(baris):
    if baris['Close'] > baris['SMA_10']:
        return 'BELI 🟢'
    else:
        return 'JUAL 🔴'

# Kita terapkan fungsi di atas ke dalam tabel data kita untuk membuat kolom 'Sinyal'
data_harga['Sinyal'] = data_harga.apply(tentukan_sinyal, axis=1)

print("Berhasil! Ini rekomendasi robot untuk 5 hari terakhir:")
# Tampilkan Harga, Rata-rata, dan Sinyalnya!
print(data_harga[['Close', 'SMA_10', 'Sinyal']].tail(5))