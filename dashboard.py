import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import plotly.colors as pc

# Membaca dataset
df = pd.read_csv('Surosowan_Stats.csv')

# Menghitung jumlah setiap Studi Path
path_counts = df["Studi Path"].value_counts().reset_index()
path_counts.columns = ["Studi Path", "Jumlah Pendaftar"]
path_counts = path_counts.sort_values(by="Jumlah Pendaftar", ascending=False).reset_index(drop=True)

# Fungsi-fungsi penghitungan
def Sum_Pendaftar(data):
    return len(data)

def Sum_Diterima(data):
    return data['Status Diterima'].sum()

def Sum_Ditolak(data):
    return data[data['Status Diterima'] == 0].shape[0]

def Sum_Lulus(data):
    return data['Status Kelulusan'].sum()

def Sum_Daerah(data):
    return len(data['Provinsi'])

def Sum_Banten(data):
    return data[data['Provinsi'] == 'Banten'].shape[0]

# Menghitung total data secara keseluruhan
Total_Pendaftar = Sum_Pendaftar(df)
Total_Diterima = Sum_Diterima(df)
Total_Ditolak = Sum_Ditolak(df)
Total_Lulus = Sum_Lulus(df)
Total_provinsi = Sum_Daerah(df)
Total_Banten = Sum_Banten(df)

# Membuat palet warna dinamis
unique_colors = pc.qualitative.Set2

# Judul dan Deskripsi
st.title("Dashboard Surosowan Cyber Academy 2024")
st.markdown("### Ringkasan Data Pendaftar")
st.markdown("Dashboard ini memberikan gambaran mengenai jumlah pendaftar, status diterima, kelulusan, dan distribusi berdasarkan jalur studi di Surosowan Cyber Academy 2024.")

# Baris 1: Indikator Utama
st.markdown("---")
st.markdown("#### Indikator Utama")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Pendaftar", value=f"{Total_Pendaftar}")

with col2:
    st.metric(label="Total Diterima", value=f"{Total_Diterima}")

with col3:
    st.metric(label="Total Ditolak", value=f"{Total_Ditolak}")

with col4:
    st.metric(label="Total Lulus", value=f"{Total_Lulus}")

# Baris 2: Grafik Distribusi Studi Path
st.markdown("---")
st.markdown("#### Distribusi Jumlah Pendaftar per Studi Path")
st.write("Grafik berikut menunjukkan jumlah pendaftar yang memilih masing-masing jalur studi")
fig = px.bar(
    path_counts, 
    x="Studi Path", 
    y="Jumlah Pendaftar", 
    color="Studi Path",
    color_discrete_sequence=unique_colors,
    title="Distribusi Jumlah Pendaftar per Studi Path"
)
fig.update_layout(width=900, height=500)
st.plotly_chart(fig, use_container_width=True)



# Baris 3: Status Diterima dan Ditolak
st.markdown("---")
st.markdown("#### Status Diterima dan Ditolak")
st.write("Grafik berikut menunjukkan perbandingan jumlah peserta yang diterima dan tidak diterima berdasarkan jalur studi")
accept_count = df.groupby(['Studi Path', 'Status Diterima']).size().unstack(fill_value=0)
fig2 = go.Figure(data=[
    go.Bar(name='Diterima', x=accept_count.index, y=accept_count[1], marker_color='green'),
    go.Bar(name='Tidak Diterima', x=accept_count.index, y=accept_count[0], marker_color='red')
])
fig2.update_layout(
    title="Jumlah Pendaftar Diterima dan Tidak Diterima per Studi Path",
    barmode='group',
    xaxis_title='Studi Path',
    yaxis_title='Jumlah Pendaftar',
    width=900, height=500
)
st.plotly_chart(fig2, use_container_width=True)

# Baris 4: Pie Chart Pekerjaan
st.markdown("---")
st.markdown("#### Distribusi Pekerjaan Pendaftar")
st.write("Pie chart berikut menunjukkan persentase pekerjaan peserta pendaftar")
Job_Status = df["Pekerjaan"].value_counts().reset_index()
Job_Status.columns = ["Pekerjaan", "Jumlah Pendaftar"]
fig3 = px.pie(
    Job_Status,
    names="Pekerjaan",
    values="Jumlah Pendaftar",
    title="Persentase Pekerjaan Pendaftar"
)
fig3.update_layout(width=900, height=500)
st.plotly_chart(fig3, use_container_width=True)

# Baris 5: Distribusi Daerah
st.markdown("---")
st.markdown("#### Distribusi Daerah Pendaftar")
st.write("Grafik berikut menampilkan jumlah pendaftar dari berbagai provinsi")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Total Daerah Terlibat", value=f"{Total_provinsi}")

with col2:
    st.metric(label="Total dari Banten", value=f"{Total_Banten}")

Province_Count = df["Provinsi"].value_counts().reset_index()
Province_Count.columns = ["Provinsi", "Jumlah Pendaftar"]

# Membuat diagram batang interaktif menggunakan Plotly
fig4 = px.bar(
    Province_Count, 
    x="Provinsi", 
    y="Jumlah Pendaftar", 
    color='Provinsi',
    title="Distribusi Jumlah Pendaftar Berdasarkan Provinsi"
)
fig4.update_layout(
    width=900,   # Lebar figur
    height=500,   # Tinggi figur
    title_font=dict(family="Arial", size=15, color="black", weight="bold"),
)

st.plotly_chart(fig4, use_container_width=True)
