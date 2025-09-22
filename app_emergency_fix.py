"""
🔧 Trading Analyzer Pro - Emergency Fix
Corrección crítica para elementos duplicados de Streamlit
"""

# Este archivo fuerza la actualización del app.py en el servidor
# para resolver el error StreamlitDuplicateElementId

import streamlit as st

# Mensaje de debug para confirmar que la nueva versión se está ejecutando
st.markdown("🔧 **VERSION MODULAR ACTIVA** - Elementos únicos implementados")

# Importar y ejecutar la versión modular principal
from config.settings import PAGE_CONFIG
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

# Configuración de página con ID único
st.set_page_config(
    page_title="Trading Analyzer Pro - Modular",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """🚀 Función principal - VERSIÓN MODULAR CORREGIDA"""
    
    # Aplicar estilos personalizados
    apply_custom_styles()
    
    # Mensaje de debug temporal
    st.info("🔧 **Versión Modular Activa** - Problema de elementos duplicados resuelto")
    
    # Crear sidebar
    create_sidebar_header()
    
    # Inicializar analizador
    analyzer = AdvancedTradingAnalyzer()
    
    # Sección de carga de archivos con claves únicas
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
        
        # Selector de secciones con claves únicas
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