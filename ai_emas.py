import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split # Alat untuk membagi data belajar & ujian
from sklearn.metrics import accuracy_score # Alat untuk menghitung nilai rapor (0-100)

print("1. Mengambil data Emas (GC=F) 1 Tahun...")
emas = yf.Ticker("GC=F")
data = emas.history(period="1y")

print("2. Menyiapkan Soal dan Kunci Jawaban...")
data['SMA_10'] = data['Close'].rolling(window=10).mean()
data['Harga_Besok'] = data['Close'].shift(-1)
data['Kunci_Jawaban'] = (data['Harga_Besok'] > data['Close']).astype(int)
data = data.dropna()

soal = data[['Close', 'SMA_10']]
jawaban = data['Kunci_Jawaban']

print("3. Membagi data: 80% untuk Belajar, 20% untuk Ujian...")
# test_size=0.2 artinya 20% data ditaruh di belakang khusus untuk ujian
soal_belajar, soal_ujian, jawaban_belajar, jawaban_ujian = train_test_split(soal, jawaban, test_size=0.2, shuffle=False)

print("4. AI sedang belajar dari 80% data. Ssssttt... 🤫")
ai_robot = RandomForestClassifier(n_estimators=100, random_state=42)
ai_robot.fit(soal_belajar, jawaban_belajar)

print("5. AI sedang mengerjakan Ujian pada 20% data sisanya...")
# AI menebak soal ujian (tanpa melihat kunci jawaban!)
tebakan_ujian = ai_robot.predict(soal_ujian)

print("6. Mengoreksi jawaban dan menghitung Nilai Rapor...")
# Kita bandingkan tebakan AI dengan kunci jawaban asli
nilai_akurasi = accuracy_score(jawaban_ujian, tebakan_ujian) * 100

print("\n==================================================")
print(f"🎓 NILAI RAPOR AI KAMU: {nilai_akurasi:.2f} dari 100")
if nilai_akurasi > 50:
    print("🌟 Hebat! AI kamu lebih pintar dari sekadar menebak koin (50/50)!")
else:
    print("😅 Wah, AI kamu nilainya di bawah 50. Butuh lebih banyak indikator (Pelajaran) nih!")
print("==================================================")