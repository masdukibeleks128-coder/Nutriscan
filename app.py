import streamlit as st
from PIL import Image
import numpy as np
import os
import tempfile
import shutil
import importlib.util

# ✅ set_page_config hanya SEKALI, di paling atas
st.set_page_config(page_title="Nutriscan", layout="wide")

# Sembunyikan header dan footer
st.markdown("""
<style>
  html, body {
    overflow-x: hidden !important;
    max-width: 100vw !important;
  }
  
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
  @media (min-width: 480px) {
    .hero { min-height: 500px; }
    .hero__content h1 { font-size: 42px; margin-left: 10px; }
    .hero__content h2 { font-size: 24px; margin-left: 10px; }
    .hero__content p { font-size: 16px; margin-left: 10px; }
    .hero__logos { margin-left: 10px; }
    .hero__logos img { width: 70px; }
  }

  /* ===== MOBILE ===== */
  @media (max-width: 480px) {
    .hero { min-height: 400px; padding-top: 16px; }
    .hero__overlay {
      background: linear-gradient(
        to bottom,
        rgba(0,0,0,0.9) 0%, /* atas gelap */
        rgba(0,0,0,0.4) 30%, /* tengah */
        rgba(0,0,0,0.4) 70%, /* tengah */
        rgba(0,0,0,0.9) 100% /* bawah gelap */
      ),
      rgba(0,0,0,0.5) !important;
    }
    .hero__content { padding: 0 16px; max-width: 100%; }
    .hero__content h1 { font-size: 26px; margin-left: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);}
    .hero__content h2 { font-size: 18px; margin-left: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);}
    .hero__content p { font-size: 13px; margin-left: 5px; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);}
    .hero__logos { margin-left: 5px; }
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
  @font-face {
      font-family: 'Aspirer Neue' ;
      src: url('https://raw.githubusercontent.com/masdukibeleks128-coder/Nutriscan/main/assets/fonts/LTAspirerNeue-SemiBold.otf') format('opentype');
      font-weight: 700;
  }
  .hero {
    position: relative;
    background-image: url('https://raw.githubusercontent.com/masdukibeleks128-coder/Nutriscan/main/background2.jpg');
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
    background: 
      linear-gradient(
        to right, 
        rgba(0,0,0,1) 0%, 
        rgba(0,0,0,1) 40%, 
        transparent 100%)
      ;
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
    font-family: 'Aspirer Neue', serif;
    font-weight: 700;
    line-height: 1.1;
    margin-top: 0 !important;
    margin-bottom: 1px !important;
  }
  .hero__content h2 {
    font-family: 'Aspirer Neue', serif;
    font-weight: 700;
    line-height: 1.1;
    margin-top: 0 !important;
    margin-bottom: 24px !important;
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
    <h2>Maize Nutrient Scanner</h2>
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

# ===== Margin Section =====
st.markdown("""
<style>
@media (min-width: 481px) {
  [data-testid="stFileUploader"],
  [data-testid="stImage"],
  [data-testid="stButton"],
  [data-testid="stHorizontalBlock"],
  [data-testid="stPlotlyChart"],
  [data-testid="stAlert"] {
    margin-left: 30px !important;
    margin-right: 30px !important;
  }
}
@media (max-width: 480px) {
  [data-testid="stFileUploader"],
  [data-testid="stImage"],
  [data-testid="stButton"],
  [data-testid="stHorizontalBlock"],
  [data-testid="stPlotlyChart"],
  [data-testid="stAlert"] {
    margin-left: 15px !important;
    margin-right: 15px !important;
  }
}
</style>
""", unsafe_allow_html=True)
# ===== FEEDBACK BANNER =====
FORM_URL = "https://forms.gle/WKv1E8zT8AeXMiZ28"

def show_feedback_banner():
    st.markdown(f"""
    <style>
    .feedback-banner {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        background: white;
        max-width: 480px;
        border: 0.5px solid #e0e0e0;
        border-left: 3px solid #639922;
        border-radius: 10px;
        padding: 14px 16px;
        margin: 16px auto 8px auto;
    }}
    .feedback-banner-left {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .feedback-icon {{
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #EAF3DE;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    .feedback-text p {{
        font-size: 14px;
        font-weight: 600;
        color: #1a1a1a;
        margin: 0 0 2px 0;
    }}
    .feedback-text span {{
        font-size: 12px;
        color: #666;
    }}
    .feedback-btn {{
        flex-shrink: 0;
        font-size: 13px;
        font-weight: 500;
        color: white !important;
        background: #639922;
        border: none;
        padding: 8px 14px;
        border-radius: 8px;
        cursor: pointer;
        text-decoration: none !important;
        white-space: nowrap;
    }}
    .feedback-btn:hover {{
        background: #3B6D11;
        color: white !important;
    }}
    </style>

    <div class="feedback-banner">
        <div class="feedback-banner-left">
            <div class="feedback-icon">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M8 1.5C4.41 1.5 1.5 4.41 1.5 8s2.91 6.5 6.5 6.5S14.5 11.59 14.5 8 11.59 1.5 8 1.5zm.5 9.75h-1v-4h1v4zm0-5.5h-1v-1h1v1z" fill="#3B6D11"/>
                </svg>
            </div>
            <div class="feedback-text">
                <p>Ragu dengan hasil deteksi ?</p>
                <span>Bantu kami tingkatkan akurasi model</span>
            </div>
        </div>
        <a href="{FORM_URL}" target="_blank" class="feedback-btn">Beri Feedback</a>
    </div>
    """, unsafe_allow_html=True)
    
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
        image = Image.open(uploaded_file).convert("RGB")
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
                    hasil = model(temp_file, conf = 0.69)

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
                        
                        st.success(f"Defisiensi terdeteksi: {objek_terdeteksi}")

                        confidence_tertinggi = confidence_dict[objek_terdeteksi]
                        
                        rekomendasi = {
                          "N_Deficiency": {
                            "gejala": "Defisiensi Nitrogen (N)",
                            "pupuk": "pupuk Urea atau ZA (Nitrogen)"
                          },
                          "P_Deficiency": {
                            "gejala": "Defisiensi Fosfor (P)",
                            "pupuk": "pupuk SP-36 atau TSP (Fosfor)"
                          },
                          "K_Deficiency": {
                            "gejala": "Defisiensi Kalium (K)",
                            "pupuk": "pupuk KCL atau ZK (Kalium)"
                          },
                          "Nutrient_Sufficiency": None
                        }
                        
                        st.markdown("""
                        <style>
                          /* Desktop : berdampingan ukuran sedang */
                          @media (min-width: 481px) {
                            [data-testid="column"] {
                              padding: 10px !important;
                            }
                          /* Paksa gambar hasil deteksi tidak meluber */
                            [data-testid="stImage"] img {
                              max-width: 50% !important;
                              height: auto !important;
                              object-fit: contain;
                            }
                          }
                          /* Mobile: tetap berdampingan tapi kecil */
                          @media (max-width: 480px) {
                            [data-testid="stHorizontalBlock"] {
                              flex-wrap: wrap !important;
                              overflow: hidden !important; /* cegah scroll kanan */
                            }
                            [data-testid="column"] {
                              min-width: 0 !important;
                              flex: 1 1 50% !important; # masing-masing 50% layar
                              padding: 2px !important;
                              display: flex !important;
                              flex-direction: column !important;
                              align-items: center !important;
                            }
                            [data-testid="stHorizontalBlock"] [data-testid="column"] > div {
                              display: flex !important;
                              flex-direction: column !important;
                              align-items: center !important;
                              width: 100% !important;
                            }
                            [data-testid="stHorizontalBlock"] [data-testid="stImage"] {
                              display: flex !important;
                              justify-content: center !important;
                              width: 100% !important;
                            }
                            [data-testid="stHorizontalBlock"] [data-testid="stImage"] img {
                              width: 100% !important;
                              height: auto !important;
                              max-width: 140px !important;
                            }
                          }
                        </style>
                        """, unsafe_allow_html=True)

                    # teks dengan label rekomendasi
                        col1, col2 = st.columns([1, 1.5])
                        with col1:
                          st.markdown("<p style='font-size: 14px; text-align: center;'>Hasil Deteksi</p>", unsafe_allow_html=True)
                          st.image(hasil[0].plot(), use_column_width=True)

                        with col2:
                          info = rekomendasi.get(objek_terdeteksi)
                          st.markdown("""
                              <style>
                              .kotak-rekomendasi {
                                padding: 15px;
                                padding-right: 40px;
                                border-radius: 10px;
                                font-size: 20px;
                                color: white;
                                line-height: 1.6;
                                text-align: justify;
                                word-wrap: break-word;
                                word-break: break-word;
                                overflow-wrap: break-word;
                                white-space: normal;
                                max-width: 600px !important;
                                box-sizzing: border-box !important;
                              }
                              </style>
                          """, unsafe_allow_html=True)
                          
                          if info is None:
                            st.markdown("""
                              <div class='kotak-rekomendasi'>
                                Berdasarkan hasil deteksi model, tanaman tidak menunjukkan gejala defisiensi hara. 
                                maka tidak diperlukan penambahan pupuk khusus.
                              </div>
                            """, unsafe_allow_html=True)
                          else:
                            st.markdown(f"""
                              <div class='kotak-rekomendasi'>
                                  Berdasarkan hasil deteksi model, tanaman menunjukkan gejala <strong>{info['gejala']}</strong>
                                  dengan tingkat keyakinan model sebesar <strong>{confidence_tertinggi*100:.2f}%</strong>, 
                                  maka diperlukan penambahan <strong>{info['pupuk']}</strong>.
                              </div>
                            """, unsafe_allow_html=True)

                        show_feedback_banner()
                      
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
