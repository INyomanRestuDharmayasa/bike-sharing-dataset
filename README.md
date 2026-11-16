# Proyek Analisis Data Penyewaan Sepeda (Bike Sharing Dataset)

Proyek ini merupakan analisis data pada **Bike Sharing Dataset** untuk memahami pola penyewaan sepeda berdasarkan kondisi cuaca, musim, tren pertumbuhan tahunan, serta waktu penggunaan, yang disajikan dalam bentuk notebook analisis dan dashboard interaktif menggunakan Streamlit.

## Struktur Direktori
```text
bike-sharing-analysis-main/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment - Virtual Environment (venv)
Pastikan terminal berada di direktori utama proyek (`bike-sharing-analysis-main/`), tempat berkas `requirements.txt` berada:

```bash
cd bike-sharing-analysis-main
python -m venv venv
```

Aktifkan virtual environment sesuai sistem operasi yang digunakan:
- **Windows:**
```bash
venv\Scripts\activate
```
- **Linux / macOS:**
```bash
source venv/bin/activate
```

Instal seluruh dependensi dari direktori utama `bike-sharing-analysis-main/`:
```bash
pip install -r requirements.txt
```

## Setup Environment - Anaconda (Alternatif)
Jika menggunakan Anaconda, jalankan perintah berikut dari direktori utama `bike-sharing-analysis-main/`:
```bash
conda create --name main-ds python=3.10
conda activate main-ds
pip install -r requirements.txt
```

## Menjalankan Notebook
1. Buka dan import berkas `notebook.ipynb` ke dalam Google Colab atau Jupyter Notebook.
2. Pastikan untuk menekan tombol **"Run All" / "Jalankan Semua"** agar seluruh sel analisis dan pembuatan dataset tereksekusi dengan benar.

## Menjalankan Dashboard Streamlit secara Lokal
Pastikan terminal berada di direktori utama `bike-sharing-analysis-main/` dan *environment* sudah aktif, lalu jalankan perintah berikut:
```bash
streamlit run dashboard/dashboard.py
```