# 🚲 Bike Sharing Data Analysis

## Project Overview

Proyek ini bertujuan untuk menganalisis pola penyewaan sepeda menggunakan **Bike Sharing Dataset**. Analisis dilakukan untuk memahami bagaimana waktu penyewaan dan kondisi cuaca berkaitan dengan jumlah penyewaan sepeda, serta melihat perbedaan perilaku antara pengguna kasual dan pengguna terdaftar.

Proyek ini mencakup proses analisis data menggunakan Python, mulai dari pengumpulan data, pemeriksaan kualitas data, pembersihan data, eksplorasi data, visualisasi, hingga penyusunan kesimpulan dan rekomendasi. Hasil analisis juga disajikan melalui dashboard interaktif menggunakan Streamlit.

## Business Questions

Analisis ini berfokus pada dua pertanyaan bisnis utama:

1. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda per jam antara hari kerja dan hari non-kerja selama Januari 2011 hingga Desember 2012, dan kapan permintaan mencapai puncaknya pada masing-masing kelompok?

2. Bagaimana rata-rata jumlah penyewaan sepeda harian berbeda berdasarkan kategori kondisi cuaca selama Januari 2011 hingga Desember 2012, dan berapa persentase perbedaannya dibandingkan dengan kondisi cuaca cerah?

Selain itu, dilakukan analisis lanjutan untuk melihat perbedaan pola penyewaan antara pengguna kasual (*casual*) dan pengguna terdaftar (*registered*) berdasarkan kelompok waktu dan jenis hari.

## Dataset

Dataset yang digunakan adalah Bike Sharing Dataset dari Capital Bikeshare, dengan periode pengamatan tahun 2011–2012.

Dataset terdiri dari dua file utama:

- **`day.csv`**: Data penyewaan sepeda harian, termasuk jumlah penyewaan, kondisi cuaca, dan informasi pengguna.
- **`hour.csv`**: Data penyewaan sepeda per jam, termasuk waktu penyewaan, jenis hari, kondisi cuaca, serta jumlah penyewaan dari pengguna kasual dan terdaftar.

Sumber dataset:
- [Bike Sharing Dataset — Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)

## Tools and Libraries

Proyek ini menggunakan beberapa tools dan library berikut:

- **Python** untuk pemrograman dan analisis data.
- **Pandas** untuk membaca, membersihkan, dan mengolah data.
- **NumPy** untuk operasi numerik.
- **Matplotlib dan Seaborn** untuk visualisasi dalam notebook.
- **Plotly** untuk membuat grafik interaktif pada dashboard.
- **Streamlit** untuk membangun dashboard berbasis web.
- **Jupyter Notebook / Google Colab** untuk mendokumentasikan proses analisis data.
- **Git dan GitHub** untuk version control dan penyimpanan kode proyek.

## Project Structure

```text
submission/
├── dashboard/
│   └── dashboard.py
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

Keterangan:

- `dashboard/dashboard.py`: Kode untuk menjalankan dashboard Streamlit.
- `data/day.csv` dan `data/hour.csv`: Dataset asli.
- `notebook.ipynb`: Dokumentasi proses analisis data.
- `requirements.txt`: Daftar library Python yang diperlukan.
- `url.txt`: Tempat menyimpan URL dashboard setelah berhasil di-deploy.

## Data Analysis Process

Proyek ini dilakukan melalui beberapa tahapan berikut.

### 1. Data Gathering

Memuat dataset harian dan per jam ke dalam DataFrame menggunakan Pandas.

### 2. Data Assessing

Memeriksa kualitas data, termasuk missing values, data duplikat, tipe data, konsistensi jumlah penyewaan, dan calon outlier.

### 3. Data Cleaning

Memperbaiki tipe data tanggal dan memeriksa hasil assessment. Data yang masih valid dipertahankan agar informasi penting tidak hilang.

### 4. Exploratory Data Analysis (EDA)

Melakukan eksplorasi untuk memahami pola penyewaan berdasarkan waktu, kondisi cuaca, serta jenis pengguna.

### 5. Visualization and Explanatory Analysis

Menyajikan hasil analisis menggunakan grafik, seperti line chart, heatmap, bar chart, dan boxplot.

### 6. Advanced Analysis

Menggunakan teknik *binning* untuk mengelompokkan jam ke dalam beberapa periode waktu, kemudian membandingkan pola penyewaan pengguna kasual dan terdaftar.

### 7. Conclusion and Recommendation

Menyusun kesimpulan dari hasil analisis dan memberikan rekomendasi terkait perencanaan ketersediaan sepeda berdasarkan waktu dan kondisi cuaca.

## Dashboard Features

Dashboard Streamlit menyediakan beberapa bagian utama:

- **Ringkasan:** Menampilkan total penyewaan, jumlah penyewaan pengguna kasual dan terdaftar, serta rata-rata penyewaan harian.
- **Pola Waktu:** Menampilkan pola penyewaan per jam dan heatmap berdasarkan hari dan jam.
- **Kondisi Cuaca:** Membandingkan rata-rata dan distribusi jumlah penyewaan pada setiap kategori cuaca.
- **Jenis Pengguna:** Membandingkan perilaku pengguna kasual dan terdaftar berdasarkan kelompok waktu.
- **Interactive Filters:** Memungkinkan pengguna memilih rentang tanggal, jenis hari, dan kondisi cuaca.

## How to Run Locally

### Prerequisites

Pastikan Python dan Git telah terinstal di komputer.

### 1. Clone Repository

```bash
git clone https://github.com/adyudaghiffari/bike-sharing-analysis.git
cd bike-sharing-analysis
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Jika menggunakan Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Prepare the Dataset

Pastikan folder `data/` berisi `day.csv` dan `hour.csv`.

Apabila ingin menggunakan hasil pembersihan data dari notebook, jalankan proses cleaning dan ekspor data ke `day_clean.csv` serta `hour_clean.csv`, kemudian simpan kedua file tersebut di folder `data/`.

Dashboard akan menggunakan data hasil cleaning apabila kedua file tersebut tersedia. Jika tidak, dashboard akan menggunakan dataset asli.

### 5. Run the Dashboard

Jalankan perintah berikut dari folder utama proyek:

```bash
python -m streamlit run dashboard/dashboard.py
```

Dashboard dapat diakses melalui alamat lokal yang ditampilkan di terminal, biasanya:

`http://localhost:8501`

Untuk menghentikan aplikasi, tekan `Ctrl + C` pada terminal.

## Deployment

Dashboard dapat di-deploy menggunakan Streamlit Community Cloud melalui repository GitHub.

Langkah umum deployment:

1. Push seluruh file proyek yang dibutuhkan ke GitHub.
2. Buka [Streamlit Community Cloud](https://share.streamlit.io/).
3. Hubungkan akun GitHub dan pilih repository proyek.
4. Pilih branch `main`.
5. Gunakan `dashboard/dashboard.py` sebagai main file path.
6. Klik Deploy dan tunggu hingga aplikasi berhasil dijalankan.

Setelah deployment berhasil, masukkan URL publik dashboard ke dalam `url.txt`.

## Author

**Adyuda Ghiffari**

GitHub: [adyudaghiffari](https://github.com/adyudaghiffari)

---

*Project ini dibuat sebagai bagian dari submission kelas analisis data Dicoding.*