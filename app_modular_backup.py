"""
🚀 Trading Analyzer Pro - Main Application
Aplicación principal simplificada y modular
"""

import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import with fallbacks for different environments
try:
    from config.settings import PAGE_CONFIG
except ImportError:
    PAGE_CONFIG = {
        "page_title": "Trading Analyzer Pro",
        "page_icon": "💰", 
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }

try:
    from core.analyzer import AdvancedTradingAnalyzer
    from ui.styles import apply_custom_styles
    from ui.sidebar import (
        create_sidebar_header, create_file_uploader, create_analyze_button,
        create_file_info, create_analysis_sections_selector, create_export_section,
        create_reset_section, show_analysis_summary, create_sidebar_footer
    )
    from ui.dashboard import create_comprehensive_dashboard, create_welcome_screen, create_file_status_indicator
    from ui.performance import create_performance_analysis_section, create_account_pnl_comparison, create_pnl_insights_section
    from ui.temporal import create_temporal_analysis_section
    from ui.risk import create_advanced_risk_analysis
except ImportError as e:
    st.error(f"🔧 Import Error: {e}")
    st.error("💡 The app is loading in emergency mode...")
    
    # Emergency fallback - create minimal functions
    def apply_custom_styles(): pass
    def create_sidebar_header(): st.sidebar.markdown("## 🧠 Trading Analyzer")
    def create_file_uploader(): return st.sidebar.file_uploader("Upload file", type=['xlsx', 'csv'])
    def create_analyze_button(enabled): return st.sidebar.button("Analyze", disabled=not enabled)
    def create_file_info(file): st.sidebar.info(f"File: {file.name}")
    def create_analysis_sections_selector(): return {"dashboard": True}
    def create_export_section(analysis): pass
    def create_reset_section(): pass
    def show_analysis_summary(analysis): pass
    def create_sidebar_footer(): pass
    def create_comprehensive_dashboard(analysis): st.write("Dashboard loading...")
    def create_welcome_screen(): st.write("Welcome! Upload a file to begin.")
    def create_file_status_indicator(name): st.info(f"Analyzing: {name}")
    def create_performance_analysis_section(analysis): pass
    def create_account_pnl_comparison(analysis): pass
    def create_pnl_insights_section(analysis): pass
    def create_temporal_analysis_section(analysis): pass
    def create_advanced_risk_analysis(analysis): pass
    
    # Minimal analyzer class
    class AdvancedTradingAnalyzer:
        def load_data_from_upload(self, file): return False
        def generate_comprehensive_analysis(self): return {}

# 🎨 Configuración de la página
st.set_page_config(**PAGE_CONFIG)

def main():
    """🚀 Función principal de la aplicación - VERSIÓN MODULAR"""
    
    # Aplicar estilos personalizados
    apply_custom_styles()
    
    # Crear sidebar
    create_sidebar_header()
    
    # Inicializar analizador
    analyzer = AdvancedTradingAnalyzer()
    
    # Sección de carga de archivos
    uploaded_file = create_file_uploader()
    analyze_button = create_analyze_button(uploaded_file is not None)
    
    # Mostrar información del archivo
    if uploaded_file:
        create_file_info(uploaded_file)
    
    # Procesar archivo
    should_analyze = False
    
    if uploaded_file is not None:
        # Verificar si es un archivo nuevo
        file_key = f"{uploaded_file.name}_{uploaded_file.size}"
        
        # Analizar automáticamente si es nuevo archivo
        if ('current_file' not in st.session_state or 
            st.session_state['current_file'] != file_key):
            should_analyze = True
        
        # O si se presiona el botón manualmente
        if analyze_button:
            should_analyze = True
    
    # Procesar el archivo si se debe analizar
    if should_analyze and uploaded_file is not None:
        # Cargar y analizar datos
        with st.spinner("🧠 Analizando con IA avanzada..."):
            if analyzer.load_data_from_upload(uploaded_file):
                # Generar análisis comprehensivo
                analysis = analyzer.generate_comprehensive_analysis()
                
                # Guardar en session state
                st.session_state['analysis'] = analysis
                st.session_state['analyzer'] = analyzer
                st.session_state['current_file'] = f"{uploaded_file.name}_{uploaded_file.size}"
                
                # Mensaje de éxito
                st.success("✅ ¡Análisis completado! Revisa los resultados abajo.")
                
                # Forzar refresco para mostrar resultados inmediatamente
                st.rerun()
            else:
                st.error("❌ Error procesando el archivo. Verifica el formato.")
    
    elif uploaded_file is not None and 'analysis' in st.session_state:
        # Archivo ya procesado
        st.sidebar.info("✅ Archivo ya analizado")
    
    # Mostrar análisis si existe
    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        
        # Mostrar mensaje de archivo analizado
        current_file = st.session_state.get('current_file', 'archivo_desconocido')
        file_name = current_file.split('_')[0] if '_' in current_file else current_file
        
        create_file_status_indicator(file_name)
        
        # Mostrar resumen en sidebar
        show_analysis_summary(analysis)
        
        # Selector de secciones
        sections = create_analysis_sections_selector()
        
        # Renderizar secciones seleccionadas
        if sections['dashboard']:
            create_comprehensive_dashboard(analysis)
            st.markdown("---")
        
        if sections['performance']:
            create_performance_analysis_section(analysis)
            st.markdown("---")
        
        if sections['accounts']:
            create_account_pnl_comparison(analysis)
            st.markdown("---")
        
        if sections['temporal']:
            create_temporal_analysis_section(analysis)
            st.markdown("---")
        
        if sections['risk']:
            create_advanced_risk_analysis(analysis)
            st.markdown("---")
        
        # Siempre mostrar insights predictivos (centrados en PnL)
        create_pnl_insights_section(analysis)
        
        # Sección de exportación
        create_export_section(analysis)
        
        # Botón de reset
        create_reset_section()
    
    else:
        # Pantalla de bienvenida
        create_welcome_screen()
    
    # Footer del sidebar
    create_sidebar_footer()

if __name__ == "__main__":
    main()