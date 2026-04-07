import streamlit as st
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import os
import tempfile
import shutil
import importlib.util

# ✅ set_page_config hanya SEKALI, di paling atas
st.set_page_config(page_title="Nutriscan", layout="wide")

# Sembunyikan header dan footer
st.markdown("""
<style>
  #MainMenu {visibility: hidden;}
  header {visibility: hidden;}
  footer {visibility: hidden;}
  .block-container {
    padding-top: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
  }

  /* ===== DESKTOP ===== */
  @media (min-width: 768px) {
    .hero { min-height: 500px; }
    .hero__content h1 { font-size: 42px; margin-left: 50px; }
    .hero__content p { font-size: 16px; margin-left: 50px; }
    .hero__logos { margin-left: 50px; }
    .hero__logos img { width: 70px; }
  }

  /* ===== MOBILE ===== */
  @media (max-width: 768px) {
    .hero { min-height: 400px; padding-top: 16px; }
    .hero__overlay {
      background: rgba(0,0,0,0.75) !important;
    }
    .hero__content { padding: 0 16px; max-width: 100%; }
    .hero__content h1 { font-size: 26px; margin-left: 16px; }
    .hero__content p { font-size: 13px; margin-left: 16px; }
    .hero__logos { margin-left: 16px; }
    .hero__logos img { width: 45px; }
  }
</style>
""", unsafe_allow_html=True)

# Cek library ultralytics
def cek_library_ultralytics():
    spec = importlib.util.find_spec("ultralytics")
    return spec is not None

YOLO_AVAILABLE = cek_library_ultralytics()

if YOLO_AVAILABLE:
    from ultralytics import YOLO
    import torch
    from ultralytics.nn.tasks import DetectionModel
    torch.serialization.add_safe_globals([DetectionModel])

# ===== HERO SECTION =====
hero_html = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;600&display=swap');

  .hero {
    position: relative;
    background-image: url('https://raw.githubusercontent.com/masdukibeleks128-coder/Nutriscan/main/background.jpeg');
    background-size: cover;
    background-position: center;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: flex-start;
    padding-top: 25px;
  }
  .hero__overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to right, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 40%, transparent 100%);
  }
  .hero__logos {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 30px;
    margin-bottom: 20px;
  }
  .hero__content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    padding: 0px 48px;
    color: #ffffff;
  }
  .hero__content h1 {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 16px;
  }
  .hero__content p {
    line-height: 1.75;
    color: rgba(255,255,255,0.88);
    margin-bottom: 32px;
    text-align: justify;
    hyphens: auto;
  }
</style>

<div class="hero">
  <div class="hero__overlay"></div>
  <div class="hero__content">
    <div class="hero__logos">
      <img src="https://raw.githubusercontent.com/masdukibeleks128-coder/Nutriscan/main/logo/logo_utm_300px.png" alt="logo utm">
      <img src="https://raw.githubusercontent.com/masdukibeleks128-coder/Nutriscan/main/logo/logo_FP_300px.png" alt="logo fp">
    </div>
    <h1>NUTRISCAN</h1>
    <p>Nutriscan merupakan salah satu project dari mahasiswa Trunojoyo Madura guna untuk
    meningkatkan digitalisasi pertanian berbasis smart farming. Project tersebut berbasis
    deep learning dimana nantinya pengguna hanya memerlukan foto daun tanaman, yang dimana
    akan langsung dideteksi oleh model. Tingkatkan hasil panen dengan diagnosis nutrisi
    yang akurat. Scan gejala kekurangan hara langsung di lapangan tanpa perlu menunggu
    hasil lab yang lama.</p>
  </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# ===== FITUR UTAMA =====
def cek_library():
    if not YOLO_AVAILABLE:
        st.error("Ultralytics tidak terpasang. Silahkan instal dengan perintah berikut:")
        st.code("pip install ultralytics")
        return False
    return True

if cek_library():
    uploaded_file = st.file_uploader("Upload foto daun tanaman", type=['jpg', 'jpeg', 'png'])

    if uploaded_file:
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "gambar.jpg")
        image = Image.open(uploaded_file)
        image = image.resize((300, 300))
        image.save(temp_file)

        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(image, caption="Gambar yang diupload")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Deteksi Gambar"):
            with st.spinner("Sedang diproses..."):
                try:
                    torch.serialization.add_safe_globals([DetectionModel])
                    model = YOLO('best.pt')
                    hasil = model(temp_file)

                    nama_kelas = hasil[0].names
                    semua_kelas = list(nama_kelas.values())
                    confidence_dict = {nama: 0.0 for nama in semua_kelas}

                    if len(hasil[0].boxes) == 0:
                        st.error("Gambar tidak dapat terdeteksi oleh model.")
                    else:
                        boxes = hasil[0].boxes
                        class_ids = boxes.cls.cpu().numpy().astype(int)
                        confidences = boxes.conf.cpu().numpy()

                        for cls_id, conf in zip(class_ids, confidences):
                            nama = nama_kelas[cls_id]
                            if conf > confidence_dict[nama]:
                                confidence_dict[nama] = float(conf)

                        objek_terdeteksi = max(confidence_dict, key=confidence_dict.get)

                        grafik = go.Figure([go.Bar(
                            x=list(confidence_dict.keys()),
                            y=list(confidence_dict.values())
                        )])
                        grafik.update_layout(
                            title='Tingkat Keyakinan Deteksi',
                            xaxis_title='Defisiensi Hara',
                            yaxis_title='Tingkat Keyakinan'
                        )

                        st.success(f"Defisiensi terdeteksi: {objek_terdeteksi}")
                        st.plotly_chart(grafik)
                        st.image(hasil[0].plot(), caption="Hasil Deteksi", use_container_width=True)

                except Exception as e:
                    st.error("Gambar tidak dapat terdeteksi")
                    st.error(f"Error: {e}")
                finally:
                    shutil.rmtree(temp_dir, ignore_errors=True)

# ===== FOOTER =====
st.markdown(
    "<div style='text-align: center; padding: 20px; color: gray;'>Program Skripsi @2026</div>",
    unsafe_allow_html=True
)
