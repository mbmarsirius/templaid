import streamlit as st, pydicom, io, re, os
from PIL import Image
from docxtpl import DocxTemplate
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
                     # .env içindeki OPENAI_API_KEY'i yükler

PHRASES = {
    "EFF.": "Dirsek eklem içi efüzyon.",
    "FRAC.": "Kemikte kırık hattı.",
}

def dicom_to_png(upload):
    ds = pydicom.dcmread(upload)
    img = Image.fromarray(ds.pixel_array).conver"RGB")
    meta = {
        "Accession": getattr(ds, "AccessionNumber", ""),
        "Modality": getattr(ds, "Modality", "DX"),
    }
    return img, meta

def build_report(findings):
    teknik = "Tek projeksiyon dijital grafi."
    kars = "Önceki inceleme ile karşılaştırılamadı."
    bulgular = "\n".join(findings) or "—"
    sonuc = bulgular
    return teknik, kars, bulgular, sonuc

def to_docx(blocks):
    TEMPLATE = Path(__file__).with_name("sb_template.docx")
    tpl = DocxTemplate(TEMPLATE)
    ctx = dict(zip(
        ["TEKNIK", "KARSILASTIRMA", "BULGULAR", "SONUC"],
        blocks))
    tpl.render(ctx)
    bio = io.BytesIO()
    tpl.save(bio)
    bio.seek(0)
    return bio


st.set_page_config(page_title="TemplAID – Taslak Rapor", layout="wide")
st.title("🩻 TemplAID – Radyoloji Rapor Taslağı")

upl = st.file_uploader("Azmed DICOM dosyasını yükleyin", type=["dcm"])
if upl:
    img, _ = dicom_to_png(upl)
    st.image(img, width=380)

    # Overlay metninden etiket yakala
    tags = re.findall(rb"(EFF\.|FRAC\.)", img.tobytes())
    findings = [PHRASES[t.decode()] for t in tags if t.decode() in PHRASES]

    if st.button("Taslak Rapor Oluştur"):
        blks = build_report(findings)
        st.subheader("BULGULAR"); st.write(blks[2])
        st.download_button("DOCX indir", to_docx(blks), "taslak_rapor.docx")

