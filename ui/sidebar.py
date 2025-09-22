"""
🎛️ Trading Analyzer Pro - Sidebar Components
Componentes del panel lateral de control
"""

import streamlit as st
from datetime import datetime
from typing import Optional
from ..config.settings import SUPPORTED_FILE_TYPES, UI_KEYS

def create_sidebar_header():
    """🎨 Header del sidebar"""
    st.sidebar.markdown("## 🧠 Control Panel IA")
    st.sidebar.markdown("---")

def create_file_uploader():
    """📁 Componente de carga de archivos"""
    st.sidebar.markdown("### 📁 Cargar Archivo de Trading")
    
    uploaded_file = st.sidebar.file_uploader(
        "Arrastra tu archivo Excel o CSV",
        type=SUPPORTED_FILE_TYPES,
        help="Soporta archivos de BingX, Binance, y otros exchanges",
        key=UI_KEYS["file_uploader"]
    )
    
    return uploaded_file

def create_analyze_button(file_uploaded: bool = False):
    """🚀 Botón de análisis"""
    return st.sidebar.button(
        "🚀 Analizar Archivo", 
        type="primary", 
        disabled=not file_uploaded,
        key=UI_KEYS["analyze_button"]
    )

def create_file_info(uploaded_file):
    """📊 Información del archivo cargado"""
    if uploaded_file:
        st.sidebar.success(f"📄 **{uploaded_file.name}**")
        st.sidebar.info(f"📏 Tamaño: {uploaded_file.size / 1024:.1f} KB")

def create_analysis_sections_selector():
    """📊 Selector de secciones de análisis"""
    st.sidebar.markdown("### 📊 Análisis de Rendimiento")
    
    sections = {
        'dashboard': st.sidebar.checkbox(
            "💰 Dashboard Principal (PnL)", 
            value=True, 
            key=UI_KEYS["checkboxes"]["dashboard"]
        ),
        'performance': st.sidebar.checkbox(
            "📈 Análisis de Ganancias", 
            value=True, 
            key=UI_KEYS["checkboxes"]["performance"]
        ),
        'accounts': st.sidebar.checkbox(
            "🏦 Comparación de Cuentas", 
            value=True, 
            key=UI_KEYS["checkboxes"]["accounts"]
        ),
        'temporal': st.sidebar.checkbox(
            "📅 Rendimiento por Tiempo", 
            value=False, 
            key=UI_KEYS["checkboxes"]["temporal"]
        ),
        'risk': st.sidebar.checkbox(
            "⚠️ Análisis de Riesgo", 
            value=False, 
            key=UI_KEYS["checkboxes"]["risk"]
        )
    }
    
    return sections

def create_export_section(analysis: dict):
    """📄 Sección de exportación"""
    st.sidebar.markdown("### 📄 Exportar Análisis")
    
    if st.sidebar.button("📥 Generar Reporte IA", key=UI_KEYS["buttons"]["export"]):
        from ..utils.report_generator import create_comprehensive_report
        
        report_content = create_comprehensive_report(analysis)
        st.sidebar.download_button(
            label="💾 Descargar Reporte Completo",
            data=report_content,
            file_name=f"trading_ai_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key=UI_KEYS["buttons"]["download"]
        )

def create_reset_section():
    """🔄 Sección de reset"""
    st.sidebar.markdown("### 🔄 Nuevo Análisis")
    
    if st.sidebar.button("🗑️ Limpiar y Empezar de Nuevo", type="secondary", key=UI_KEYS["buttons"]["clear"]):
        # Limpiar session state
        keys_to_clear = ['analysis', 'analyzer', 'current_file']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def create_status_indicator(status: str, message: str):
    """📊 Indicador de estado"""
    if status == "success":
        st.sidebar.success(message)
    elif status == "info":
        st.sidebar.info(message)
    elif status == "warning":
        st.sidebar.warning(message)
    elif status == "error":
        st.sidebar.error(message)

def create_analysis_progress(current_step: str, total_steps: int, current_step_num: int):
    """📈 Indicador de progreso del análisis"""
    progress_percent = current_step_num / total_steps
    
    st.sidebar.markdown("### 🔄 Progreso del Análisis")
    st.sidebar.progress(progress_percent)
    st.sidebar.write(f"**Paso {current_step_num}/{total_steps}**: {current_step}")

def show_analysis_summary(analysis: dict):
    """📋 Resumen del análisis en sidebar"""
    if not analysis:
        return
    
    st.sidebar.markdown("### 📊 Resumen del Análisis")
    
    # Métricas básicas
    trading_performance = analysis.get('trading_performance', {})
    overall = trading_performance.get('overall_metrics', {})
    
    total_pnl = overall.get('total_pnl_all_accounts', 0)
    total_accounts = overall.get('total_accounts', 0)
    global_win_rate = overall.get('global_win_rate', 0)
    
    # Mostrar métricas compactas
    if total_pnl >= 0:
        st.sidebar.success(f"💰 PnL: +${total_pnl:,.2f}")
    else:
        st.sidebar.error(f"💰 PnL: ${total_pnl:,.2f}")
    
    st.sidebar.info(f"🏦 Cuentas: {total_accounts}")
    st.sidebar.info(f"🎯 Win Rate: {global_win_rate:.1f}%")
    
    # Alertas si las hay
    alerts = analysis.get('smart_alerts', [])
    if alerts:
        alert_count = len(alerts)
        critical_alerts = len([a for a in alerts if "🚨" in a])
        
        if critical_alerts > 0:
            st.sidebar.warning(f"⚠️ {critical_alerts} alertas críticas")
        else:
            st.sidebar.info(f"📢 {alert_count} alertas")

def create_sidebar_footer():
    """👥 Footer del sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
            <p>💰 <strong>Trading Analyzer Pro</strong></p>
            <p>Powered by AI & Data Science</p>
        </div>
        """, 
        unsafe_allow_html=True
    )