import streamlit as st
import pandas as pd
from datetime import date

# Configuración básica de la página
st.set_page_config(page_title="Control de Negocios", layout="centered")

st.title("📊 Panel de Control de Negocios")

# Menú lateral para elegir el negocio
negocio = st.sidebar.selectbox(
    "Selecciona el negocio a gestionar:",
    ["Cerrajería Automotriz", "Importadora de Vehículos", "Snacks y Granizadas"]
)

st.header(f"Registrar movimiento en: {negocio}")

# Formulario de ingreso de datos
with st.form("registro_ventas", clear_on_submit=True):
    fecha = st.date_input("Fecha", date.today())
    
    if negocio == "Cerrajería Automotriz":
        descripcion = st.text_input("Servicio realizado (Ej. Copia llave, Programación)")
    elif negocio == "Importadora de Vehículos":
        descripcion = st.text_input("Vehículo/Placa/Cliente (Ej. Renta Toyota Corolla)")
    else:
        descripcion = st.selectbox("Producto", ["Granizada de frutas", "Chocobanano", "Waffle", "Crepa", "Frappé", "Bandeja Mango"])
    
    ingreso = st.number_input("Ingreso (Q)", min_value=0.0, step=10.0)
    costo = st.number_input("Costo/Gasto (Q)", min_value=0.0, step=10.0)
    
    submit = st.form_submit_button("Guardar Registro")

if submit:
    ganancia = ingreso - costo
    st.success(f"✅ ¡Guardado! {descripcion} | Ganancia: Q{ganancia}")
    # Aquí el código se conectaría a una base de datos o un Excel para guardar el historial.
