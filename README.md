# 🛒 E-Commerce Customer Segmentation: RFM Analysis & Two-Tier K-Means Clustering

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![nbviewer](https://img.shields.io/badge/Render%20with-nbviewer-orange.svg?logo=jupyter&logoColor=white)](https://nbviewer.org/github/jaluprayoga/customer_segmentation/blob/main/notebook.ipynb)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-4c72b0.svg)](https://seaborn.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)

Proyek *Data Science & Customer Analytics* *end-to-end* untuk mengidentifikasi persona perilaku belanja pelanggan pada platform *e-commerce* ritel berbasis di Inggris (United Kingdom) menggunakan kombinasi **RFM Analysis (Recency, Frequency, Monetary)** dan arsitektur pemodelan **Two-Tier Customer Segmentation (Isolation Forest + K-Means Clustering)**.

> 🌐 **Pratinjau Notebook Online:** Jika GitHub mengalami limit render saat membuka notebook, Anda dapat melihat pratinjau lengkap notebook secara langsung melalui **[nbviewer (Klik di sini)](https://nbviewer.org/github/jaluprayoga/customer_segmentation/blob/main/notebook.ipynb)**.

---

## 📌 Daftar Isi
1. [Ringkasan Proyek & Latar Belakang](#-ringkasan-proyek--latar-belakang)
2. [Arsitektur Metodologi (Two-Tier Segmentation)](#-arsitektur-metodologi-two-tier-segmentation)
3. [Panduan Instalasi & Penggunaan Cepat](#-panduan-instalasi--penggunaan-cepat)
4. [Modul Kustom Visualisasi (`utils/`)](#-modul-kustom-visualisasi-utils)
5. [Temuan Utama & Profil Klaster Bisnis](#-temuan-utama--profil-klaster-bisnis)
   - [Model Global (Seluruh Pelanggan)](#1-model-global-seluruh-pelanggan-k--3--tier-1-outliers)
   - [Model Khusus Pasar Internasional (Non-UK)](#2-model-khusus-pasar-internasional-non-uk-k--4--tier-1-outliers)
6. [Rekomendasi Strategi Pemasaran & Ekspor](#-rekomendasi-strategi-pemasaran--ekspor)

---

## 📖 Ringkasan Proyek & Latar Belakang

*Dataset* mencatat seluruh riwayat transaksi pembelian selama periode satu tahun (01 Desember 2010 hingga 09 Desember 2011) yang mencakup **541.909 baris transaksi** dari **37 negara asal**.

### Tahapan Preprocessing Data:
- **Pembersihan Missing Values:** Transaksi tanpa `CustomerID` (135.080 baris / ~24,9%) dieliminasi karena segmentasi membutuhkan identitas unik pelanggan.
- **Pembersihan Data Anomali:** Transaksi pembatalan/retur (`Quantity <= 0`: 8.905 baris / 2,19%) dan kesalahan input harga (`UnitPrice <= 0`: 40 baris / 0,01%) difilter.
- **Data Siap Analisis:** Menghasilkan **397.884 baris transaksi bersih** dari **4.338 pelanggan unik** dan **18.532 faktur**.

---

## 🛡️ Arsitektur Metodologi (Two-Tier Segmentation)

Algoritma K-Means meminimalkan *Within-Cluster Sum of Squares* (WCSS) berbasis jarak Euclidean:
$$d(p, q) = \sqrt{(R_p - R_q)^2 + (F_p - F_q)^2 + (M_p - M_q)^2}$$

### Tantangan Analisis:
1. **Titik Ungkit (*High Leverage Points*):** Akun grosir (*wholesalers*) dan distributor komersial melakukan transaksi ratusan ribu pound sterling, menarik *centroid* K-Means secara ekstrem dan mendistorsi klaster ritel.
2. **Dilema Bisnis:** Outlier transaksi bernilai tinggi adalah pelanggan paling berharga (*highest-value whales*), sehingga **tidak boleh dihapus** dari bisnis.
3. **Disparitas Skala RFM:** Nilai *Monetary* (£) jauh lebih besar daripada *Recency* (hari) dan *Frequency* (pesanan).

### Solusi Dua Tingkat:
* **Tier 1 (Outliers — B2B Wholesalers & VIP Whales):** Akun anomali bervolume/nilai raksasa (5,00% populasi) diisolasi terlebih dahulu menggunakan algoritma *unsupervised* **Isolation Forest** (`contamination=0.05`) dan dikelola melalui strategi *Key Account Management*.
* **Tier 2 (Inliers — Core Retail Customers):** Sebanyak 95,00% pelanggan ritel reguler distandarisasi menggunakan `StandardScaler` ($\mu = 0, \sigma = 1$) agar seluruh sumbu RFM berbobot adil, lalu dimodelkan secara alami menggunakan **K-Means Clustering**.

---

## 🚀 Panduan Instalasi & Penggunaan Cepat

### 1. Kloning Repositori
```bash
git clone https://github.com/jaluprayoga/customer_segmentation.git
cd customer_segmentation
```

### 2. Buat & Aktifkan Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS (Bash):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 4. Unduh Dataset Otomatis
Untuk menjaga ukuran repositori Git tetap ringan, berkas dataset mentah (`Online Retail.xlsx` ~23.7 MB) tidak disimpan langsung di Git, melainkan diunduh melalui skrip otomatis:
```bash
python download_dataset.py
```
*Skrip ini mendukung multi-mirror CDN cepat dengan progress bar dan otomatis menempatkan data ke `dataset/Online Retail.xlsx`.*

### 5. Jalankan Notebook
Buka IDE pilihan Anda (VS Code, Cursor, atau Jupyter Lab):
```bash
jupyter lab
```
Pilih kernel `.venv` dan jalankan notebook [`notebook.ipynb`](./notebook.ipynb).

---

## 📊 Modul Kustom Visualisasi (`utils/`)

Repositori ini menyertakan modul modular [`utils/custom_chart.py`](./utils/custom_chart.py) untuk menyederhanakan kode visualisasi di notebook:

- **`plot_pie_chart(data, title, ...)`**: Membuat visualisasi proporsi kategori dengan persen otomatis, explode, dan palet warna selaras.
- **`plot_bar_chart(data, x, y, title, ...)`**: Membuat bar chart beranotasi nilai di atas batang secara otomatis (`fmt=',.0f'`) dan menghindari deprecation warning Seaborn.
- **`plot_line_chart(x, y, title, xlabel, ylabel, ...)`**: Membuat grafik tren berkala (mingguan, bulanan, per jam) dengan penanda titik dan anotasi nilai puncak.

---

## 💡 Temuan Utama & Profil Klaster Bisnis

### 1. Model Global Seluruh Pelanggan ($k = 3$ + Tier 1 Outliers)

Diterapkan pada **4.338 pelanggan** (217 akun Tier 1 + 4.121 pelanggan ritel Tier 2):

| Klaster / Segmen | Jumlah Pelanggan | Proporsi (% Pop.) | Rata-rata Recency | Rata-rata Frequency | Rata-rata Monetary | Persona Bisnis |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Tier 1 (Outliers)** | **217** | **5,00%** | 125,53 hari (Median: 19) | 481,85 order (Median: 250) | £18.100,50 (Median: £7.374,90) | **B2B Wholesalers & VIP Whales** |
| **Tier 2 - Cluster 0** | **2.548** | **58,74%** | 45,96 hari (Median: 36) | 52,96 order (Median: 41) | £884,45 (Median: £675,29) | **Active Core Regulars** |
| **Tier 2 - Cluster 1** | **995** | **22,94%** | 240,95 hari (Median: 238) | 23,38 order (Median: 17) | £394,97 (Median: £302,70) | **At-Risk / Churned Customers** |
| **Tier 2 - Cluster 2** | **578** | **13,32%** | 22,48 hari (Median: 15) | 233,75 order (Median: 215) | £4.043,30 (Median: £3.628,14) | **High-Value Loyal Champions** |

*(Proporsi Tier 2 terhadap inlier: Cluster 0 = 61,83%, Cluster 1 = 24,14%, Cluster 2 = 14,03%).*

---

### 2. Model Khusus Pasar Internasional (Non-UK, $k = 4$ + Tier 1 Outliers)

Diterapkan khusus pada **418 pelanggan internasional di luar Inggris**:

| Klaster / Segmen Non-UK | Jumlah Pelanggan | Proporsi (% Pop. Non-UK) | Rata-rata Recency | Rata-rata Frequency | Rata-rata Monetary | Persona Internasional |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Tier 1 (Outliers)** | **21** | **5,02%** | 116,71 hari (Median: 23) | 665,33 order (Median: 222) | £40.931,88 (Median: £13.689,67) | **Overseas B2B Wholesalers & Global Exporters** |
| **Tier 2 - Cluster 0** | **204** | **48,80%** | 55,63 hari (Median: 49,5) | 40,41 order (Median: 36) | £879,90 (Median: £750,52) | **Regular Mid-Tier Overseas Shoppers** |
| **Tier 2 - Cluster 1** | **29** | **6,94%** | 19,76 hari (Median: 15) | 291,48 order (Median: 294) | £8.252,63 (Median: £7.281,38) | **Super Champions / Top Overseas VIPs** |
| **Tier 2 - Cluster 2** | **81** | **19,38%** | 33,49 hari (Median: 21) | 135,32 order (Median: 128) | £3.406,40 (Median: £3.338,22) | **Loyal High-Potential Shoppers** |
| **Tier 2 - Cluster 3** | **83** | **19,86%** | 270,43 hari (Median: 277) | 23,29 order (Median: 18) | £586,79 (Median: £415,70) | **Dormant / Lost Overseas Accounts** |

---

## 🎯 Rekomendasi Strategi Pemasaran & Ekspor

1. **B2B & Mega Whales (Tier 1 Global & Non-UK):**
   - Penugasan *Dedicated Key Account Manager* personal.
   - Skema kontrak volume berjenjang (*Tiered Bulk Pricing*) dan fasilitas termin pembayaran fleksibel (*Net 30/60 days wire payment / Letter of Credit*).
   - Dukungan kepabeanan (*customs clearance*) dan pengiriman kontainer FOB/CIF.
2. **High-Value Champions & Overseas VIPs (Tier 2):**
   - Layanan pengiriman kilat internasional gratis (*Free International Express Shipping*).
   - Akses awal produk baru (*early access*) dan hadiah apresiasi fisik khas Inggris (*luxury British gift with purchase*).
3. **Active Regulars & High-Potential (Tier 2):**
   - Program loyalitas *tier-upgrade* untuk mendorong kenaikan kasta belanja.
   - Paket pengiriman pintar (*smart shipping bundles*) yang mengoptimalkan batas bobot flat ongkir.
4. **At-Risk & Dormant Customers (Tier 2):**
   - Kampanye *automated win-back* dengan voucher promosi terbatas saat musim diskon besar (Black Friday / Boxing Day).
   - Penghentian iklan berbayar (*ad spend suppression*) jika akun tidak aktif setelah 2 kali kampanye reaktivasi untuk efisiensi anggaran pemasaran.

---

## 🛠️ Stack Teknologi

- **Bahasa Pemrograman:** Python 3.10+
- **Manipulasi & Analisis Data:** Pandas, NumPy, OpenPyXL
- **Machine Learning & Statistik:** Scikit-Learn, Scipy, Yellowbrick
- **Visualisasi Data:** Matplotlib, Seaborn, Plotly Express
- **Lingkungan Pengembangan:** Jupyter Notebook, VS Code, Virtual Environment (`venv`)
