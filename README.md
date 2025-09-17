#  extractor-informasi-cerdas-v2
# 🔎 Extractor Informasi Cerdas

Aplikasi web serbaguna yang dibangun dengan Streamlit untuk menganalisis teks tidak terstruktur dan mengekstrak informasi penting secara otomatis. Aplikasi ini menggunakan teknik Natural Language Processing (NLP) untuk mengidentifikasi entitas kunci dan hubungannya, lalu menyajikannya dalam format tabel yang mudah dipahami.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://[NAMA-APP-STREAMLIT-ANDA].streamlit.app/)

## 🚀 Demo Aplikasi Langsung

Anda bisa mencoba aplikasi ini secara langsung di:
**[➡️ Live Demo Aplikasi](https://[NAMA-APP-STREAMLIT-ANDA].streamlit.app/)**

---

## 📸 Tampilan Aplikasi

![Screenshot Aplikasi](screenshot.png)

---

## ✨ Fitur Utama

* **Konfigurasi Entitas Dinamis:** Pengguna dapat mendefinisikan sendiri entitas dan kata kunci yang ingin dicari (misalnya Produk, Fitur, Masalah).
* **Analisis N-Gram:** Menampilkan frasa 2 kata (bigram) dan 3 kata (trigram) yang paling sering muncul untuk menemukan topik utama.
* **Named Entity Recognition (NER):** Menandai entitas yang telah dikonfigurasi secara visual di dalam teks.
* **Ekstraksi Informasi Terstruktur:** Mengubah hasil analisis menjadi tabel yang terstruktur, menunjukkan hubungan antar entitas.
* **Unduh Hasil:** Hasil ekstraksi dapat diunduh dalam format CSV untuk analisis lebih lanjut.

---

## 🛠️ Teknologi yang Digunakan

* **Framework Aplikasi:** Streamlit
* **Pemrosesan Bahasa (NLP):**
    * **spaCy:** Untuk pemrosesan teks dan NER berbasis aturan (`PhraseMatcher`).
    * **NLTK:** Untuk tokenisasi dan analisis N-Gram.
* **Manipulasi Data:** Pandas
* **Platform Deployment:** Streamlit Community Cloud

### Konsep Inti yang Diterapkan

1.  **N-Gram:** Urutan N kata yang berdekatan untuk mengidentifikasi frasa umum.
2.  **Named Entity Recognition (NER):** Proses menemukan dan mengklasifikasikan entitas bernama seperti produk, fitur, atau opini.
3.  **Information Extraction (IE):** Proses otomatis untuk mengambil informasi terstruktur (seperti hubungan antar entitas) dari teks mentah.

---

## 📓 Notebook Eksplorasi Google Colab

Proses awal analisis, pembersihan data, dan eksplorasi model dilakukan dalam notebook Google Colab. Anda bisa mengaksesnya melalui tautan di bawah ini untuk melihat detail prosesnya.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]([URL_COLAB_ANDA_YANG_SUDAH_DISALIN])

---

## 💻 Cara Menjalankan Secara Lokal

Jika Anda ingin menjalankan aplikasi ini di komputer Anda sendiri, ikuti langkah-langkah berikut:

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/](https://github.com/)[NAMA_USER_ANDA]/[NAMA_REPO_ANDA].git
    ```

2.  **Masuk ke direktori proyek:**
    ```bash
    cd [NAMA_REPO_ANDA]
    ```

3.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi Streamlit:**
    ```bash
    streamlit run app.py
    ```

Aplikasi akan terbuka secara otomatis di browser Anda.