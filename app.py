import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de página y colores premium "Circus"
st.set_page_config(page_title="POS - Circus Chiquimula", layout="wide", initial_sidebar_state="expanded")

# CSS para el diseño corporativo elegante (Rojo, Dorado y Blanco)
st.markdown("""
    <style>
    .circus-title { font-size:42px; font-weight:900; color:#8B0000; text-align:center; text-transform:uppercase; letter-spacing: 2px; margin-bottom:0px; }
    .circus-subtitle { font-size:18px; color:#D4AF37; text-align:center; font-style:italic; margin-bottom:30px; }
    .metric-box { background-color:#FFFFFF; padding:20px; border-radius:12px; border-top:5px solid #8B0000; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); text-align:center;}
    .metric-value { font-size: 28px; font-weight: bold; color: #1B2631; }
    .metric-label { font-size: 14px; color: #7F8C8D; text-transform: uppercase; }
    div[data-testid="stSidebar"] { background-color: #FDFEFE; border-right: 2px solid #D4AF37; }
    .product-card { border: 1px solid #EAEDED; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="circus-title">🎪 CIRCUS CHIQUIMULA</div>', unsafe_allow_html=True)
st.markdown('<div class="circus-subtitle">Premium Snacks & Drinks • Est. 2020</div>', unsafe_allow_html=True)

# 2. Base de Datos Completa del Menú
if "inv_circus" not in st.session_state:
    productos_circus = [
        # --- GRANIZADAS (14 Sabores) ---
        {"Categoría": "Granizadas", "Producto": "Granizada de Limón", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🍋"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Fresa", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🍓"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Tamarindo", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🫘"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Mango", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🥭"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Piña", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🍍"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Mora", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🫐"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Chicle", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🍬"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Uva", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🍇"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Naranja", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🍊"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Coco", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🥥"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Maracuyá", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🟡"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Sandía", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🍉"},
        {"Categoría": "Granizadas", "Producto": "Granizada de Manzana Verde", "Precio (Q)": 15.0, "Stock": 100, "Icono": "🍏"},
        {"Categoría": "Granizadas", "Producto": "Granizada Especial / Mixta", "Precio (Q)": 20.0, "Stock": 100, "Icono": "🍧"},

        # --- CHOCO FRUTAS ---
        {"Categoría": "Choco Frutas", "Producto": "Chocobanano", "Precio (Q)": 5.0, "Stock": 100, "Icono": "🍌"},
        {"Categoría": "Choco Frutas", "Producto": "Chocofresa", "Precio (Q)": 8.0, "Stock": 100, "Icono": "🍓"},
        {"Categoría": "Choco Frutas", "Producto": "Chocosandía", "Precio (Q)": 10.0, "Stock": 100, "Icono": "🍉"},
        {"Categoría": "Choco Frutas", "Producto": "Chocococo", "Precio (Q)": 8.0, "Stock": 100, "Icono": "🥥"},
        {"Categoría": "Choco Frutas", "Producto": "Choco Piña", "Precio (Q)": 8.0, "Stock": 100, "Icono": "🍍"},

        # --- BEBIDAS Y LICUADOS ---
        {"Categoría": "Bebidas", "Producto": "Licuado de Frutas", "Precio (Q)": 18.0, "Stock": 50, "Icono": "🧋"},
        {"Categoría": "Bebidas", "Producto": "Frappé Especial", "Precio (Q)": 20.0, "Stock": 50, "Icono": "🥤"},
        {"Categoría": "Bebidas", "Producto": "Agua Pura Botella", "Precio (Q)": 5.0, "Stock": 100, "Icono": "💧"},
        {"Categoría": "Bebidas", "Producto": "Coca-Cola Lata", "Precio (Q)": 7.0, "Stock": 100, "Icono": "🥫"},
        {"Categoría": "Bebidas", "Producto": "Coca-Cola Botella", "Precio (Q)": 10.0, "Stock": 100, "Icono": "🍾"},

        # --- SNACKS Y CREPAS ---
        {"Categoría": "Snacks y Crepas", "Producto": "Bandeja de Mango Verde", "Precio (Q)": 12.0, "Stock": 50, "Icono": "🥭"},
        {"Categoría": "Snacks y Crepas", "Producto": "Tiras Ácidas", "Precio (Q)": 5.0, "Stock": 100, "Icono": "🌈"},
        {"Categoría": "Snacks y Crepas", "Producto": "Crepa Dulce", "Precio (Q)": 25.0, "Stock": 40, "Icono": "🥞"},
        {"Categoría": "Snacks y Crepas", "Producto": "Waffle Clásico", "Precio (Q)": 25.0, "Stock": 40, "Icono": "🧇"}
    ]
    st.session_state.inv_circus = pd.DataFrame(productos_circus)

if "historial_circus" not in st.session_state:
    st.session_state.historial_circus = pd.DataFrame(columns=["Hora", "Producto", "Monto (Q)"])

# 3. Función Interna de Venta
def registrar_venta(producto, precio):
    idx = st.session_state.inv_circus.index[st.session_state.inv_circus['Producto'] == producto].tolist()[0]
    if st.session_state.inv_circus.at[idx, 'Stock'] > 0:
        st.session_state.inv_circus.at[idx, 'Stock'] -= 1
        nueva_venta = {"Hora": datetime.now().strftime("%H:%M:%S"), "Producto": producto, "Monto (Q)": precio}
        st.session_state.historial_circus = pd.concat([st.session_state.historial_circus, pd.DataFrame([nueva_venta])], ignore_index=True)
        return True
    return False

# 4. Navegación en el Menú Lateral
st.sidebar.markdown("<h2 style='text-align: center; color: #8B0000;'>🎪 Menú de Operaciones</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
pagina = st.sidebar.radio("", ["✨ Punto de Venta (Caja)", "📦 Bodega / Inventario", "💎 Reporte Diario (Cierre)"])

# ==========================================
# PANTALLA 1: PUNTO DE VENTA (CAJA)
# ==========================================
if pagina == "✨ Punto de Venta (Caja)":
    
    ingresos_hoy = st.session_state.historial_circus["Monto (Q)"].sum() if not st.session_state.historial_circus.empty else 0.0
    ventas_hoy = len(st.session_state.historial_circus)
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-box"><div class="metric-label">Ventas Atendidas</div><div class="metric-value">{ventas_hoy}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-box"><div class="metric-label">Ingresos Brutos</div><div class="metric-value" style="color:#27AE60;">Q {ingresos_hoy:.2f}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-box"><div class="metric-label">Estado de Caja</div><div class="metric-value" style="color:#D4AF37;">ABIERTA</div></div>', unsafe_allow_html=True)
    st.write("---")

    categorias = st.session_state.inv_circus["Categoría"].unique()
    tabs = st.tabs(list(categorias))
    
    for i, cat in enumerate(categorias):
        with tabs[i]:
            df_cat = st.session_state.inv_circus[st.session_state.inv_circus["Categoría"] == cat]
            cols = st.columns(4) 
            for index, row in df_cat.reset_index().iterrows():
                with cols[index % 4]:
                    with st.container():
                        st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size:55px; line-height: 1;'>{row['Icono']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<h5 style='color:#8B0000; min-height: 40px; margin-top: 10px;'>{row['Producto']}</h5>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color:#7F8C8D; font-size: 13px; margin-bottom: 10px;'>Stock: {row['Stock']}</p>", unsafe_allow_html=True)
                        
                        if st.button(f"🛒 Q {row['Precio (Q)']:.2f}", key=f"btn_{row['Producto']}", use_container_width=True):
                            if registrar_venta(row['Producto'], row['Precio (Q)']):
                                st.toast(f"✅ ¡Despachado! {row['Producto']}", icon="🎪")
                                st.rerun()
                            else:
                                st.error(f"❌ Sin stock de {row['Producto']}")
                        st.markdown("</div>", unsafe_allow_html=True)
                st.write("") # Espaciador vertical

# ==========================================
# PANTALLA 2: BODEGA E INVENTARIO
# ==========================================
elif pagina == "📦 Bodega / Inventario":
    st.header("📦 Control de Insumos y Precios")
    st.write("Modifica el inventario de las frutas, hielo y productos. Si quieres editar los íconos o precios, haz doble clic directamente en la tabla.")
    
    inventario_editado = st.data_editor(
        st.session_state.inv_circus, 
        use_container_width=True, 
        num_rows="dynamic",
        column_config={
            "Precio (Q)": st.column_config.NumberColumn(format="Q %.2f"),
        }
    )
    if st.button("💾 Actualizar Bodega", type="primary"):
        st.session_state.inv_circus = inventario_editado
        st.success("✅ Los datos del menú han sido guardados exitosamente.")
        st.rerun()

# ==========================================
# PANTALLA 3: CIERRE DE CAJA Y REPORTES
# ==========================================
elif pagina == "💎 Reporte Diario (Cierre)":
    st.header("💎 Auditoría de Caja")
    
    if st.session_state.historial_circus.empty:
        st.info("La caja registradora está vacía. Aún no se han registrado ventas en esta sesión.")
    else:
        st.dataframe(st.session_state.historial_circus.iloc[::-1], use_container_width=True, hide_index=True)
        
        csv_data = st.session_state.historial_circus.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Cierre Z (Excel / CSV)",
            data=csv_data,
            file_name=f"Cierre_Circus_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime="text/csv",
            use_container_width=True
        )
