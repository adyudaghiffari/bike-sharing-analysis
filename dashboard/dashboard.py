
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# ==================================================
# 1. PENGATURAN HALAMAN
# ==================================================

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ==================================================
# 2. MENENTUKAN LOKASI DATASET
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

day_clean_path = DATA_DIR / "day_clean.csv"
hour_clean_path = DATA_DIR / "hour_clean.csv"

day_raw_path = DATA_DIR / "day.csv"
hour_raw_path = DATA_DIR / "hour.csv"

# Mengutamakan data hasil cleaning dari notebook
if day_clean_path.exists() and hour_clean_path.exists():
    DAY_PATH = day_clean_path
    HOUR_PATH = hour_clean_path
    DATA_SOURCE = "Data hasil cleaning notebook"

# Jika data hasil cleaning belum tersedia, gunakan data asli
elif day_raw_path.exists() and hour_raw_path.exists():
    DAY_PATH = day_raw_path
    HOUR_PATH = hour_raw_path
    DATA_SOURCE = "Dataset asli (data cleaning belum tersedia)"

else:
    st.error(
        "Dataset tidak ditemukan. Pastikan folder data "
        "berisi day.csv dan hour.csv, atau day_clean.csv "
        "dan hour_clean.csv."
    )
    st.stop()


# ==================================================
# 3. MEMBACA DATASET
# ==================================================

@st.cache_data
def load_data(day_path, hour_path):
    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)

    # Mengubah kolom tanggal ke format datetime
    day_df["dteday"] = pd.to_datetime(
        day_df["dteday"],
        errors="coerce"
    )

    hour_df["dteday"] = pd.to_datetime(
        hour_df["dteday"],
        errors="coerce"
    )

    return day_df, hour_df


day_df, hour_df = load_data(
    str(DAY_PATH),
    str(HOUR_PATH)
)

# Memastikan kolom yang dibutuhkan tersedia
required_day = {
    "dteday", "cnt", "casual", "registered",
    "weathersit", "workingday"
}

required_hour = {
    "dteday", "cnt", "casual", "registered",
    "weathersit", "workingday", "hr", "weekday"
}

if not required_day.issubset(day_df.columns):
    st.error("Kolom yang dibutuhkan tidak lengkap pada day.csv.")
    st.stop()

if not required_hour.issubset(hour_df.columns):
    st.error("Kolom yang dibutuhkan tidak lengkap pada hour.csv.")
    st.stop()

# Membuang baris yang tanggalnya tidak terbaca
day_df = day_df.dropna(subset=["dteday"]).copy()
hour_df = hour_df.dropna(subset=["dteday"]).copy()

if day_df.empty or hour_df.empty:
    st.error("Dataset kosong atau tidak memiliki tanggal yang valid.")
    st.stop()


# ==================================================
# 4. LABEL KATEGORI
# ==================================================

WEATHER_LABELS = {
    1: "Cerah / berawan ringan",
    2: "Berkabut / berawan",
    3: "Hujan ringan / salju ringan",
    4: "Cuaca buruk"
}

WORKINGDAY_LABELS = {
    0: "Hari non-kerja",
    1: "Hari kerja"
}

WEEKDAY_LABELS = {
    0: "Minggu",
    1: "Senin",
    2: "Selasa",
    3: "Rabu",
    4: "Kamis",
    5: "Jumat",
    6: "Sabtu"
}

TIME_ORDER = [
    "Dini hari",
    "Pagi",
    "Siang",
    "Sore",
    "Malam"
]


# ==================================================
# 5. JUDUL DASHBOARD
# ==================================================

st.title("🚲 Bike Sharing Dashboard")

st.markdown(
    """
    Dashboard ini digunakan untuk menganalisis pola penyewaan sepeda
    berdasarkan waktu, kondisi cuaca, dan jenis pengguna.

    Data yang digunakan mencakup periode tahun 2011–2012.
    """
)

if "cleaning" not in DATA_SOURCE.lower():
    st.info(
        "Dashboard sedang menggunakan dataset asli. "
        "Agar menggunakan hasil cleaning notebook, simpan "
        "day_clean.csv dan hour_clean.csv ke folder data."
    )
else:
    st.success("Dashboard menggunakan data hasil cleaning notebook.")

st.caption(f"Sumber data: {DATA_SOURCE}")


# ==================================================
# 6. FILTER DASHBOARD
# ==================================================

st.sidebar.title("Filter Data")

min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

selected_dates = st.sidebar.date_input(
    "Rentang tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Menangani kondisi ketika pengguna baru memilih
# satu tanggal atau rentang tanggal belum lengkap
if isinstance(selected_dates, (tuple, list)):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif len(selected_dates) == 1:
        start_date = end_date = selected_dates[0]
    else:
        start_date, end_date = min_date, max_date
else:
    start_date = end_date = selected_dates

# Pilihan jenis hari
day_type = st.sidebar.selectbox(
    "Jenis hari",
    [
        "Semua",
        "Hari kerja",
        "Hari non-kerja"
    ]
)

# Pilihan kondisi cuaca
weather_codes = sorted(
    set(
        pd.to_numeric(day_df["weathersit"], errors="coerce")
        .dropna().astype(int).unique()
    )
    |
    set(
        pd.to_numeric(hour_df["weathersit"], errors="coerce")
        .dropna().astype(int).unique()
    )
)

selected_weather = st.sidebar.multiselect(
    "Kondisi cuaca",
    options=weather_codes,
    default=weather_codes,
    format_func=lambda code: WEATHER_LABELS.get(
        code, f"Kategori {code}"
    )
)


# ==================================================
# 7. FILTER DATA BERDASARKAN PILIHAN PENGGUNA
# ==================================================

start_timestamp = pd.Timestamp(start_date)
end_timestamp = pd.Timestamp(end_date)

filtered_day_df = day_df[
    (day_df["dteday"] >= start_timestamp)
    & (day_df["dteday"] <= end_timestamp)
    & (day_df["weathersit"].isin(selected_weather))
].copy()

filtered_hour_df = hour_df[
    (hour_df["dteday"] >= start_timestamp)
    & (hour_df["dteday"] <= end_timestamp)
    & (hour_df["weathersit"].isin(selected_weather))
].copy()

# Filter hari kerja / non-kerja
if day_type == "Hari kerja":
    filtered_day_df = filtered_day_df[
        filtered_day_df["workingday"] == 1
    ]

    filtered_hour_df = filtered_hour_df[
        filtered_hour_df["workingday"] == 1
    ]

elif day_type == "Hari non-kerja":
    filtered_day_df = filtered_day_df[
        filtered_day_df["workingday"] == 0
    ]

    filtered_hour_df = filtered_hour_df[
        filtered_hour_df["workingday"] == 0
    ]

if filtered_day_df.empty or filtered_hour_df.empty:
    st.warning(
        "Tidak ada data yang sesuai dengan filter. "
        "Coba ubah rentang tanggal, jenis hari, atau kondisi cuaca."
    )
    st.stop()


# ==================================================
# 8. RINGKASAN PENYEWAAN
# ==================================================

total_rentals = filtered_day_df["cnt"].sum()
total_casual = filtered_day_df["casual"].sum()
total_registered = filtered_day_df["registered"].sum()
average_daily_rentals = filtered_day_df["cnt"].mean()

st.subheader("Ringkasan Penyewaan Sepeda")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Penyewaan",
    f"{total_rentals:,.0f}"
)

col2.metric(
    "Pengguna Kasual",
    f"{total_casual:,.0f}"
)

col3.metric(
    "Pengguna Terdaftar",
    f"{total_registered:,.0f}"
)

col4.metric(
    "Rata-rata Penyewaan Harian",
    f"{average_daily_rentals:,.0f}"
)

st.caption(
    f"Periode: {start_date.strftime('%d %b %Y')} "
    f"sampai {end_date.strftime('%d %b %Y')}"
)


# ==================================================
# 9. TAB DASHBOARD
# ==================================================

tab_overview, tab_time, tab_weather, tab_users = st.tabs(
    [
        "Ringkasan",
        "Pola Waktu",
        "Kondisi Cuaca",
        "Jenis Pengguna"
    ]
)


# ==================================================
# 10. TAB RINGKASAN
# ==================================================

with tab_overview:
    st.subheader("Tren Penyewaan Harian")

    daily_trend = (
        filtered_day_df
        .sort_values("dteday")
        .copy()
    )

    fig_trend = px.line(
        daily_trend,
        x="dteday",
        y="cnt",
        markers=True,
        title="Jumlah Penyewaan Sepeda per Hari",
        labels={
            "dteday": "Tanggal",
            "cnt": "Jumlah Penyewaan"
        },
        template="plotly_white"
    )

    fig_trend.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

    st.markdown(
        """
        **Cara membaca grafik:** sumbu horizontal menunjukkan tanggal,
        sedangkan sumbu vertikal menunjukkan jumlah penyewaan sepeda.
        Gunakan grafik ini untuk melihat perubahan permintaan selama
        periode yang dipilih.
        """
    )


# ==================================================
# 11. TAB POLA WAKTU
# ==================================================

with tab_time:
    st.subheader("Penyewaan Berdasarkan Jam")

    hourly_summary = (
        filtered_hour_df
        .groupby(["workingday", "hr"], as_index=False)["cnt"]
        .mean()
    )

    hourly_summary["Jenis Hari"] = (
        hourly_summary["workingday"]
        .map(WORKINGDAY_LABELS)
    )

    fig_hourly = px.line(
        hourly_summary,
        x="hr",
        y="cnt",
        color="Jenis Hari",
        markers=True,
        title="Rata-rata Penyewaan Berdasarkan Jam",
        labels={
            "hr": "Jam",
            "cnt": "Rata-rata Penyewaan",
            "Jenis Hari": "Jenis Hari"
        },
        template="plotly_white"
    )

    fig_hourly.update_xaxes(
        tickmode="linear",
        dtick=1
    )

    st.plotly_chart(
        fig_hourly,
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("Pola Penyewaan Berdasarkan Hari dan Jam")

    heatmap_source = filtered_hour_df.copy()

    heatmap_source["Nama Hari"] = (
        heatmap_source["weekday"]
        .map(WEEKDAY_LABELS)
    )

    weekday_order = [
        "Minggu", "Senin", "Selasa", "Rabu",
        "Kamis", "Jumat", "Sabtu"
    ]

    heatmap_data = (
        heatmap_source
        .groupby(["Nama Hari", "hr"])["cnt"]
        .mean()
        .reset_index()
    )

    heatmap_pivot = heatmap_data.pivot(
        index="Nama Hari",
        columns="hr",
        values="cnt"
    )

    heatmap_pivot = heatmap_pivot.reindex(weekday_order)

    fig_heatmap = px.imshow(
        heatmap_pivot,
        aspect="auto",
        color_continuous_scale="YlGnBu",
        labels={
            "x": "Jam",
            "y": "Hari",
            "color": "Rata-rata Penyewaan"
        },
        title="Heatmap Rata-rata Penyewaan"
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )

    st.markdown(
        """
        **Cara membaca grafik:** line chart membandingkan pola permintaan
        berdasarkan jam pada hari kerja dan non-kerja. Heatmap membantu
        menemukan kombinasi hari dan jam dengan rata-rata penyewaan tinggi.
        """
    )


# ==================================================
# 12. TAB KONDISI CUACA
# ==================================================

with tab_weather:
    st.subheader("Penyewaan Berdasarkan Kondisi Cuaca")

    weather_source = filtered_day_df.copy()

    weather_source["Kategori Cuaca"] = (
        weather_source["weathersit"]
        .map(WEATHER_LABELS)
        .fillna("Kategori tidak diketahui")
    )

    weather_summary = (
        weather_source
        .groupby(
            ["weathersit", "Kategori Cuaca"],
            as_index=False
        )
        .agg(
            rata_rata_penyewaan=("cnt", "mean"),
            jumlah_hari=("cnt", "count")
        )
        .sort_values("weathersit")
    )

    fig_weather = px.bar(
        weather_summary,
        x="Kategori Cuaca",
        y="rata_rata_penyewaan",
        hover_data=["jumlah_hari"],
        title="Rata-rata Penyewaan per Kategori Cuaca",
        labels={
            "Kategori Cuaca": "Kondisi Cuaca",
            "rata_rata_penyewaan": "Rata-rata Penyewaan",
            "jumlah_hari": "Jumlah Hari"
        },
        template="plotly_white"
    )

    st.plotly_chart(
        fig_weather,
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("Sebaran Penyewaan pada Setiap Kondisi Cuaca")

    fig_weather_box = px.box(
        weather_source,
        x="Kategori Cuaca",
        y="cnt",
        points="outliers",
        title="Distribusi Penyewaan Harian Berdasarkan Cuaca",
        labels={
            "Kategori Cuaca": "Kondisi Cuaca",
            "cnt": "Jumlah Penyewaan"
        },
        template="plotly_white"
    )

    st.plotly_chart(
        fig_weather_box,
        use_container_width=True
    )

    st.dataframe(
        weather_summary[
            [
                "Kategori Cuaca",
                "rata_rata_penyewaan",
                "jumlah_hari"
            ]
        ].rename(
            columns={
                "rata_rata_penyewaan": "Rata-rata Penyewaan",
                "jumlah_hari": "Jumlah Hari"
            }
        ).round(2),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        **Cara membaca grafik:** bar chart membandingkan rata-rata
        penyewaan pada setiap kondisi cuaca. Boxplot memperlihatkan
        sebaran data sehingga variasi penyewaan dapat dibandingkan.
        """
    )


# ==================================================
# 13. TAB JENIS PENGGUNA
# ==================================================

with tab_users:
    st.subheader("Perbandingan Jenis Pengguna")

    user_totals = pd.DataFrame(
        {
            "Jenis Pengguna": [
                "Kasual",
                "Terdaftar"
            ],
            "Total Penyewaan": [
                total_casual,
                total_registered
            ]
        }
    )

    fig_user_total = px.bar(
        user_totals,
        x="Jenis Pengguna",
        y="Total Penyewaan",
        color="Jenis Pengguna",
        title="Total Penyewaan Berdasarkan Jenis Pengguna",
        labels={
            "Jenis Pengguna": "Jenis Pengguna",
            "Total Penyewaan": "Total Penyewaan"
        },
        template="plotly_white"
    )

    st.plotly_chart(
        fig_user_total,
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("Pola Pengguna Berdasarkan Kelompok Waktu")

    segment_source = filtered_hour_df.copy()

    # Mengelompokkan jam menjadi lima periode waktu
    segment_source["Kelompok Waktu"] = pd.cut(
        segment_source["hr"],
        bins=[-1, 5, 9, 15, 19, 23],
        labels=TIME_ORDER
    )

    segment_source["Jenis Hari"] = (
        segment_source["workingday"]
        .map(WORKINGDAY_LABELS)
    )

    segment_summary = (
        segment_source
        .groupby(
            ["Jenis Hari", "Kelompok Waktu"],
            observed=True
        )[["casual", "registered"]]
        .mean()
        .reset_index()
    )

    segment_plot = segment_summary.melt(
        id_vars=["Jenis Hari", "Kelompok Waktu"],
        value_vars=["casual", "registered"],
        var_name="Jenis Pengguna",
        value_name="Rata-rata Penyewaan"
    )

    segment_plot["Jenis Pengguna"] = (
        segment_plot["Jenis Pengguna"]
        .map({
            "casual": "Kasual",
            "registered": "Terdaftar"
        })
    )

    fig_segment = px.bar(
        segment_plot,
        x="Kelompok Waktu",
        y="Rata-rata Penyewaan",
        color="Jenis Pengguna",
        barmode="group",
        facet_col="Jenis Hari",
        category_orders={
            "Kelompok Waktu": TIME_ORDER,
            "Jenis Hari": [
                "Hari non-kerja",
                "Hari kerja"
            ]
        },
        title="Rata-rata Penyewaan per Kelompok Waktu",
        labels={
            "Kelompok Waktu": "Kelompok Waktu",
            "Rata-rata Penyewaan": "Rata-rata Penyewaan per Jam",
            "Jenis Pengguna": "Jenis Pengguna"
        },
        template="plotly_white"
    )

    fig_segment.update_layout(
        legend_title_text="Jenis Pengguna"
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )

    st.markdown(
        """
        **Cara membaca grafik:** grafik membandingkan jumlah penyewaan
        pengguna kasual dan terdaftar berdasarkan kelompok waktu.
        Perbandingan ini dapat membantu memahami perbedaan pola penggunaan
        pada hari kerja dan non-kerja.
        """
    )


# ==================================================
# 14. INFORMASI SUMBER DATA
# ==================================================

st.markdown("---")

st.caption(
    "Bike Sharing Dashboard | Dataset periode 2011–2012. "
    "Angka dan grafik mengikuti filter yang dipilih pengguna."
)
