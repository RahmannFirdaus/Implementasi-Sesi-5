"""
generate_data.py
================
Script pembuat dataset simulasi riset BRIN.
Menghasilkan data sintetis untuk:
  - Deteksi pohon berbasis citra drone
  - Indeks permukiman kumuh berbasis data satelit
  - Penanda anomali kritis sebagai uji Pre-attentive Visual Coding

Referensi Domain: Riset Pemetaan Kawasan Kumuh & Deteksi Pohon
                  oleh Bapak Arafat Febrian Dirza (Chief HCI & Visualization, BRIN)
"""

import pandas as pd
import numpy as np


def generate_sample_data(output_path: str = "data_riset_brin.csv") -> pd.DataFrame:
    """
    Membuat dataset simulasi riset lingkungan spasial BRIN.

    Parameters
    ----------
    output_path : str
        Path file CSV keluaran.

    Returns
    -------
    pd.DataFrame
        DataFrame dataset yang dihasilkan.
    """
    np.random.seed(42)

    # Rentang tanggal observasi: 6 bulan (180 hari)
    dates = pd.date_range(start="2026-01-01", periods=180, freq="D")

    # Wilayah riset BRIN (mencerminkan lokasi riset narasumber)
    regions = [
        "Sumatera (Bengkulu)",
        "Jawa Barat (Bandung)",
        "Banten (Serpong)",
        "Kalimantan Timur",
    ]

    data = []
    for reg in regions:
        # Basis jumlah pohon berbeda antar wilayah (variasi karakteristik tutupan lahan)
        if "Bengkulu" in reg:
            base_trees = 1200
            base_slum = 45.0
        elif "Bandung" in reg:
            base_trees = 1500
            base_slum = 65.0
        elif "Serpong" in reg:
            base_trees = 900
            base_slum = 30.0
        else:
            # Kalimantan Timur
            base_trees = 2100
            base_slum = 20.0

        for i, d in enumerate(dates):
            # Simulasi data pohon dengan pola musiman dan noise acak
            tree_count = int(
                base_trees
                + np.sin(i / 10) * 50
                + np.random.randint(-20, 20)
            )

            # Simulasi indeks kumuh dengan pola cosinus dan noise Gaussian
            slum_index = round(
                float(
                    base_slum
                    + np.cos(i / 15) * 5
                    + np.random.normal(0, 1.5)
                ),
                2,
            )

            # -------------------------------------------------------
            # Anomaly Trigger — Implementasi Pre-attentive Attribute
            # Anomali dipicu secara periodik (setiap 30 hari) pada
            # wilayah Bengkulu untuk mensimulasikan kejadian lonjakan
            # indeks kumuh yang harus segera dikenali user (<200 ms).
            # -------------------------------------------------------
            is_anomaly = 1 if (i % 30 == 0 and "Bengkulu" in reg) else 0
            if is_anomaly:
                slum_index += 15.0  # Lonjakan signifikan sebagai sinyal kritis

            data.append(
                {
                    "tanggal": d.strftime("%Y-%m-%d"),
                    "wilayah": reg,
                    "jumlah_pohon_drone": tree_count,
                    "indeks_permukiman_kumuh": round(slum_index, 2),
                    "status_anomali": "Anomali Kritis" if is_anomaly else "Normal",
                }
            )

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"[OK] Dataset berhasil dibuat: {output_path}")
    print(f"     Total baris data : {len(df):,}")
    print(f"     Wilayah tercakup : {df['wilayah'].nunique()}")
    print(f"     Rentang tanggal  : {df['tanggal'].min()} -- {df['tanggal'].max()}")
    print(f"     Total anomali    : {(df['status_anomali'] == 'Anomali Kritis').sum()}")
    return df


if __name__ == "__main__":
    generate_sample_data()
