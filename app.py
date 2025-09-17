import streamlit as st
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter
import re

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="Extractor Cerdas ✨",
    page_icon="🔎",
    layout="wide"
)

# --- Fungsi yang di-cache untuk mempercepat loading ---

# Mengunduh resource NLTK (hanya sekali)
@st.cache_resource
def download_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    return True

# Memuat model spaCy (resource berat, jadi di-cache)
@st.cache_resource
def load_spacy_model(model="en_core_web_sm"):
    return spacy.load(model)

# Mengonversi DataFrame ke CSV untuk diunduh
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# --- Memuat Model dan Resource ---
download_nltk_resources()
nlp = load_spacy_model()

# =====================================================================================
# --- INTERFACE APLIKASI (UI) ---
# =====================================================================================

st.title("🔎 Extractor Informasi Cerdas")
st.markdown("Analisis teks mentah untuk menemukan entitas kunci dan hubungannya. Konfigurasikan entitas Anda di sidebar!")

# --- SIDEBAR UNTUK KONFIGURASI ---
st.sidebar.header("⚙️ Konfigurasi Entitas")
st.sidebar.markdown("""
Definisikan kategori dan kata kunci yang ingin Anda ekstrak. 
Aplikasi ini akan mencari kata-kata ini dalam teks Anda.
""")

# Contoh default untuk memudahkan pengguna
contoh_utama = "Ponsel Cerdas X Pro\nLaptop Gaming Z1"
contoh_atribut = "kamera\nbaterai\nlayar\nkeyboard\nkipas\nperforma"
contoh_deskriptor = "buruk\ntidak responsif\npanas\npayah\nmengecewakan\noverheat\nberisik\nkurang cerah\nbagus\ncepat\nluar biasa"

entitas_utama_label = st.sidebar.text_input("Label Entitas Utama (e.g., PRODUK)", "PRODUK")
entitas_utama_keywords = st.sidebar.text_area("Kata Kunci Entitas Utama (satu per baris)", contoh_utama, height=100)

entitas_atribut_label = st.sidebar.text_input("Label Entitas Atribut (e.g., FITUR)", "FITUR")
entitas_atribut_keywords = st.sidebar.text_area("Kata Kunci Entitas Atribut (satu per baris)", contoh_atribut, height=150)

entitas_deskriptor_label = st.sidebar.text_input("Label Entitas Deskriptor (e.g., MASALAH/OPINI)", "OPINI")
entitas_deskriptor_keywords = st.sidebar.text_area("Kata Kunci Entitas Deskriptor (satu per baris)", contoh_deskriptor, height=150)

st.sidebar.info("Aplikasi ini menggunakan **spaCy** untuk NER berbasis aturan dan **NLTK** untuk analisis N-Gram.")

# --- AREA UTAMA UNTUK INPUT DAN OUTPUT ---
st.subheader("📝 Masukkan Teks Anda di Sini")
contoh_teks = """
Saya baru beli Ponsel Cerdas X Pro, kameranya bagus tapi daya tahan baterai sangat buruk. Cuma tahan 5 jam!
Kecewa dengan Ponsel Cerdas X Pro. Layar sering tidak responsif dan kadang restart sendiri. Tidak direkomendasikan.
Untuk Laptop Gaming Z1, performanya kencang. Tapi masalahnya ada di keyboard yang panas saat dipakai main game berat.
Daya tahan baterai Ponsel Cerdas X Pro benar-benar payah. Sangat mengecewakan.
Laptop Gaming Z1 milik saya punya problem overheat. Kipasnya berisik sekali.
Secara umum Ponsel Cerdas X Pro bagus, hanya saja layarnya kurang cerah di bawah matahari.
Performa gaming di Laptop Gaming Z1 luar biasa, tapi keyboard jadi sangat panas setelah 30 menit.
"""
input_text = st.text_area("Salin dan tempel teks yang ingin dianalisis", contoh_teks, height=250)

if st.button("🚀 Analisis Sekarang!", type="primary"):
    if not input_text.strip():
        st.warning("Mohon masukkan teks untuk dianalisis.")
    elif not all([entitas_utama_keywords.strip(), entitas_atribut_keywords.strip(), entitas_deskriptor_keywords.strip()]):
        st.warning("Mohon definisikan kata kunci untuk semua kategori entitas di sidebar.")
    else:
        with st.spinner("Sedang memproses teks... Mohon tunggu."):
            
            # --- 1. PROSES ANALISIS N-GRAM ---
            st.subheader("📊 Analisis N-Gram")
            semua_ulasan_text = input_text.lower()
            tokens = word_tokenize(re.sub(r'[^a-zA-Z\s]', '', semua_ulasan_text))
            stop_words = set(stopwords.words('english')) # Bisa ditambahkan stopwords Indonesia jika perlu
            filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
            
            bigram_counts = Counter(ngrams(filtered_tokens, 2))
            trigram_counts = Counter(ngrams(filtered_tokens, 3))
            
            with st.expander("Lihat Frasa Paling Umum"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Top Bigram (2 Kata)**")
                    df_bigram = pd.DataFrame(bigram_counts.most_common(10), columns=['Bigram', 'Jumlah'])
                    df_bigram['Bigram'] = df_bigram['Bigram'].apply(lambda x: ' '.join(x))
                    st.dataframe(df_bigram, use_container_width=True)
                with col2:
                    st.write("**Top Trigram (3 Kata)**")
                    df_trigram = pd.DataFrame(trigram_counts.most_common(10), columns=['Trigram', 'Jumlah'])
                    df_trigram['Trigram'] = df_trigram['Trigram'].apply(lambda x: ' '.join(x))
                    st.dataframe(df_trigram, use_container_width=True)

            # --- 2. PROSES NER BERBASIS ATURAN ---
            st.subheader("🎨 Hasil Named Entity Recognition (NER)")
            
            # Mengambil keywords dari sidebar dan membersihkannya
            utama_list = [line.strip() for line in entitas_utama_keywords.split('\n') if line.strip()]
            atribut_list = [line.strip() for line in entitas_atribut_keywords.split('\n') if line.strip()]
            deskriptor_list = [line.strip() for line in entitas_deskriptor_keywords.split('\n') if line.strip()]

            matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
            matcher.add(entitas_utama_label, [nlp.make_doc(text) for text in utama_list])
            matcher.add(entitas_atribut_label, [nlp.make_doc(text) for text in atribut_list])
            matcher.add(entitas_deskriptor_label, [nlp.make_doc(text) for text in deskriptor_list])
            
            doc = nlp(input_text)
            matches = matcher(doc)
            
            spans = [Span(doc, start, end, label=nlp.vocab.strings[match_id]) for match_id, start, end in matches]
            doc.ents = spacy.util.filter_spans(spans)
            
            colors = {"PRODUK": "#85C1E9", "FITUR": "#FAD7A0", "OPINI": "#F1948A"}
            ent_labels = [entitas_utama_label, entitas_atribut_label, entitas_deskriptor_label]
            html = spacy.displacy.render(doc, style="ent", options={"ents": ent_labels, "colors": colors}, jupyter=False)
            st.write(html, unsafe_allow_html=True)

            # --- 3. PROSES INFORMATION EXTRACTION (IE) ---
            st.subheader("🗂️ Hasil Information Extraction (Tabel Terstruktur)")
            extracted_info = []
            
            # Memproses per kalimat untuk konteks yang lebih baik
            for sent in doc.sents:
                current_utama = [ent.text for ent in sent.ents if ent.label_ == entitas_utama_label]
                current_atribut = [ent.text for ent in sent.ents if ent.label_ == entitas_atribut_label]
                current_deskriptor = [ent.text for ent in sent.ents if ent.label_ == entitas_deskriptor_label]
                
                # Hanya ekstrak jika ada entitas utama dalam kalimat
                if current_utama:
                    # Asosiasikan setiap atribut dan deskriptor dengan entitas utama
                    for atribut in current_atribut:
                        for deskriptor in current_deskriptor:
                            extracted_info.append({
                                entitas_utama_label: current_utama[0],
                                entitas_atribut_label: atribut,
                                entitas_deskriptor_label: deskriptor,
                                'Sumber Kalimat': sent.text.strip()
                            })
                    # Jika hanya ada deskriptor tanpa atribut spesifik
                    if not current_atribut and current_deskriptor:
                        for deskriptor in current_deskriptor:
                            extracted_info.append({
                                entitas_utama_label: current_utama[0],
                                entitas_atribut_label: 'Umum',
                                entitas_deskriptor_label: deskriptor,
                                'Sumber Kalimat': sent.text.strip()
                            })

            if extracted_info:
                df_hasil = pd.DataFrame(extracted_info)
                st.dataframe(df_hasil, use_container_width=True)
                
                # Tombol Download
                csv = convert_df_to_csv(df_hasil)
                st.download_button(
                    label="📥 Unduh Hasil sebagai CSV",
                    data=csv,
                    file_name="hasil_ekstraksi.csv",
                    mime="text/csv",
                )
            else:
                st.info("Tidak ditemukan hubungan antar entitas yang terstruktur berdasarkan konfigurasi Anda.")