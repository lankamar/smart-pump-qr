import streamlit as st
from datetime import datetime
import urllib.parse

# Configuración de Página
st.set_page_config(page_title="Smart Pump Tracker", page_icon="🏥")

# Estilos CSS para móvil
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 3em;
        font-weight: bold;
    }
    .success-msg {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
    }
    /* Estilo tipo App Nativa */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    h1 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
        text-align: center;
    }
    .stSelectbox label {
        font-size: 1.2rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Obtener parámetros de la URL (del QR)
query_params = st.query_params
pump_id = query_params.get("bomba", "Desconocida")
pump_serial = query_params.get("serie", "N/A")

st.markdown(f"<h1 style='font-size: 24px;'>🏥 Bomba #{pump_id}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>Serie: {pump_serial} | 🕒 {datetime.now().strftime('%H:%M')}</p>", unsafe_allow_html=True)
st.markdown("---")

# Selección de Rol con Iconos
role = st.radio("👤 ¿Quién reporta?", ["Seleccionar...", "🍎 Nutrición", "💉 Enfermería"], index=0, horizontal=True)

recipient_email = "alimentacionenteral@hospitaldeclinicas.uba.ar"

if role == "🍎 Nutrición":
    st.info("Complete los datos para informar la indicación.")
    
    col1, col2 = st.columns(2)
    with col1:
        signer = st.text_input("✍️ Su Nombre:", placeholder="Ej: Juan Pérez")
    with col2:
        bed_input = st.text_input("🛏️ Código de Cama:", placeholder="Ej: 11432")

    # Lógica de Camas Hospital
    bed_details = ""
    if bed_input and bed_input.isdigit():
        bed_num = int(bed_input)
        floor = bed_num // 1000
        room = (bed_num % 1000) // 100
        bed = bed_num % 100
        
        bed_details = f"Piso {floor} | Sala {room} | Cama {bed}"
        st.success(f"📍 Ubicación detectada: **{bed_details}**")
    
    indication = st.text_area("💊 Indicación / Fórmula:", placeholder="Ej: Nutrison Energy 1000ml a 63ml/h")
    
    if signer and bed_input and indication:
        subject = f"ACTUALIZACIÓN BOMBA #{pump_id} - Cama {bed_input}"
        body = f"""Hola,
        
Reporto actualización de bomba:
- Bomba: #{pump_id} ({pump_serial})
- Código Cama: {bed_input}
- Ubicación: {bed_details}
- Indicación: {indication}
- Firma: {signer}
- Hora: {datetime.now().strftime('%H:%M')}

Saludos."""
        
        # Codificar para URL
        subject_enc = urllib.parse.quote(subject)
        body_enc = urllib.parse.quote(body)
        mailto_link = f"mailto:{recipient_email}?subject={subject_enc}&body={body_enc}"
        
        st.markdown(f"""
            <a href="{mailto_link}" target="_blank" style="text-decoration: none;">
                <button style="
                    width: 100%;
                    background-color: #28a745;
                    color: white;
                    padding: 15px;
                    border: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 20px;">
                    ✅ GENERAR CORREO
                </button>
            </a>
            <p style='text-align: center; font-size: 0.8rem; margin-top: 10px; color: gray;'>
                Se abrirá su app de correo para enviar.
            </p>
        """, unsafe_allow_html=True)


elif role == "💉 Enfermería":
    st.success("Informe que la bomba ya no se está utilizando.")
    
    signer = st.text_input("✍️ Su Nombre:", placeholder="Ej: Lic. María Gomez")
    
    if signer:
        subject = f"DISPONIBILIDAD BOMBA #{pump_id}"
        body = f"""Hola,
        
La bomba #{pump_id} ({pump_serial}) ha sido liberada y está DISPONIBLE para su retiro o limpieza.

- Firma: {signer}
- Hora: {datetime.now().strftime('%H:%M')}

Saludos,
Enfermería."""
        
        # Codificar para URL
        subject_enc = urllib.parse.quote(subject)
        body_enc = urllib.parse.quote(body)
        mailto_link = f"mailto:{recipient_email}?subject={subject_enc}&body={body_enc}"
        
        st.markdown(f"""
            <a href="{mailto_link}" target="_blank" style="text-decoration: none;">
                <button style="
                    width: 100%;
                    background-color: #17a2b8;
                    color: white;
                    padding: 15px;
                    border: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 20px;">
                    🟢 INFORMAR DISPONIBLE
                </button>
            </a>
            <p style='text-align: center; font-size: 0.8rem; margin-top: 10px; color: gray;'>
                Se abrirá su app de correo para enviar.
            </p>
        """, unsafe_allow_html=True)

# Debug info (borrar en producción)
with st.expander("Información Técnica"):
    st.write(query_params)
