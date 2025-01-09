import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st 

df = pd.read_csv('Surosowan_Stats.csv')

# Menghitung jumlah setiap Studi Path
path_counts = df["Studi Path"].value_counts().reset_index()
path_counts.columns = ["Studi Path", "Jumlah Pendaftar"]
path_counts = path_counts.sort_values(by="Jumlah Pendaftar", ascending=False).reset_index(drop=True)

# Membuat sidebar untuk memilih Studi Path
st.sidebar.title("Filter Dashboard")
all_paths = path_counts["Studi Path"].tolist()
selected_path = st.sidebar.selectbox("Pilih Studi Path:", options=["All Path"] + all_paths)

# Fungsi untuk menghitung total pendaftar dan lulus berdasarkan path
def Sum_Pendaftar(data):
    return len(data)

def Sum_Lulus(data):
    return data['Status Kelulusan'].sum()

# Menentukan warna berdasarkan pilihan
def highlight_path(row):
    if selected_path == "All Path" or row["Studi Path"] == selected_path:
        return "Red"  # Warna mencolok untuk path yang disorot
    else:
        return "Gray"  # Warna abu-abu untuk path lainnya

path_counts["Warna"] = path_counts.apply(highlight_path, axis=1)


# Filter data berdasarkan pilihan pengguna
if selected_path != "All Path":
    filtered_data = df[df["Studi Path"] == selected_path]
else:
    filtered_data = df

# Menghitung total pendaftar dan lulus pada data yang difilter
Total_Pendaftar = Sum_Pendaftar(filtered_data)
Total_Lulus = Sum_Lulus(filtered_data)

# Membuat dashboard utama
st.header(f'Dashboard Surosowan Cyber Academy 2024 {selected_path}')
st.write(f"Menampilkan data untuk path: **{selected_path}**")

# Membagi layout menjadi dua kolom
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label='Total Pendaftar',
        value=f"{Total_Pendaftar:,}"  # Format angka dengan pemisah ribuan
    )
with col2:
    st.metric(
        label='Total Peserta Lulus',
        value=f"{Total_Lulus:,}"  # Format angka dengan pemisah ribuan
    )

# Membuat diagram batang interaktif
fig = px.bar(
    path_counts, 
    x="Studi Path", 
    y="Jumlah Pendaftar",
    title="Jumlah Pendaftar Tiap Path Surosowan Cyber Academy 2024",
    color="Warna",
    color_discrete_map="identity",  # Menggunakan warna spesifik dari kolom
    category_orders={"Studi Path": all_paths},  # Menjaga urutan x-axis sesuai DataFrame terurut
)

fig.update_layout(
    width=700,   # Lebar figur
    height=550,  # Tinggi figur
    showlegend=False           # Menyembunyikan legenda warna
)

# Menampilkan diagram interaktif di Streamlit
st.header(f"Jumlah Pendaftar {selected_path}")
st.plotly_chart(fig, use_container_width=True)