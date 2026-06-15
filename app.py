import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de diseño de la página corporativa
st.set_page_config(
    page_title="Punto de Venta e Inventario - Snacks & Granizadas", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuales personalizados
st.markdown("""
    <style>
    .main-title { font-size:32px; font-weight:bold; color:#2E4053; margin-bottom:20px; }
    .metric-box { background-color:#F8F9F9; padding:15px; border-radius:10px; border-left:5px solid #5DADE2; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🍓 Sistema de Control Profesional - Antojos & Granizadas</div>', unsafe_allow_html=True)

# 2. Base de Datos en Memoria (Inicialización)
if "inventario" not in st.session_state:
    productos_iniciales = [
        {"Producto": "Granizada Regular", "Categoría": "Granizadas", "Precio Venta (Q)": 15.0, "Existencias": 60},
        {"Producto": "Granizada Especial (Sabores/Mix)", "Categoría": "Granizadas", "Precio Venta (Q)": 20.0, "Existencias": 45},
        {"Producto": "Chocobanano", "Categoría": "Frutas con Chocolate", "Precio Venta (Q)": 5.0, "Existencias": 100},
        {"Producto": "Chocofresa", "Categoría": "Frutas con Chocolate", "Precio Venta (Q)": 8.0, "Existencias": 70},
        {"Producto": "Frappé", "Categoría": "Bebidas Frías", "Precio Venta (Q)": 18.0, "Existencias": 40},
        {"Producto": "Crepa Dulce", "Categoría": "Snacks", "Precio Venta (Q)": 25.0, "Existencias": 35},
        {"Producto": "Agua Pura Botella", "Categoría": "Bebidas", "Precio Venta (Q)": 5.0, "Existencias": 80},
        {"Producto": "Coca-Cola", "Categoría": "Bebidas", "Precio Venta (Q)": 7.0, "Existencias": 48},
        {"Producto": "Bandeja de Mango Verde", "Categoría": "Snacks", "Precio Venta (Q)": 12.0, "Existencias": 30}
    ]
    st.session_state.inventario = pd.DataFrame(productos_iniciales)

if "historial_ventas" not in st.session_state:
    st.session_state.historial_ventas = pd.DataFrame(columns=["Fecha y Hora", "Producto", "Cantidad", "Precio Unitario (Q)", "Total Recaudado (Q)"])

# 3. Métricas Principales en la barra superior
total_ventas_Q = st.session_state.historial_ventas["Total Recaudado (Q)"].sum() if not st.session_state.historial_ventas.empty else 0.0
productos_alerta = st.session_state.inventario[st.session_state.inventario["Existencias"] <= 10]

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-box"><h4>💰 Ventas del Día</h4><h2>Q {total_ventas_Q:.2f}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><h4>📦 Productos en Menú</h4><h2>{len(st.session_state.inventario)} Items</h2></div>', unsafe_allow_html=True)
with col3:
    color_alerta = "#E74C3C" if len(productos_alerta) > 0 else "#2ECC71"
    st.markdown(f'<div class="metric-box" style="border-left-color:{color_alerta}"><h4>🚨 Alertas de Stock Bajo</h4><h2>{len(productos_alerta)} Productos</h2></div>', unsafe_allow_html=True)

st.write("---")

# 4. Creación de las Pestañas de Navegación
tab1, tab2, tab3 = st.tabs(["🛒 Registrar Ventas (POS)", "📦 Gestión de Inventario y Precios", "📈 Historial y Reportes"])

# ==========================================
# PESTAÑA 1: PUNTO DE VENTA (REGISTRAR VENTAS)
# ==========================================
with tab1:
    st.subheader("🛒 Nueva Orden de Venta")
    
    col_izq, col_der = st.columns([2, 1])
    
    with col_izq:
        categorias = ["Todos"] + list(st.session_state.inventario["Categoría"].unique())
        cat_seleccionada = st.selectbox("Filtrar por tipo de producto:", categorias)
        
        if cat_seleccionada == "Todos":
            df_filtrado = st.session_state.inventario
        else:
            df_filtrado = st.session_state.inventario[st.session_state.inventario["Categoría"] == cat_seleccionada]
            
        lista_productos = df_filtrado["Producto"].tolist()
        producto_sel = st.selectbox("Selecciona el producto vendido:", lista_productos)
        
        datos_prod = st.session_state.inventario[st.session_state.inventario["Producto"] == producto_sel].iloc[0]
        precio_actual = datos_prod["Precio Venta (Q)"]
        stock_actual = datos_prod["Existencias"]
        
        st.info(f"💡 **Precio unitario:** Q {precio_actual:.2f} | **Disponibles en inventario:** {stock_actual} unidades")

    with col_der:
        cantidad = st.number_input("Cantidad a vender:", min_value=1, max_value=int(stock_actual) if stock_actual > 0 else 1, value=1, step=1)
        total_pago = cantidad * precio_actual
        st.markdown(f"### Total a Cobrar:\n## Q {total_pago:.2f}")
        
        btn_cobrar = st.button("🔥 Confirmar y Registrar Venta", use_container_width=True)

    if btn_cobrar:
        if stock_actual >= cantidad:
            st.session_state.inventario.loc[st.session_state.inventario["Producto"] == producto_sel, "Existencias"] -= cantidad
            
            nueva_venta = {
                "Fecha y Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Producto": producto_sel,
                "Cantidad": cantidad,
                "Precio Unitario (Q)": precio_actual,
                "Total Recaudado (Q)": total_pago
            }
            st.session_state.historial_ventas = pd.concat([st.session_state.historial_ventas, pd.DataFrame([nueva_venta])], ignore_index=True)
            
            st.success(f"✅ Venta registrada: {cantidad}x {producto_sel} por Q {total_pago:.2f}")
            st.rerun()
        else:
            st.error("❌ ¡Error! No tienes suficientes existencias en el inventario para completar esta venta.")

# ==========================================
# PESTAÑA 2: GESTIÓN DE INVENTARIO Y PRECIOS
# ==========================================
with tab2:
    st.subheader("📦 Panel de Control de Inventario")
    st.write("Puedes editar los precios o agregar stock directamente haciendo doble clic sobre las celdas de la tabla de abajo:")
    
    inventario_editado = st.data_editor(
        st.session_state.inventario,
        column_config={
            "Producto": st.column_config.TextColumn("Nombre del Producto", disabled=True),
            "Categoría": st.column_config.SelectboxColumn("Categoría", options=["Granizadas", "Frutas con Chocolate", "Bebidas Frías", "Snacks", "Bebidas"]),
            "Precio Venta (Q)": st.column_config.NumberColumn("Precio Público (Q)", min_value=0.0, format="Q %.2f"),
            "Existencias": st.column_config.NumberColumn("Unidades Disponibles", min_value=0, step=1)
        },
        use_container_width=True,
        num_rows="dynamic"
    )
    
    if st.button("💾 Guardar Cambios Manuales de Inventario/Precios"):
        st.session_state.inventario = inventario_editado
        st.success("✅ El inventario y la lista de precios han sido actualizados de forma segura.")
        st.rerun()

    if len(productos_alerta) > 0:
        st.warning("⚠️ **¡Productos próximos a agotarse! Necesitas reabastecer:**")
        st.dataframe(productos_alerta[["Producto", "Existencias"]], use_container_width=True, hide_index=True)

# ==========================================
# PESTAÑA 3: HISTORIAL Y REPORTES
# ==========================================
with tab3:
    st.subheader("📈 Auditoría e Historial General de Ventas")
    
    if st.session_state.historial_ventas.empty:
        st.info("Aún no se han registrado transacciones comerciales en este turno.")
    else:
        st.dataframe(st.session_state.historial_ventas.iloc[::-1], use_container_width=True, hide_index=True)
        
        csv_data = st.session_state.historial_ventas.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Reporte Financiero (CSV)",
            data=csv_data,
            file_name=f"reporte_ventas_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime="text/csv",
            use_container_width=True
        )
