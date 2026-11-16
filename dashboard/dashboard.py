import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Dashboard Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide"
)

st.markdown("""
    <style>
    div[data-testid="stAlert"] {
        min-height: 230px;
        display: flex;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

sns.set(style='darkgrid')

def create_byseason_df(df):
    byseason_df = df.groupby(by="season_day").cnt_day.mean().reset_index()
    byseason_df.rename(columns={
        "season_day": "season",
        "cnt_day": "avg_rental"
    }, inplace=True)
    return byseason_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit_day").cnt_day.mean().reset_index()
    byweather_df.rename(columns={
        "weathersit_day": "weathersit",
        "cnt_day": "avg_rental"
    }, inplace=True)
    return byweather_df

def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by="workingday_day")[["casual_day", "registered_day"]].mean().reset_index()
    byworkingday_df.rename(columns={
        "workingday_day": "workingday",
        "casual_day": "casual",
        "registered_day": "registered"
    }, inplace=True)
    return byworkingday_df

def create_bytime_df(df):
    bytime_df = df.groupby(by="time_category").agg({
        "cnt_hour": "mean",
        "casual_hour": "mean",
        "registered_hour": "mean"
    }).reset_index()
    bytime_df.rename(columns={
        "cnt_hour": "cnt",
        "casual_hour": "casual",
        "registered_hour": "registered"
    }, inplace=True)
    bytime_df['time_category'] = pd.Categorical(
        bytime_df['time_category'],
        ["Pagi (00-10)", "Siang (11-14)", "Sore (15-18)", "Malam (19-23)"]
    )
    return bytime_df

all_df = pd.read_csv("dashboard/main_data.csv")
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

if "valid_date_range" not in st.session_state:
    st.session_state.valid_date_range = (min_date, max_date)

with st.sidebar:
    st.markdown("# 🚲 Bike Sharing")
    st.caption("Dashboard Analisis Penyewaan Sepeda (2011–2012)")
    st.divider()
    
    date_range = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

if isinstance(date_range, tuple) and len(date_range) == 2:
    st.session_state.valid_date_range = date_range

start_date, end_date = st.session_state.valid_date_range

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                 (all_df["dteday"] <= str(end_date))]

byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(main_df)
byworkingday_df = create_byworkingday_df(main_df)
bytime_df = create_bytime_df(main_df)

st.header('Dashboard Analisis Penyewaan Sepeda 🚲')
st.markdown("Ringkasan performa penyewaan sepeda berdasarkan musim, kondisi cuaca, kategori hari, dan klaster waktu.")

col1, col2, col3 = st.columns(3)

with col1:
    avg_daily_rentals = round(main_df["cnt_day"].mean(), 1)
    st.metric("Rata-Rata Sewa Harian", value=f"{avg_daily_rentals:,} sepeda")

with col2:
    avg_hourly_rentals = round(main_df["cnt_hour"].mean(), 1)
    st.metric("Rata-Rata Sewa Per Jam", value=f"{avg_hourly_rentals:,} sepeda")

with col3:
    total_hourly_rentals = main_df["cnt_hour"].sum()
    st.metric("Total Penyewaan Sepeda", value=f"{total_hourly_rentals:,} sepeda")

st.divider()

st.subheader("1. Rata-Rata Penyewaan Harian Berdasarkan Musim dan Kondisi Cuaca")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    y="avg_rental",
    x="season",
    data=byseason_df.sort_values(by="avg_rental", ascending=False),
    palette=colors,
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Berdasarkan Musim", loc="center", fontsize=50, pad=20)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(
    y="avg_rental",
    x="weathersit",
    data=byweather_df.sort_values(by="avg_rental", ascending=False),
    palette=colors,
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Berdasarkan Kondisi Cuaca", loc="center", fontsize=50, pad=20)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

with st.expander("Lihat Insight Musim & Cuaca"):
    st.write(
        "- **Musim:** Musim gugur (*Fall*) mencatat rata-rata penyewaan harian tertinggi (**5.644 sepeda/hari**), "
        "sedangkan musim semi (*Spring*) terendah (**2.604 sepeda/hari**).\n"
        "- **Cuaca:** Kondisi cerah/berawan sebagian (*Clear/Partly Cloudy*) mendominasi dengan rata-rata "
        "**4.877 sepeda/hari**, jauh di atas cuaca hujan/salju ringan (**1.803 sepeda/hari**)."
    )

st.divider()

st.subheader("2. Perbandingan Pengguna Casual vs Registered: Hari Kerja vs Akhir Pekan/Libur")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors_casual = ["#D3D3D3", "#90CAF9"]
    sns.barplot(
        y="casual",
        x="workingday",
        data=byworkingday_df.sort_values(by="casual", ascending=True),
        palette=colors_casual,
        ax=ax
    )
    ax.set_title("Rata-Rata Pengguna Casual / Hari", loc="center", fontsize=45, pad=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors_registered = ["#D3D3D3", "#90CAF9"]
    sns.barplot(
        y="registered",
        x="workingday",
        data=byworkingday_df.sort_values(by="registered", ascending=True),
        palette=colors_registered,
        ax=ax
    )
    ax.set_title("Rata-Rata Pengguna Registered / Hari", loc="center", fontsize=45, pad=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with st.expander("Lihat Insight Perilaku Tipe Pengguna"):
    st.write(
        "- **Pengguna Registered:** Jauh lebih aktif pada hari kerja (*Working Day*) dengan rata-rata **3.978 sepeda/hari** "
        "dibandingkan akhir pekan (**2.959 sepeda/hari**), menunjukkan penggunaan untuk mobilitas rutin.\n"
        "- **Pengguna Casual:** Melonjak lebih dari dua kali lipat pada akhir pekan/libur (*Weekend/Holiday*) sebesar "
        "**1.371 sepeda/hari** dibandingkan hari kerja (**607 sepeda/hari**), menunjukkan penggunaan untuk rekreasi."
    )

st.divider()

st.subheader("3. Rata-Rata Penyewaan Per Jam Berdasarkan Klaster Kategori Waktu")

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors_time = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"]

sns.barplot(
    y="cnt",
    x="time_category",
    data=bytime_df.sort_values(by="time_category"),
    palette=colors_time,
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Total Rata-Rata Sewa / Jam", loc="center", fontsize=42, pad=20)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=26)

sns.barplot(
    y="casual",
    x="time_category",
    data=bytime_df.sort_values(by="time_category"),
    palette=colors_time,
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Rata-Rata Casual / Jam", loc="center", fontsize=42, pad=20)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=26)

sns.barplot(
    y="registered",
    x="time_category",
    data=bytime_df.sort_values(by="time_category"),
    palette=colors_time,
    ax=ax[2]
)
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("Rata-Rata Registered / Jam", loc="center", fontsize=42, pad=20)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=26)

st.pyplot(fig)

with st.expander("Lihat Insight Klaster Kategori Waktu"):
    st.write(
        "- **Puncak Aktivitas:** Klaster **Sore (15–18)** menjadi waktu tersibuk dengan rata-rata **363 sepeda/jam**, "
        "diikuti **Siang (11–14)** (**239 sepeda/jam**), **Malam (19–23)** (**186 sepeda/jam**), dan terendah pada **Pagi (00–10)** (**109 sepeda/jam**).\n"
        "- **Proporsi Pengguna:** Pengguna *registered* selalu mendominasi di seluruh kategori waktu (sekitar 71%–88%), "
        "sementara proporsi tertinggi pengguna *casual* terjadi pada waktu **Siang (11–14)** (~29%)."
    )

st.divider()

st.subheader("Kesimpulan & Rekomendasi Strategis")

col_conc, col_rec = st.columns(2)

with col_conc:
    st.info(
        "**Kesimpulan Utama:**\n"
        "1. Penyewaan tertinggi terjadi pada **musim gugur (Fall)** dan saat **cuaca cerah**, serta turun tajam pada musim semi dan cuaca hujan.\n"
        "2. Pengguna **registered** mendominasi pada **hari kerja**, sedangkan pengguna **casual** meningkat tajam pada **akhir pekan/libur**.\n"
        "3. Puncak penyewaan per jam terjadi pada klaster **Sore (15–18)** dengan dominasi pengguna *registered*."
    )

with col_rec:
    st.success(
        "**Rekomendasi (Action Item):**\n"
        "1. **Optimalisasi Armada & Perawatan:** Pastikan ketersediaan unit maksimal menjelang jam sibuk **Sore (15–18)**, serta jadwalkan perawatan rutin (*maintenance*) besar pada **musim semi (Spring)** atau saat cuaca hujan.\n"
        "2. **Promo Segmen Casual:** Luncurkan paket promo akhir pekan dan jam siang (11–14) untuk menarik penyewa *casual*, disertai penawaran konversi keanggotaan (*membership*)."
    )