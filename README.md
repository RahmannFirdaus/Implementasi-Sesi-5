# 🌳 BRIN Environmental & Spatial Research Dashboard

> **Studi Kasus Lengkap Implementasi IMK & Visualisasi Data**  
> Berdasarkan materi pemaparan **Bapak Arafat Febrian Dirza**  
> *(Chief of Research Group for HCI and Visualization, BRIN)*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?logo=streamlit)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-blue?logo=plotly)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📑 Latar Belakang

Dashboard ini dikembangkan sebagai **studi kasus praktikum** mata kuliah **Interaksi Manusia Komputer (IMK) & Visualisasi Data**, mengimplementasikan seluruh prinsip yang dipaparkan oleh narasumber dalam domain riset nyata BRIN:

- **Pemetaan kawasan permukiman kumuh** berbasis data satelit
- **Deteksi & perhitungan pohon** menggunakan citra drone

### 👤 User Persona Target: **Budi** *(30 tahun)*
| Atribut | Detail |
|---|---|
| **Peran** | Data Analyst / Executive Decision Maker di BRIN |
| **Kebutuhan Utama** | Memantau KPI lingkungan dalam <5 detik sebelum rapat |
| **Pain Point** | Filter wilayah yang rumit & rincian anomali yang tersembunyi |
| **Goal** | Mengambil keputusan berbasis data dengan cepat dan akurat |

---

## 🧠 Prinsip IMK & Visualisasi yang Diimplementasikan

### 1. Pre-attentive Attributes (<200 ms)
> Warna merah kontras `#E53935` digunakan khusus untuk menandai **Anomali Kritis**.  
> Otak manusia memproses perbedaan warna sebelum pemrosesan kognitif teks aktif.

### 2. Prinsip Gestalt — Enclosure & Proximity
> Kartu KPI dikelompokkan dengan border dan bayangan logis → menekan **Extrinsic Cognitive Load** mendekati nol.

### 3. Shneiderman's Visual Information Seeking Mantra
| Step | Implementasi |
|---|---|
| **Overview First** | 4 kartu KPI ringkasan di bagian atas halaman |
| **Zoom & Filter** | Sidebar interaktif: filter wilayah, tanggal, & status anomali |
| **Detail on Demand** | Expander tabel data mentah + tombol ekspor CSV |

### 4. Maximizing Data-Ink Ratio (Tufte)
> Template `plotly_dark` tanpa chartjunk — tidak ada efek 3D, grid tebal, atau dekorasi berlebihan.  
> Setiap piksel warna menyampaikan informasi data nyata.

### 5. Nielsen Heuristics & POUR
- ✅ **Visibility of System Status** — Loading indicator `st.cache_data`
- ✅ **Error Prevention** — Validasi input tanggal & warning jika filter kosong
- ✅ **Consistency & Standards** — Tata letak dan warna konsisten di seluruh halaman

---

## 🗂️ Struktur Repositori

```
brin-spatial-dashboard/
├── app.py                # Aplikasi utama dashboard interaktif Streamlit
├── generate_data.py      # Script pembuat dataset simulasi riset BRIN
├── data_riset_brin.csv   # Dataset sampel hasil simulasi (auto-generated)
├── requirements.txt      # Daftar pustaka & dependensi Python
└── README.md             # Dokumentasi proyek & panduan penggunaan
```

---

## 🚀 Panduan Instalasi & Menjalankan Aplikasi

### Prasyarat
- Python 3.9 atau lebih baru
- pip (Python package manager)
- Git

### Langkah 1: Clone Repositori

```bash
git clone https://github.com/<username>/brin-spatial-dashboard.git
cd brin-spatial-dashboard
```

### Langkah 2: Buat Virtual Environment (Direkomendasikan)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Langkah 3: Install Dependensi

```bash
pip install -r requirements.txt
```

### Langkah 4: Generate Dataset Simulasi

```bash
python generate_data.py
```

Output yang diharapkan:
```
✅ Dataset berhasil dibuat: data_riset_brin.csv
   Total baris data : 720
   Wilayah tercakup : 4
   Rentang tanggal  : 2026-01-01 — 2026-06-29
   Total anomali    : 6
```

### Langkah 5: Jalankan Dashboard

```bash
streamlit run app.py
```

Buka browser di: **http://localhost:8501**

---

## 📊 Fitur Utama Dashboard

| Fitur | Deskripsi | Prinsip IMK |
|---|---|---|
| **KPI Cards** | Ringkasan total pohon, rata-rata indeks kumuh, jumlah anomali | Overview First, Gestalt Proximity |
| **Line Chart** | Tren deteksi pohon per wilayah seiring waktu | Data-Ink Ratio |
| **Scatter Anomali** | Deteksi visual anomali dengan warna merah kontras | Pre-attentive Attributes |
| **Bar Chart** | Perbandingan rata-rata pohon antar wilayah | Gestalt Proximity |
| **Box Plot** | Distribusi indeks kumuh per wilayah | Statistical Overview |
| **Sidebar Filter** | Filter wilayah, tanggal, dan status interaktif | Zoom & Filter |
| **Data Table + Export** | Rincian data mentah + ekspor CSV | Detail on Demand |
| **Anomali Badge** | Animasi pulsing merah jika ada anomali kritis | Pre-attentive (Animation) |

---

## 📤 Panduan Upload ke GitHub

### Persiapan Awal (Sekali Saja)

```bash
# Konfigurasi identitas Git
git config --global user.name "Nama Anda"
git config --global user.email "email@anda.com"
```

### Langkah Upload

```bash
# 1. Inisialisasi repositori Git lokal
git init

# 2. Tambahkan semua file ke staging
git add .

# 3. Commit pertama
git commit -m "feat: Initial commit — BRIN Environmental Dashboard

Implementasi lengkap studi kasus IMK & Visualisasi Data:
- Pre-attentive Color Coding untuk anomali kritis
- Shneiderman's Visual Information Seeking Mantra
- Gestalt Enclosure & Proximity pada KPI cards
- Maximizing Data-Ink Ratio (Plotly dark theme)
- Nielsen Heuristics: error prevention & status visibility"

# 4. Hubungkan ke remote repository GitHub
git remote add origin https://github.com/<username>/brin-spatial-dashboard.git

# 5. Push ke GitHub
git branch -M main
git push -u origin main
```

### File `.gitignore` yang Direkomendasikan

```
# Virtual environment
venv/
env/
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo

# Streamlit cache
.streamlit/

# Dataset (opsional — generate ulang dengan script)
# data_riset_brin.csv

# IDE files
.vscode/
.idea/
*.swp
```

---

## 📦 Dependensi

| Library | Versi Minimum | Kegunaan |
|---|---|---|
| `streamlit` | 1.30.0 | Framework dashboard web interaktif |
| `pandas` | 2.0.0 | Manipulasi & analisis data tabular |
| `plotly` | 5.18.0 | Visualisasi data interaktif |
| `numpy` | 1.24.0 | Komputasi numerik & simulasi data |

---

## 📚 Referensi Akademik

1. **Shneiderman, B.** (1996). *The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations.* IEEE Symposium on Visual Languages.
2. **Tufte, E.R.** (2001). *The Visual Display of Quantitative Information.* Graphics Press.
3. **Nielsen, J.** (1994). *Usability Engineering.* Morgan Kaufmann.
4. **Ware, C.** (2012). *Information Visualization: Perception for Design.* Morgan Kaufmann.
5. **Treisman, A.** (1985). *Preattentive processing in vision.* Computer Vision, Graphics, and Image Processing, 31(2), 156–177.

---

## 👨‍💻 Informasi Pengembang

**Dikembangkan untuk:**  
Praktikum Mata Kuliah IMK & Visualisasi Data  
Berdasarkan materi narasumber: **Bapak Arafat Febrian Dirza**  
*(Chief of Research Group for HCI and Visualization, BRIN)*

---

*Dashboard ini merupakan implementasi akademik untuk tujuan pembelajaran.*  
*Data yang digunakan adalah simulasi sintetis — bukan data riset aktual BRIN.*
