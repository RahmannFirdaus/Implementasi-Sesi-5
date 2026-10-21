# 🌳 BRIN Environmental & Spatial Research Dashboard

> **Studi Kasus Lengkap Implementasi IMK & Visualisasi Data**  

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

### 2. Prinsip Gestalt - Enclosure & Proximity
> Kartu KPI dikelompokkan dengan border dan bayangan logis → menekan **Extrinsic Cognitive Load** mendekati nol.

### 3. Shneiderman's Visual Information Seeking Mantra
| Step | Implementasi |
|---|---|
| **Overview First** | 4 kartu KPI ringkasan di bagian atas halaman |
| **Zoom & Filter** | Sidebar interaktif: filter wilayah, tanggal, & status anomali |
| **Detail on Demand** | Expander tabel data mentah + tombol ekspor CSV |

### 4. Maximizing Data-Ink Ratio (Tufte)
> Template `plotly_dark` tanpa chartjunk - tidak ada efek 3D, grid tebal, atau dekorasi berlebihan.  
> Setiap piksel warna menyampaikan informasi data nyata.

### 5. Nielsen Heuristics & POUR
- ✅ **Visibility of System Status** - Loading indicator `st.cache_data`
- ✅ **Error Prevention** - Validasi input tanggal & warning jika filter kosong
- ✅ **Consistency & Standards** - Tata letak dan warna konsisten di seluruh halaman

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
5. **Treisman, A.** (1985). *Preattentive processing in vision.* Computer Vision, Graphics, and Image Processing, 31(2), 156-177.

