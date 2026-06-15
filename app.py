import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración principal de la página
st.set_page_config(page_title="Caja - Snacks y Granizadas", layout="wide", initial_sidebar_state="expanded")

# 2. Inicialización de la Base de Datos con todos tus productos
if "inventario" not in st.session_state:
    productos_iniciales = [
        # --- GRANIZADAS ---
        {"Producto": "Granizada de Limón", "Categoría": "Granizadas", "Precio (Q)": 15.0, "Stock": 50, "Imagen": "https://placehold.co/400x300/f0f4c3/000000?text=Foto+Limon"},
        {"Producto": "Granizada de Fresa", "Categoría": "Granizadas", "Precio (Q)": 15.0, "Stock": 50, "Imagen": "https://placehold.co/400x300/ffcdd2/000000?text=Foto+Fresa"},
        {"Producto": "Granizada de Tamarindo", "Categoría": "Granizadas", "Precio (Q)": 15.0, "Stock": 50, "Imagen": "https://placehold.co/400x300/d7ccc8/000000?text=Foto+Tamarindo"},
        {"Producto": "Granizada de Mango", "Categoría": "Granizadas", "Precio (Q)": 15.0, "Stock": 50, "Imagen": "https://placehold.co/400x300/ffe082/000000?text=Foto+Mango"},
        {"Producto": "Granizada Especial/Mixta", "Categoría": "Granizadas", "Precio (Q)": 20.0, "Stock": 40, "Imagen": "https://placehold.co/400x300/e1bee7/000000?text=Foto+Mixta"},
        
        # --- CHOCO FRUTAS ---
        {"Producto": "Chocobanano", "Categoría": "Choco Frutas", "Precio (Q)": 5.0, "Stock": 80, "Imagen": "https://placehold.co/400x300/fff9c4/000000?text=Chocobanano"},
        {"Producto": "Chocofresa", "Categoría": "Choco Frutas", "Precio (Q)": 8.0, "Stock": 60, "Imagen": "https://placehold.co/400x300/ffcdd2/000000?text=Chocofresa"},
        {"Producto": "Chocosandía", "Categoría": "Choco Frutas", "Precio (Q)": 10.0, "Stock": 30, "Imagen": "https://placehold.co/400x300/c8e6c9/000000?text=Chocosandia"},
        {"Producto": "Chocococo", "Categoría": "Choco Frutas", "Precio (Q)": 8.0, "Stock": 40, "Imagen": "https://placehold.co/400x300/ffffff/000000?text=Chocococo"},
        
        # --- BEBIDAS Y LICUADOS ---
        {"Producto": "Agua Pura Botella", "Categoría": "Bebidas y Licuados", "Precio (Q)": 5.0, "Stock": 100, "Imagen": "https://placehold.co/400x300/b3e5fc/000000?text=Agua+Pura"},
        {"Producto": "Coca-Cola Lata", "Categoría": "Bebidas y Licuados", "Precio (Q)": 7.0, "Stock": 60, "Imagen": "https://placehold.co/400x300/ef9a9a/000000?text=Coca+Lata"},
        {"Producto": "Coca-Cola Botella", "Categoría": "Bebidas y Licuados", "Precio (Q)": 10.0, "Stock": 60, "Imagen": "https://placehold.co/400x300/ef9a9a/000000?text=Coca+Botella"},
        {"Producto": "Licuado de Frutas", "Categoría": "Bebidas y Licuados", "Precio (Q)": 18.0, "Stock": 40, "Imagen": "https://placehold.co/400x300/f3e5f5/000000?text=Licuado"},
        
        # --- SNACKS Y CREPAS ---
        {"Producto": "Bandeja Mango Verde", "Categoría": "Snacks y Crepas", "Precio (Q)": 12.0, "Stock": 35, "Imagen": "https://placehold.co/400x300/cddc39/000000?text=Mango+Verde"},
        {"Producto": "Tiras Ácidas", "Categoría": "Snacks y Crepas", "Precio (Q)": 5.0, "Stock": 100, "Imagen": "https://placehold.co/400x300/ffecb3/000000?text=Tiras+Acidas"},
        {"Producto": "Crepa", "Categoría": "Snacks y Crepas", "Precio (Q)": 25.0, "Stock": 30, "Imagen": "https://placehold.co/400x300/ffe0b2/000000?text=Foto+Crepa"}
    ]
    st.session_state.inventario = pd.DataFrame(productos_iniciales)

if "historial_ventas" not in st.session_state:
    st.session_state.historial_ventas = pd.DataFrame(columns=["Hora", "Producto", "Monto (Q)"])

# 3. Función oculta que registra la venta
def registrar_venta(producto, precio):
    idx = st.session_state.inventario.index[st.session_state.inventario['Producto'] == producto].tolist()[0]
    if st.session_state.inventario.at[idx, 'Stock'] > 0:
        st.session_state.inventario.at[idx, 'Stock'] -= 1
        nueva_venta = {"Hora": datetime.now().strftime("%H:%M:%S"), "Producto": producto, "Monto (Q)": precio}
        st.session_state.historial_ventas = pd.concat([st.session_state.historial_ventas, pd.DataFrame([nueva_venta])], ignore_index=True)
        return True
    return False

# 4. Diseño del Menú Lateral (Navegación)
st.sidebar.title("🍔 Sistema POS")
st.sidebar.write("Elige la sección:")
pagina_actual = st.sidebar.radio("", ["🏠 Menú Principal (Caja)", "📦 Inventario", "💰 Ingresos y Ventas"])

# Cálculo de dinero en caja
dinero_caja = st.session_state.historial_ventas["Monto (Q)"].sum() if not st.session_state.historial_ventas.empty else 0.0
st.sidebar.markdown("---")
st.sidebar.success(f"### 💵 Caja Hoy:\n## Q {dinero_caja:.2f}")

# ==========================================
# PANTALLA 1: MENÚ PRINCIPAL (BOTONES CON FOTOS)
# ==========================================
if pagina_actual == "🏠 Menú Principal (Caja)":
    st.title("🛒 Caja Registradora")
    
    tabs = st.tabs(["🍧 Granizadas", "🍫 Choco Frutas", "🥤 Bebidas y Licuados", "🍟 Snacks y Crepas"])
    
    def construir_catalogo(categoria):
        df_cat = st.session_state.inventario[st.session_state.inventario["Categoría"] == categoria]
        cols = st.columns(3)
        for index, row in df_cat.reset_index().iterrows():
            with cols[index % 3]:
                with st.container():
                    st.image(row["Imagen"], use_column_width=True)
                    st.markdown(f"<h5 style='text-align: center;'>{row['Producto']}</h5>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; color: gray; font-size: 14px;'>Stock: {row['Stock']}</p>", unsafe_allow_html=True)
                    
                    if st.button(f"🛒 Cobrar Q {row['Precio (Q)']:.2f}", key=f"btn_{row['Producto']}", use_container_width=True):
                        if registrar_venta(row['Producto'], row['Precio (Q)']):
                            st.toast(f"✅ ¡Vendido! 1x {row['Producto']}", icon="💸")
                            st.rerun()
                        else:
                            st.error(f"❌ No hay {row['Producto']} en inventario.")
                st.write("")

    with tabs[0]: construir_catalogo("Granizadas")
    with tabs[1]: construir_catalogo("Choco Frutas")
    with tabs[2]: construir_catalogo("Bebidas y Licuados")
    with tabs[3]: construir_catalogo("Snacks y Crepas")

# ==========================================
# PANTALLA 2: INVENTARIO
# ==========================================
elif pagina_actual == "📦 Inventario":
    st.title("📦 Control de Existencias")
    st.info("Haz doble clic en cualquier número de 'Stock' o 'Precio' para editarlo. Luego presiona el botón azul para guardar.")
    
    inventario_modificado = st.data_editor(
        st.session_state.inventario.drop(columns=["Imagen"]),
        use_container_width=True,
        num_rows="dynamic"
    )
    
    if st.button("💾 Guardar Nuevos Valores", type="primary"):
        imagenes = st.session_state.inventario["Imagen"]
        st.session_state.inventario = inventario_modificado
        st.session_state.inventario["Imagen"] = imagenes
        st.success("✅ Inventario actualizado correctamente.")
        st.rerun()

# ==========================================
# PANTALLA 3: INGRESOS Y VENTAS
# ==========================================
elif pagina_actual == "💰 Ingresos y Ventas":
    st.title("💰 Historial de Caja")
    
    if st.session_state.historial_ventas.empty:
        st.write("Aún no has hecho ventas hoy.")
    else:
        st.dataframe(st.session_state.historial_ventas.iloc[::-1], use_container_width=True)
