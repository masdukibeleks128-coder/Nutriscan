import streamlit as st
# st.title('ksksksksks')
# st.write('this is streamlit')
# name = st.text_input('Insert your name')
# age = st.slider('pilih usia', 0, 100, 150)
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import os
import tempfile
import shutil
import importlib.util

# Kode untuk menyembunyikan header dan footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# import YOLO

def cek_library_ultralytics():
    spec = importlib.util.find_spec("ultralytics")
    if spec is None :
        return False
    return True

YOLO_AVAILABLE = cek_library_ultralytics()

if YOLO_AVAILABLE :
    from ultralytics import YOLO
    import torch
    from ultralytics.nn.tasks import DetectionModel
    
    torch.serialization.add_safe_globals([DetectionModel])

st.set_page_config(page_title="Nutriscan",
                   layout="wide")
# app.py
import streamlit as st

st.set_page_config(layout="wide", page_title="Nutriscan")

# Hapus padding bawaan Streamlit
st.markdown("""
<style>
  .block-container {
    padding-top: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
  }
</style>
""", unsafe_allow_html=True)

hero_html = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;600&display=swap');

  .hero {
    position: relative;
    min-height: 480px;
    background-image: url('https://raw.githubusercontent.com/masdukibeleks128-coder/deficiency-detection/main/background.jpeg');
    background-size: cover;
    background-position: center;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
  }
  .hero__overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to right, rgba(0,0,0,0.92) 0%, rgba(0,0,0,0.5) 60%, transparent 100%);
  }
  .hero__logo {
    position: absolute;
    top: 15px;
    left: 128px;
    z-index: 3;
    width: 50px;
    height: auto;
  }
  .hero__content {
    position: relative;
    z-index: 2;
    max-width: 600px;
    padding: 60px 48px; /* atas kanan bawah kiri */
    color: #ffffff;
  }
  .hero__content h1 {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 16px;
    margin-left: 80px;
  }
  .hero__content p {
    font-size: 15px;
    line-height: 1.75;
    color: rgba(255,255,255,0.88);
    margin-bottom: 32px;
    margin-left: 80px;
  }
</style>

<div class="hero">
  <div class="hero__overlay"></div>
  <img class="hero__logo" src="https://raw.githubusercontent.com/masdukibeleks128-coder/deficiency-detection/main/logo/logo utm 300 px.png" alt="logo">
  <div class="hero__content">
    <h1>NUTRISCAN</h1>
    <p>Nutriscan merupakan salah satu project dari mahasiswa Trunojoyo Madura guna untuk meningkatkan digitalisasi pertanian berbasis smart farming.
    Project tersebut berbasis deep learning dimana nantinya pengguna hanya memerlukan foto daun tanaman, yang dimana akan langsung dideteksi oleh model.
    Tingkatkan hasil panen dengan diagnosis nutrisi yang akurat. Scan gejala kekurangan hara langsung di lapangan tanpa perlu menunggu hasil lab yang lama.
    </p>
  </div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)

bg_url = "https://raw.githubusercontent.com/masdukibeleks128-coder/deficiency-detection/main/background.jpeg"
front_url = "https://raw.githubusercontent.com/masdukibeleks128-coder/deficiency-detection/main/background.jpeg"
logo_utm_url = "https://raw.githubusercontent.com/masdukibeleks128-coder/deficiency-detection/main/logo/logo utm 300 px.png" 
logo_fp_url = "https://raw.githubusercontent.com/masdukibeleks128-coder/deficiency-detection/main/logo/logo FP 300px.png"

# periksa apakah library YOLO tersedia
def cek_library():
    if not YOLO_AVAILABLE:
        st.error("Ultralytics tidak terpasang. silahkan instal dengnan perintah berikut:")
        st.code("pip install ultralytics")
        return False
    return True

# text tulisan utama
st.markdown(f"""
    <div style="
            position: absolute;
            top: -37px;
            left: -10px;
            background-color: white;
            width: 160px;
            height: 75px;
            border-radius: 40px;
            display: flex;
            align-items: center:
            justify-content: center;">
    </div>
<img src="{logo_utm_url}" style="
    position: absolute;
    top: -25px;
    left: 10px;
    width: 50px;">
<img src="{logo_fp_url}" style="
    position: absolute;
    top: -25px;
    left: 75px;
    width: 50px;">
<h1 style="color: white;"> NUTRISCAN </h1>
<h5 style="color: white;"> Maize Nutrient Scanner</h5>
</div>
""", unsafe_allow_html=True)

#cek library
if cek_library():
        uploaded_file = st.file_uploader("Upload your picture", type=['jpg','jpeg','png'])

        if uploaded_file: 
            #temporary files
            temp_dir = tempfile.mkdtemp()
            temp_file = os.path.join(temp_dir, "gambar.jpg")
            image = Image.open(uploaded_file)

            #resize ukuran gambar
            image = image.resize((300,300))
            image.save(temp_file)
    
            #show picture
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.image(image, caption="gambar yang diupload")
            st.markdown("</div>", unsafe_allow_html=True)

            #deteksi gambar
            if st.button("Deteksi gambar"):
                with st.spinner("sedang diproses"):
                    try:
                        # Pastikan safe globals terdaftar tepat sebelum load
                        torch.serialization.add_safe_globals([DetectionModel])
                        model = YOLO('best.pt')
                        hasil = model(temp_file)

                        # Ambil semua nama kelas dari model
                        nama_kelas = hasil[0].names
                        semua_kelas = list(nama_kelas.values())
                        confidence_dict = {nama: 0.0 for nama in semua_kelas}
                    
                        # Pastikan ada hasil deteksi
                        if len(hasil[0].boxes) == 0:
                             st.error("Gambar tidak dapat terdeteksi oleh model.")
                        else:
                            # Ambil hasil deteksi
                            boxes = hasil[0].boxes

                            # Ambil daftar nama kelas dan confidence
                            class_ids = boxes.cls.cpu().numpy().astype(int)
                            confidences = boxes.conf.cpu().numpy()

                            # Isi confidence tertinggi untuk setiap kelas yang muncul
                            for cls_id, conf in zip(class_ids, confidences):
                                nama = nama_kelas[cls_id]
                                if conf > confidence_dict[nama]:
                                    confidence_dict[nama] = float(conf)

                            # cari kelas dengan confidence tertinggi
                            objek_terdeteksi = max(confidence_dict, key=confidence_dict.get)

                            # Buat grafik keyakinan
                            grafik = go.Figure([go.Bar(x=list(confidence_dict.keys()), y=list(confidence_dict.values()))])
                            grafik.update_layout(title='Tingkat Keyakinan Deteksi',
                                                 xaxis_title='Defisiensi Hara',
                                                 yaxis_title='Tingkat keyakinan')

                            # Tampilkan hasil
                            st.success(f"Defisiensi terdeteksi: {objek_terdeteksi}")
                            st.plotly_chart(grafik)
    
                            # Tampilkan gambar hasil deteksi
                            st.image(hasil[0].plot(), caption="Hasil Deteksi", use_container_width=True)


                    except Exception as e :
                        st.error("gambar tidak dapat terdeteksi")
                        st.error(f"Error:{e}")

                    #hapus file sementara
                    finally:
                        shutil.rmtree(temp_dir,ignore_errors=True)

st.markdown(
"<div style='text-align: center;' class='footer'>Program Skripsi @2026</div>",
unsafe_allow_html=True
)


                    








