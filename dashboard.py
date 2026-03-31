import streamlit as st
from yahooquery import Ticker # Alat baru kita
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="XAUUSD AI Dashboard", layout="wide")

st.title("📈 Dashboard Trading Emas (XAUUSD) v1.0")
st.write("Sistem Prediksi Harga berbasis Machine Learning (Jalur Stabil)")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Pengaturan Robot")
modal = st.sidebar.number_input("Modal Investasi ($)", value=10000)
risiko = st.sidebar.slider("Batas Risiko (%)", 0.5, 5.0, 2.0)

# --- PROSES DATA & AI ---
@st.cache_data(ttl=3600)
def ambil_data_dan_prediksi():
    try:
        # Menggunakan yahooquery sebagai pengganti yfinance
        t = Ticker('GC=F')
        data = t.history(period='1y')
        
        # Penyesuaian format data dari yahooquery ke pandas
        if isinstance(data, pd.DataFrame) and not data.empty:
            # Jika data berbentuk multi-index, kita rapikan
            if 'adjclose' in data.columns:
                data = data.rename(columns={'adjclose': 'Close'})
            
            # Reset index agar kolom Date bisa dibaca
            data = data.reset_index()
            data = data.set_index('date')
        else:
            return None, None, None

        # Tambah Indikator
        data['SMA_10'] = data['Close'].rolling(window=10).mean()
        data['Harga_Besok'] = data['Close'].shift(-1)
        data['Kunci_Jawaban'] = (data['Harga_Besok'] > data['Close']).astype(int)
        df = data.dropna().copy()
        
        # Latih AI
        soal = df[['Close', 'SMA_10']]
        jawaban = df['Kunci_Jawaban']
        ai = RandomForestClassifier(n_estimators=100, random_state=42)
        ai.fit(soal, jawaban)
        
        # Prediksi
        soal_terakhir = soal.tail(1)
        prediksi = ai.predict(soal_terakhir)[0]
        harga_skrg = soal_terakhir['Close'].iloc[0]
        
        return df, prediksi, harga_skrg
    except Exception as e:
        return None, None, None

# Eksekusi
df_tabel, hasil_prediksi, harga_hari_ini = ambil_data_dan_prediksi()

if df_tabel is not None:
    # --- TAMPILAN UTAMA ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 Grafik Harga Emas 30 Hari Terakhir")
        st.line_chart(df_tabel['Close'].tail(30))

    with col2:
        st.subheader("🤖 Rekomendasi AI")
        if hasil_prediksi == 1:
            st.success("PREDIKSI: NAIK 🟢")
            st.metric(label="Harga Saat Ini", value=f"${harga_hari_ini:.2f}", delta="📈 BUY")
        else:
            st.error("PREDIKSI: TURUN 🔴")
            st.metric(label="Harga Saat Ini", value=f"${harga_hari_ini:.2f}", delta="📉 WAIT", delta_color="inverse")
        
        rugi_max = modal * (risiko / 100)
        st.info(f"🛡️ **Safety Info:**\nJangan rugi lebih dari **${rugi_max:.2f}**!")

    st.divider()
    st.write("Data Tabel (5 Hari Terakhir):")
    st.dataframe(df_tabel[['Close', 'SMA_10']].tail(5))
else:
    st.error("🛑 Server data sedang sibuk. Mohon tunggu 5 menit dan klik 'Rerun' di menu kanan atas.")