import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set gaya visual
sns.set(style='dark')

# Load cleaned data
all_df = pd.read_csv("main_data.csv")

# Mengubah kolom tahun, bulan, hari, dan jam menjadi kolom datetime untuk analisis waktu
all_df['datetime'] = pd.to_datetime(all_df[['year', 'month', 'day', 'hour']])

# Filter data berdasarkan rentang waktu
min_date = all_df["datetime"].min()
max_date = all_df["datetime"].max()

with st.sidebar:
    # Menambahkan logo perusahaan (gunakan URL gambar yang tersedia)
    st.image("image.png")
    
    # Mengambil rentang waktu dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataset berdasarkan rentang waktu yang dipilih
main_df = all_df[(all_df["datetime"] >= str(start_date)) & 
                 (all_df["datetime"] <= str(end_date))]

# Menampilkan header aplikasi
st.header('Dashboard Analisis Kualitas Udara Kota Shunyi :sparkles:')

# Analisis Rata-Rata Polutan per Bulan
st.subheader('Rata-rata Konsentrasi PM2.5 per Bulan')
monthly_avg = main_df.groupby(['year', 'month'])['PM2.5'].mean().reset_index()
monthly_avg['datetime'] = pd.to_datetime(monthly_avg[['year', 'month']].assign(day=1))
monthly_avg.sort_values(by='datetime', inplace=True)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_avg["datetime"],
    monthly_avg["PM2.5"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.set_title('Rata-rata Konsentrasi PM2.5 per Bulan', fontsize=20)
ax.set_ylabel('Konsentrasi PM2.5 (µg/m³)', fontsize=15)
ax.set_xlabel('Bulan', fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

# Menemukan bulan dengan rata-rata konsentrasi PM2.5 tertinggi
highest_pm25_month = monthly_avg.loc[monthly_avg['PM2.5'].idxmax()]

st.subheader('Bulan dengan Rata-rata Konsentrasi PM2.5 Tertinggi')
st.write(f"Bulan: {highest_pm25_month['month']} Tahun: {highest_pm25_month['year']} - Rata-rata PM2.5: {highest_pm25_month['PM2.5']:.2f} µg/m³")

# Hubungan antara TEMP dan PM2.5, PM10
st.subheader("Hubungan antara Suhu Udara (TEMP) dan Konsentrasi PM2.5 serta PM10")

# Scatter plot TEMP vs PM2.5
fig, ax = plt.subplots(figsize=(16, 8))
sns.scatterplot(data=main_df, x='TEMP', y='PM2.5', ax=ax, color='blue', label='PM2.5', alpha=0.6)
sns.scatterplot(data=main_df, x='TEMP', y='PM10', ax=ax, color='orange', label='PM10', alpha=0.6)
ax.set_title('Hubungan Suhu Udara (TEMP) dengan PM2.5 dan PM10', fontsize=20)
ax.set_xlabel('Suhu Udara (°C)', fontsize=15)
ax.set_ylabel('Konsentrasi (µg/m³)', fontsize=15)
ax.legend()
st.pyplot(fig)

# Menampilkan Statistik Temperatur, Tekanan, dan Kelembaban
st.subheader("Statistik Temperatur, Tekanan, dan Kelembaban")
col1, col2, col3 = st.columns(3)

with col1:
    avg_temp = main_df['TEMP'].mean()
    st.metric("Rata-rata Temperatur (°C)", value=f"{avg_temp:.2f}")

with col2:
    avg_pres = main_df['PRES'].mean()
    st.metric("Rata-rata Tekanan (hPa)", value=f"{avg_pres:.2f}")

with col3:
    avg_dewp = main_df['DEWP'].mean()
    st.metric("Rata-rata Titik Embun (°C)", value=f"{avg_dewp:.2f}")

# Menampilkan rata-rata konsentrasi polutan lainnya jika diperlukan
st.subheader("Konsentrasi Rata-rata SO2 dan NO2 per Bulan")
monthly_so2_no2_avg = main_df.groupby(['year', 'month']).agg({
    'SO2': 'mean',
    'NO2': 'mean'
}).reset_index()
monthly_so2_no2_avg['datetime'] = pd.to_datetime(monthly_so2_no2_avg[['year', 'month']].assign(day=1))

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_so2_no2_avg['datetime'],
    monthly_so2_no2_avg['SO2'],
    marker='o',
    linewidth=2,
    label='SO2',
    color="#FFA07A"
)
ax.plot(
    monthly_so2_no2_avg['datetime'],
    monthly_so2_no2_avg['NO2'],
    marker='o',
    linewidth=2,
    label='NO2',
    color="#20B2AA"
)
ax.set_title('Rata-rata Konsentrasi SO2 dan NO2 per Bulan', fontsize=20)
ax.set_ylabel('Konsentrasi (µg/m³)', fontsize=15)
ax.set_xlabel('Bulan', fontsize=15)
ax.legend()
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)
