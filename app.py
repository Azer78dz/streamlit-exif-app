# ********************************************************/
# Nom ......... : app.py
# Rôle ........ :  à utiliser dans le cours OIC chapitre 4 
# Auteur ...... : Bouaziz Ayoub Louaye
# Version ..... : V1.0 du 15/06/2025
# Licence ..... : réalisé dans le cadre du cours IOC    
# Description : Application Streamlit pour éditer EXIF et afficher des cartes GPS
# ********************************************************/

import streamlit as st
from PIL import Image, ExifTags
from exif import Image as ExifImage
import folium
from streamlit_folium import st_folium

# --- 1. Affichage d'une photo ---
st.title("🎉 Éditeur EXIF avec Streamlit")
st.write("## 📷 Photo actuelle")

uploaded_file = st.file_uploader("Téléchargez une image JPG", type=['jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Image téléchargée", use_column_width=True)

    # --- 2. Lecture EXIF existant ---
    exif_data = img.getexif()
    exif = {}
    for tag, value in exif_data.items():
        decoded = ExifTags.TAGS.get(tag, tag)
        exif[decoded] = value

    st.write("### Métadonnées EXIF actuelles :")
    st.json(exif)

    # --- 3. Formulaire pour modifier EXIF ---
    st.write("## ✏️ Modifier les métadonnées EXIF")
    artist = st.text_input("Auteur", exif.get('Artist', ''))
    copyright = st.text_input("Copyright", exif.get('Copyright', ''))
    gps_lat = st.number_input("Latitude (°)", value=36.75, format="%.6f")  # Par défaut Alger
    gps_lon = st.number_input("Longitude (°)", value=3.06, format="%.6f")

    if st.button("💾 Sauvegarder l'image avec nouveaux EXIF"):
        uploaded_file.seek(0)  # Rewind
        exif_img = ExifImage(uploaded_file)
        exif_img.make = artist
        exif_img.copyright = copyright

        # GPS sous forme DMS -> Décimal converti
        exif_img.gps_latitude = gps_lat
        exif_img.gps_latitude_ref = 'N' if gps_lat >= 0 else 'S'
        exif_img.gps_longitude = gps_lon
        exif_img.gps_longitude_ref = 'E' if gps_lon >= 0 else 'W'

        # Sauvegarde
        with open("photo_edited.jpg", "wb") as f:
            f.write(exif_img.get_file())

        st.success("✅ Image sauvegardée sous `photo_edited.jpg`")

    # --- 4. Affichage des coordonnées sur une carte ---
    st.write("## 🗺️ Carte de la position GPS")

    m = folium.Map(location=[gps_lat, gps_lon], zoom_start=10)
    folium.Marker([gps_lat, gps_lon], tooltip="Position GPS").add_to(m)
    st_folium(m, width=700)

    # --- 5. Carte voyages / destinations ---
    st.write("## 🌍 Mes voyages ou destinations rêvées")
    places = [
        {"name": "Alger", "coords": [36.75, 3.06]},
        {"name": "Paris", "coords": [48.8566, 2.3522]},
        {"name": "Tokyo", "coords": [35.6762, 139.6503]}
    ]
    m2 = folium.Map(location=[20, 0], zoom_start=2)

    for place in places:
        folium.Marker(place["coords"], tooltip=place["name"]).add_to(m2)

    folium.PolyLine([p["coords"] for p in places], color="blue").add_to(m2)
    st_folium(m2, width=700)

else:
    st.info("📂 Veuillez téléverser une image JPG pour commencer.")

