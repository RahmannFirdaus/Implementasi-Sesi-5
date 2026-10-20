"""
app.py
======
BRIN Environmental & Spatial Research Dashboard
================================================
Aplikasi dashboard interaktif Streamlit untuk pemantauan data lingkungan spasial BRIN.

Prinsip IMK & Visualisasi Data yang Diimplementasikan:
  1. Pre-attentive Attributes (<200 ms)  — Warna merah kontras untuk anomali kritis
  2. Prinsip Gestalt (Enclosure & Proximity) — Kartu KPI dengan border logis
  3. Shneiderman's Visual Information Seeking Mantra:
       • Overview First   → KPI summary di bagian atas
       • Zoom & Filter    → Sidebar filter wilayah & tanggal
       • Detail on Demand → Expander tabel data mentah & ekspor CSV
  4. Maximizing Data-Ink Ratio — Template plotly_white, tanpa chartjunk
  5. Nielsen Heuristics & POUR — Loading indicator, konsistensi, pencegahan error

Domain Riset: Pemetaan Kawasan Kumuh & Deteksi Pohon berbasis Citra Satelit/Drone
Narasumber  : Bapak Arafat Febrian Dirza (Chief of Research Group HCI & Visualization, BRIN)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# PAGE CONFIGURATION
# Heuristik Nielsen #4: Konsistensi & Standar — layout wide untuk density info
# =============================================================================
st.set_page_config(
    page_title="BRIN Environmental Research Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CUSTOM CSS
# Prinsip Gestalt Enclosure & Proximity:
#   - Kartu KPI dengan border dan bayangan halus
#   - Kontras tinggi untuk elemen anomali (Pre-attentive Color Coding)
#   - Tipografi bersih untuk meminimalkan Extrinsic Cognitive Load
# =============================================================================
st.markdown(
    """
    <style>
    /* ─── Google Font Import ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ─── Global Reset ───────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ─── Main Background (Dark Scientific Theme) ────────── */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        color: #e6edf3;
    }

    /* ─── Sidebar Styling ────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #1c2128 100%);
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #8b949e;
        font-size: 0.80rem;
    }

    /* ─── KPI Metric Cards (Gestalt Enclosure) ───────────── */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #1c2128, #21262d);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px 24px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        color: #e6edf3 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    /* Pre-attentive: delta merah untuk anomali */
    [data-testid="stMetricDeltaIcon-down"],
    [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }

    /* ─── Section Headers ────────────────────────────────── */
    h1 {
        color: #58a6ff !important;
        font-weight: 700 !important;
        font-size: 1.9rem !important;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #cdd9e5 !important;
        font-weight: 600 !important;
    }
    h4 {
        color: #8b949e !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px !important;
    }

    /* ─── Divider ────────────────────────────────────────── */
    hr {
        border-color: #30363d !important;
        margin: 12px 0 !important;
    }

    /* ─── Plotly Chart Container ─────────────────────────── */
    .stPlotlyChart {
        background: #1c2128 !important;
        border-radius: 12px;
        border: 1px solid #30363d;
        padding: 4px;
    }

    /* ─── Expander (Detail on Demand) ────────────────────── */
    [data-testid="stExpander"] {
        background: #1c2128 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    [data-testid="stExpander"] summary {
        color: #58a6ff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* ─── Download Button ────────────────────────────────── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #2ea043, #3fb950) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(46,160,67,0.4) !important;
    }

    /* ─── Anomali Badge (Pre-attentive Visual Warning) ───── */
    .anomali-badge {
        display: inline-block;
        background: rgba(229, 57, 53, 0.15);
        border: 1px solid #E53935;
        color: #ff6b6b;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        animation: pulse-badge 2s infinite;
    }
    @keyframes pulse-badge {
        0%, 100% { box-shadow: 0 0 0 0 rgba(229,57,53,0.4); }
        50%       { box-shadow: 0 0 0 6px rgba(229,57,53,0); }
    }

    /* ─── Info Banner ─────────────────────────────────────── */
    .info-banner {
        background: linear-gradient(135deg, rgba(88,166,255,0.08), rgba(56,139,253,0.05));
        border-left: 3px solid #58a6ff;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0 16px 0;
        font-size: 0.85rem;
        color: #8b949e;
        line-height: 1.6;
    }
    .info-banner strong { color: #cdd9e5; }

    /* ─── Dataframe ───────────────────────────────────────── */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
    }

    /* ─── Multiselect Pills ───────────────────────────────── */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #1f6feb !important;
        color: white !important;
        border-radius: 6px !important;
    }

    /* ─── Caption / Footer ────────────────────────────────── */
    .stCaption {
        color: #484f58 !important;
        font-size: 0.75rem !important;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# DATA LOADING WITH CACHING
# Heuristik Nielsen #1: Visibility of System Status
# st.cache_data meminimalkan waktu tunggu ulang (respons <5 detik untuk Budi)
# =============================================================================
@st.cache_data(show_spinner="⏳ Memuat dataset riset BRIN...")
def load_data(path: str = "data_riset_brin.csv") -> pd.DataFrame:
    """
    Memuat dan mem-parse dataset CSV riset BRIN.
    Di-cache oleh Streamlit agar tidak reload berulang.
    """
    df = pd.read_csv(path)
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "⚠️ **Dataset tidak ditemukan!**  \n"
        "Jalankan perintah berikut terlebih dahulu di terminal:  \n"
        "```bash\npython generate_data.py\n```"
    )
    st.stop()
except Exception as exc:
    st.error(f"❌ Terjadi kesalahan saat memuat data: `{exc}`")
    st.stop()

# =============================================================================
# SIDEBAR — ZOOM & FILTER
# Shneiderman's Mantra Step 2: Zoom & Filter
# UCD: Kemudahan akses kontrol → pengguna (Budi) dapat menyaring data
#       sebelum rapat tanpa membaca dokumentasi manual
# =============================================================================
with st.sidebar:
    st.markdown("## 🌳 Navigasi & Filter")
    st.markdown(
        '<div class="info-banner">'
        "<strong>UCD Principle:</strong> Panel ini mengimplementasikan "
        "<em>Zoom & Filter</em> dari Shneiderman's Mantra — "
        "memungkinkan pengguna menyempurnakan tampilan data sesuai konteks kebutuhan."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Filter Wilayah ────────────────────────────────────────────────────────
    all_regions = sorted(df["wilayah"].unique().tolist())
    wilayah_selected = st.multiselect(
        "📍 Wilayah Riset:",
        options=all_regions,
        default=all_regions,
        help="Pilih satu atau lebih wilayah pemantauan BRIN.",
    )

    st.markdown("---")

    # ── Filter Rentang Tanggal ─────────────────────────────────────────────────
    date_min = df["tanggal"].min().date()
    date_max = df["tanggal"].max().date()

    date_range = st.date_input(
        "📅 Rentang Tanggal Pengamatan:",
        value=[date_min, date_max],
        min_value=date_min,
        max_value=date_max,
        help="Saring data berdasarkan rentang tanggal observasi.",
    )

    # Validasi input tanggal (pencegahan error — Nielsen Heuristic #5)
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

    st.markdown("---")

    # ── Filter Status Anomali ─────────────────────────────────────────────────
    status_options = df["status_anomali"].unique().tolist()
    status_selected = st.multiselect(
        "🚨 Status Data:",
        options=status_options,
        default=status_options,
        help="Filter berdasarkan status anomali data.",
    )

    st.markdown("---")
    st.markdown(
        '<div class="info-banner">'
        "📊 <strong>Data Range:</strong><br/>"
        f"&nbsp;&nbsp;Dari: <code>{date_min}</code><br/>"
        f"&nbsp;&nbsp;Hingga: <code>{date_max}</code><br/>"
        f"&nbsp;&nbsp;Total Wilayah: <code>{len(all_regions)}</code>"
        "</div>",
        unsafe_allow_html=True,
    )

# =============================================================================
# FILTERING DATAFRAME
# =============================================================================
if not wilayah_selected:
    st.warning("⚠️ Pilih minimal satu wilayah untuk menampilkan data.")
    st.stop()

filtered_df = df[
    (df["wilayah"].isin(wilayah_selected))
    & (df["tanggal"].dt.date >= start_date)
    & (df["tanggal"].dt.date <= end_date)
    & (df["status_anomali"].isin(status_selected))
].copy()

if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih. Silakan sesuaikan filter.")
    st.stop()

# =============================================================================
# HEADER — OVERVIEW FIRST
# Shneiderman's Mantra Step 1: Overview First
# Judul besar + konteks naratif → orientasi instan untuk Budi sebelum rapat
# =============================================================================
st.markdown("# 🌳 BRIN Environmental & Spatial Research Dashboard")

total_anomalies = (filtered_df["status_anomali"] == "Anomali Kritis").sum()

col_title, col_badge = st.columns([4, 1])
with col_title:
    st.markdown(
        '<div class="info-banner">'
        "<strong>Studi Kasus IMK & Visualisasi Data</strong> — "
        "Berdasarkan materi riset <em>Bapak Arafat Febrian Dirza</em> "
        "(Chief of Research Group for HCI & Visualization, BRIN).<br/>"
        "Prinsip: <strong>Maximizing Data-Ink Ratio</strong> · "
        "<strong>Pre-attentive Color Coding</strong> · "
        "<strong>Zero Extrinsic Cognitive Load</strong> · "
        "<strong>Shneiderman's Visual Information Seeking Mantra</strong>."
        "</div>",
        unsafe_allow_html=True,
    )
with col_badge:
    if total_anomalies > 0:
        st.markdown(
            f'<div style="padding-top:14px; text-align:center;">'
            f'<span class="anomali-badge">🔴 {total_anomalies} Anomali Terdeteksi</span>'
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="padding-top:14px; text-align:center;">'
            '<span style="color:#3fb950; font-weight:600; font-size:0.85rem;">'
            "✅ Semua Data Normal"
            "</span></div>",
            unsafe_allow_html=True,
        )

st.divider()

# =============================================================================
# KPI METRICS — GESTALT PROXIMITY & PRE-ATTENTIVE ATTRIBUTES
# Empat kartu KPI memberikan gambaran data sekilas (<5 detik)
# sesuai kebutuhan user persona Budi (Executive Decision Maker)
# =============================================================================
st.markdown("#### 📊 Ringkasan KPI — Overview First (Shneiderman's Mantra Step 1)")

col1, col2, col3, col4 = st.columns(4)

total_trees = filtered_df["jumlah_pohon_drone"].sum()
avg_slum = filtered_df["indeks_permukiman_kumuh"].mean()
max_slum = filtered_df["indeks_permukiman_kumuh"].max()
total_records = len(filtered_df)

with col1:
    st.metric(
        label="🌲 Total Pohon Terdeteksi (Drone)",
        value=f"{total_trees:,}",
        help="Total kumulatif pohon terdeteksi dari citra drone pada periode & wilayah terpilih.",
    )

with col2:
    st.metric(
        label="🏘️ Rata-rata Indeks Kumuh",
        value=f"{avg_slum:.2f}",
        help="Rata-rata indeks permukiman kumuh berdasarkan data satelit.",
    )

with col3:
    st.metric(
        label="🚨 Jumlah Anomali Kritis",
        value=f"{total_anomalies}",
        delta="Perhatian Kritis" if total_anomalies > 0 else "Semua Normal",
        delta_color="inverse" if total_anomalies > 0 else "normal",
        help="Jumlah titik data yang teridentifikasi sebagai anomali lonjakan indeks kumuh.",
    )

with col4:
    st.metric(
        label="📍 Wilayah Dipantau",
        value=f"{len(wilayah_selected)} / {len(all_regions)}",
        help="Rasio wilayah yang sedang ditampilkan terhadap total wilayah tersedia.",
    )

st.divider()

# =============================================================================
# CHARTS — HIGH DATA-INK RATIO, ZERO CHARTJUNK
# Prinsip Tufte: Template plotly_white, tanpa efek 3D, tanpa dekorasi berlebihan
# Setiap piksel warna menyampaikan informasi data nyata
# =============================================================================
st.markdown("#### 📈 Visualisasi Tren & Distribusi Spasial")

# ── Row 1: Line Chart & Scatter Anomali ──────────────────────────────────────
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown(
        "#### Tren Deteksi Pohon Seiring Waktu",
        help="Line chart menampilkan fluktuasi jumlah pohon terdeteksi per wilayah. "
             "Maximizing Data-Ink Ratio: tidak ada chartjunk, grid halus.",
    )

    # Agregasi harian per wilayah agar chart tidak overplotted
    tree_daily = (
        filtered_df.groupby(["tanggal", "wilayah"])["jumlah_pohon_drone"]
        .mean()
        .reset_index()
    )

    fig_tree = px.line(
        tree_daily,
        x="tanggal",
        y="jumlah_pohon_drone",
        color="wilayah",
        labels={
            "tanggal": "Tanggal",
            "jumlah_pohon_drone": "Jumlah Pohon",
            "wilayah": "Wilayah",
        },
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_tree.update_traces(
        mode="lines",
        line=dict(width=2),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Pohon: <b>%{y:,}</b><extra></extra>",
    )
    fig_tree.update_layout(
        plot_bgcolor="rgba(28,33,40,0)",
        paper_bgcolor="rgba(28,33,40,0)",
        font_color="#8b949e",
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            orientation="h",
            y=-0.25,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
        yaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
        hoverlabel=dict(bgcolor="#1c2128", font_size=12),
    )
    st.plotly_chart(fig_tree, use_container_width=True)

with chart_col2:
    st.markdown(
        "#### Deteksi Anomali Indeks Permukiman Kumuh",
        help="Scatter chart dengan pre-attentive color coding: "
             "merah (#E53935) untuk Anomali Kritis, biru (#1E88E5) untuk Normal. "
             "Otak mengenali perbedaan warna dalam <200 ms.",
    )

    fig_slum = px.scatter(
        filtered_df,
        x="tanggal",
        y="indeks_permukiman_kumuh",
        color="status_anomali",
        # ─────────────────────────────────────────────────────────────────────
        # Pre-attentive Attribute: Warna merah tinggi kontras (#E53935) untuk
        # Anomali Kritis memungkinkan deteksi visual instan (<200 ms) tanpa
        # membaca label — sesuai prinsip yang dipaparkan narasumber.
        # ─────────────────────────────────────────────────────────────────────
        color_discrete_map={
            "Normal": "#1E88E5",
            "Anomali Kritis": "#E53935",
        },
        size="indeks_permukiman_kumuh",
        size_max=16,
        hover_data={"wilayah": True, "tanggal": "|%d %b %Y"},
        labels={
            "indeks_permukiman_kumuh": "Indeks Kumuh",
            "status_anomali": "Status",
            "tanggal": "Tanggal",
        },
        template="plotly_dark",
    )
    fig_slum.update_layout(
        plot_bgcolor="rgba(28,33,40,0)",
        paper_bgcolor="rgba(28,33,40,0)",
        font_color="#8b949e",
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            orientation="h",
            y=-0.25,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
        yaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
        hoverlabel=dict(bgcolor="#1c2128", font_size=12),
    )
    st.plotly_chart(fig_slum, use_container_width=True)

st.markdown("---")

# ── Row 2: Bar Chart Perbandingan Wilayah & Box Plot Distribusi ───────────────
bar_col, box_col = st.columns(2)

with bar_col:
    st.markdown(
        "#### Perbandingan Rata-rata Pohon per Wilayah",
        help="Bar chart horizontal untuk perbandingan antar wilayah — "
             "Gestalt Proximity: kategori dikodekan secara visual oleh warna.",
    )
    region_summary = (
        filtered_df.groupby("wilayah")["jumlah_pohon_drone"]
        .mean()
        .reset_index()
        .rename(columns={"jumlah_pohon_drone": "rata_pohon"})
        .sort_values("rata_pohon", ascending=True)
    )

    fig_bar = px.bar(
        region_summary,
        x="rata_pohon",
        y="wilayah",
        orientation="h",
        labels={"rata_pohon": "Rata-rata Pohon Terdeteksi", "wilayah": ""},
        template="plotly_dark",
        color="rata_pohon",
        color_continuous_scale="Teal",
    )
    fig_bar.update_layout(
        plot_bgcolor="rgba(28,33,40,0)",
        paper_bgcolor="rgba(28,33,40,0)",
        font_color="#8b949e",
        margin=dict(l=10, r=10, t=20, b=10),
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
        yaxis=dict(linecolor="#30363d"),
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{y}</b><br>Rata-rata Pohon: <b>%{x:,.0f}</b><extra></extra>"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with box_col:
    st.markdown(
        "#### Distribusi Indeks Kumuh per Wilayah (Box Plot)",
        help="Box plot menampilkan sebaran, median, dan outlier indeks kumuh "
             "— mendukung analisis statistik deskriptif cepat.",
    )
    fig_box = px.box(
        filtered_df,
        x="wilayah",
        y="indeks_permukiman_kumuh",
        color="wilayah",
        labels={
            "indeks_permukiman_kumuh": "Indeks Permukiman Kumuh",
            "wilayah": "Wilayah",
        },
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_box.update_layout(
        plot_bgcolor="rgba(28,33,40,0)",
        paper_bgcolor="rgba(28,33,40,0)",
        font_color="#8b949e",
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        xaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickangle=-20),
        yaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# =============================================================================
# DETAIL ON DEMAND — Shneiderman's Mantra Step 3
# Data mentah hanya ditampilkan saat pengguna secara eksplisit memintanya
# (klik expander), menghindari information overload pada tampilan utama.
# =============================================================================
with st.expander(
    "🔍 Detail on Demand: Rincian Data Mentah & Ekspor (Klik untuk Membuka)",
    expanded=False,
):
    st.markdown(
        '<div class="info-banner">'
        "<strong>Detail on Demand</strong> — Shneiderman's Mantra Step 3.<br/>"
        "Data mentah ditampilkan sesuai permintaan eksplisit pengguna, "
        "mencegah <em>information overload</em> pada tampilan ringkasan."
        "</div>",
        unsafe_allow_html=True,
    )

    # Highlight baris anomali
    def highlight_anomali(row):
        if row["status_anomali"] == "Anomali Kritis":
            return ["background-color: rgba(229,57,53,0.15); color: #ff6b6b;"] * len(row)
        return [""] * len(row)

    display_df = filtered_df.copy()
    display_df["tanggal"] = display_df["tanggal"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df.style.apply(highlight_anomali, axis=1),
        use_container_width=True,
        height=320,
    )

    st.markdown(f"**Total baris ditampilkan:** `{len(display_df):,}` dari `{len(df):,}` data keseluruhan.")

    col_dl1, col_dl2 = st.columns([1, 3])
    with col_dl1:
        csv_data = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Ekspor Data Terfilter (CSV)",
            data=csv_data,
            file_name="brin_spatial_filtered_data.csv",
            mime="text/csv",
            use_container_width=True,
        )

# =============================================================================
# FOOTER
# =============================================================================
st.divider()
st.caption(
    "🌳 **BRIN Environmental & Spatial Research Dashboard** · "
    "Implementasi Studi Kasus Praktikum IMK & Visualisasi Data · "
    "Narasumber: Bapak Arafat Febrian Dirza (Chief HCI & Visualization, BRIN) · "
    f"Data per {df['tanggal'].max().strftime('%d %B %Y')}"
)
