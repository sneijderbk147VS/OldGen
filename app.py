import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os
import urllib.parse

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="TG SISTEMA V.3", layout="wide")

# Inicializar estados
if "db" not in st.session_state: st.session_state.db = []
if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "num_pro" not in st.session_state: st.session_state.num_pro = 621 
if "num_con" not in st.session_state: st.session_state.num_con = 456 #
if "mostrar_registro_con" not in st.session_state: st.session_state.mostrar_registro_con = False

# --- LOGIN ---
if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>SISTEMA TG</h2>", unsafe_allow_html=True)
        u = st.text_input("👤 USUARIO")
        p = st.text_input("🔑 ACCESO", type="password")
        if st.button("DESBLOQUEAR"):
            if u == "10323102" and p == "2026":
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- INTERFAZ ---
tab1, tab2, tab3 = st.tabs(["📄 PROFORMA", "📜 CONTRATO", "🗄️ HISTORIAL"])

with tab1:
    st.markdown("### 🚀 EMISIÓN DE PROFORMA")
    with st.form("p_form"):
        c1, c2 = st.columns(2)
        cliente = c1.text_input("CLIENTE")
        telf = c1.text_input("WHATSAPP")
        monto = c2.number_input("MONTO S/", min_value=0.0)
        desc = st.text_area("DESCRIPCIÓN", height=100)
        if st.form_submit_button("💾 GUARDAR"):
            st.session_state.db.append({"TIPO": "PROFORMA", "Nro": st.session_state.num_pro, "Fecha": datetime.now().strftime("%d/%m/%Y"), "Cliente": cliente, "Monto": monto})
            st.session_state.num_pro += 1
            st.success("Proforma guardada con éxito.")
            st.rerun()

with tab2:
    st.markdown(f"### 📝 GESTIÓN DE CONTRATOS - PRÓXIMO: N° {st.session_state.num_con:06d}")
    
    # Botón principal para abrir el "bloquecito" de datos
    if not st.session_state.mostrar_registro_con:
        if st.button("➕ CREAR NUEVO CONTRATO", use_container_width=True):
            st.session_state.mostrar_registro_con = True
            st.rerun()
    
    # El "Bloquecito" o hojita pequeña para poner datos
    if st.session_state.mostrar_registro_con:
        with st.expander("📄 HOJA DE DATOS DEL CONTRATO", expanded=True):
            c_nom = st.text_input("Nombre del Cliente / Empresa")
            c_mon = st.number_input("Monto del Contrato S/", min_value=0.0)
            
            col_b1, col_b2 = st.columns(2)
            if col_b1.button("✅ GENERAR Y SUBIR NÚMERO"):
                if c_nom:
                    st.session_state.db.append({
                        "TIPO": "CONTRATO", 
                        "Nro": st.session_state.num_con, 
                        "Fecha": datetime.now().strftime("%d/%m/%Y"), 
                        "Cliente": c_nom, 
                        "Monto": c_mon
                    })
                    st.session_state.num_con += 1 # Sube el número solo al confirmar
                    st.session_state.mostrar_registro_con = False
                    st.success(f"Contrato N° {st.session_state.num_con-1:06d} registrado.")
                    st.rerun()
                else:
                    st.error("Por favor, pon el nombre del cliente.")
            
            if col_b2.button("❌ CANCELAR"):
                st.session_state.mostrar_registro_con = False
                st.rerun()

    st.divider()
    # Vista del contrato para llenar (JotForm)
    st.components.v1.iframe("https://form.jotform.com/260770452401045", height=700, scrolling=True)

with tab3:
    st.subheader("🗄️ REGISTROS GUARDADOS")
    if st.session_state.db:
        # Se muestra la tabla simple sin botones de Excel para que no falle
        import pandas as pd
        df = pd.DataFrame(st.session_state.db)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay registros todavía.")