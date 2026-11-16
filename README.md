# Proyek Analisis Data: Bike Sharing Dataset

Analisis data penyewaan sepeda (*Bike Sharing* Capital Bikeshare), mencakup proses *data wrangling*, *EDA*, visualisasi, analisis lanjutan (*Clustering* / *Manual Grouping* kategori waktu), serta *dashboard* Streamlit interaktif.

## Pertanyaan Bisnis

- **Pertanyaan 1**: Bagaimana perbandingan rata-rata jumlah penyewaan sepeda harian berdasarkan kondisi cuaca dan musim sepanjang tahun 2011 hingga 2012?
- **Pertanyaan 2**: Bagaimana perbedaan pola rata-rata penyewaan sepeda harian antara pengguna casual dan registered pada hari kerja dibandingkan hari libur/akhir pekan selama periode 2011–2012?
- **Pertanyaan 3**: Pada kelompok kategori waktu manakah terjadi puncak rata-rata penyewaan sepeda per jam, serta bagaimana perbandingan proporsi pengguna casual dan registered di setiap kategori waktu tersebut selama tahun 2011–2012?

## Struktur Direktori

submission
├── dashboard
│   ├── main_data.csv
│   └── dashboard.py
├── data
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt

## Setup Environment

```bash
python -m venv venv
source venv/bin/activate      
pip install -r requirements.txt