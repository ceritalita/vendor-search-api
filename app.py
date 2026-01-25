import streamlit as st
import pandas as pd
import io
import os
import datetime

st.set_page_config(page_title="Vendor Search API", layout="wide")
# Membuat 2 kolom untuk Judul dan Logo
# 0.8 untuk judul (kiri), 0.2 untuk logo (kanan)
col_title, col_logo = st.columns([0.8, 0.2])

with col_title:
    st.title("🔍 Vendor Search Engine")
    st.markdown("##### *Created by Asosiasi Procurement Indonesia (API)*")

# Tombol Refresh di pojok kanan atas
col1, col2 = st.columns([0.85, 0.15])

with col2:
    if st.button("🔄 Perbarui Data"):
        st.cache_data.clear()
        st.rerun()

# Menampilkan info update terakhir (Hanya Tanggal)
if os.path.exists("Vendor_API.csv"):
    timestamp = os.path.getmtime("Vendor_API.csv")
    last_upd = datetime.datetime.fromtimestamp(timestamp)
    # Menampilkan tanggal update
    st.caption(f"Data terakhir diperbarui: {last_upd.strftime('%d %B %Y')}")
    # Menampilkan informasi tambahan dengan font/ukuran yang sama
    st.caption("Database diupdate setiap hari Senin. Jika ingin menambahkan vendor atau perubahan informasi lainnya, hubungi Admin API (Lita)")
# ------------------------------------------------

@st.cache_data(ttl=3600)
def load_data():
    # Mencoba membaca CSV dengan berbagai kemungkinan pemisah (koma atau titik koma)
    try:
        # engine='python' membantu mendeteksi pemisah otomatis
        df = pd.read_csv("Vendor_API.csv", sep=None, engine='python')
        # Membersihkan spasi di nama kolom (antisipasi typo)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return str(e)

data = load_data()

if isinstance(data, str):
    st.error(f"File ditemukan tapi tidak bisa dibaca: {data}")
else:
    df = data
    
    # --- BAGIAN SIDEBAR ---
with st.sidebar:
    # 1. Tampilkan Logo di Paling Atas Sidebar
    if os.path.exists("logo_api.png"):
        st.image("logo_api.png", width=100)
    
    st.write("---") # Garis pembatas bawah logo
    
    # 2. Tampilan Filter Kategori
    if 'Kategori' in df.columns:
        # Sidebar Filter
        st.sidebar.header("Filter")
        kategori_list = ["Semua"] + sorted(list(df['Kategori'].unique()))
        selected_kategori = st.sidebar.selectbox("Pilih Kategori", kategori_list)

    # 3. Tampilan disclaimer
        st.sidebar.markdown("---") # Garis pembatas
        st.sidebar.caption("""
        **📌Disclaimer:**
        List vendor dikumpulkan berdasarkan rekomendasi anggota API. 
        
        Mohon melakukan penelusuran lebih lanjut sebelum melakukan transaksi apapun. 
        
        Segala kerugian yang timbul dikarenakan kelalaian individu, di luar tanggung jawab API.
        """)
    # --- BATAS SIDEBAR ---

# Search Box
search_query = st.text_input("Cari Produk, Jasa, atau Nama Vendor:", "")

# Logika Filter
filtered_df = df.copy()
if selected_kategori != "Semua":
    filtered_df = filtered_df[filtered_df['Kategori'] == selected_kategori]

if search_query:
    # Cari di semua kolom teks
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]
    
# Tampilkan Tabel halaman utama
st.write(f"Menampilkan **{len(filtered_df)}** vendor:")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
