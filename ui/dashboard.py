"""
📊 Trading Analyzer Pro - Dashboard Components
Componentes principales del dashboard
"""

import streamlit as st
from typing import Dict
from .styles import apply_custom_styles
from .metrics import create_advanced_metrics_section
from .charts import create_performance_charts
from ..config.settings import UI_KEYS

def create_comprehensive_dashboard(analysis: Dict):
    """🚀 Dashboard Comprehensivo centrado en PnL"""
    
    st.markdown('''
    <div class="main-header">
        <h1>💰 Trading Analyzer Pro - Dashboard PnL</h1>
        <p>Análisis inteligente de ganancias y rendimiento</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Métricas principales mejoradas
    if 'trading_performance' in analysis:
        create_advanced_metrics_section(analysis)
    
    # Alertas inteligentes destacadas
    if 'smart_alerts' in analysis:
        create_smart_alerts_section(analysis)
    else:
        st.markdown('''
        <div class="performance-excellent">
            <h4>✅ No hay alertas críticas - Todo funciona correctamente</h4>
        </div>
        ''', unsafe_allow_html=True)

def create_smart_alerts_section(analysis: Dict):
    """🚨 Sección de alertas inteligentes"""
    
    smart_alerts = analysis.get('smart_alerts', [])
    
    if smart_alerts:
        st.subheader("🚨 Alertas Inteligentes")
        
        for alert in smart_alerts:
            if "🚨" in alert:
                alert_class = "inactivity-alert"
            elif "⚠️" in alert:
                alert_class = "trading-insight"
            else:
                alert_class = "performance-excellent"
            
            st.markdown(f'''
            <div class="{alert_class}">
                <h4>{alert}</h4>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="performance-excellent">
            <h4>✅ No hay alertas - Sistema funcionando correctamente</h4>
        </div>
        ''', unsafe_allow_html=True)

def create_main_header():
    """🎨 Crear header principal de la aplicación"""
    
    apply_custom_styles()
    
    st.markdown('''
    <div class="main-header fade-in-up">
        <h1>💰 Trading Analyzer Pro</h1>
        <p>Análisis Avanzado de Trading con Inteligencia Artificial</p>
    </div>
    ''', unsafe_allow_html=True)

def create_welcome_screen():
    """🏠 Pantalla de bienvenida cuando no hay archivo cargado"""
    
    create_main_header()
    
    st.markdown("""
    ## 🎯 Características Principales
    
    ✅ **Análisis Multi-Cuenta**: Soporta múltiples cuentas y exchanges  
    ✅ **Win Rate Inteligente**: Cálculo automático de tasas de éxito  
    ✅ **Alertas IA**: Notificaciones inteligentes sobre tu rendimiento  
    ✅ **Visualizaciones Avanzadas**: Gráficos interactivos con Plotly  
    ✅ **Métricas de Riesgo**: Análisis de volatilidad y ratios  
    ✅ **Exportación de Reportes**: Descarga análisis completos  
    
    ### 📁 Formatos Soportados
    - **Excel**: .xlsx, .xls (con múltiples hojas)
    - **CSV**: Archivos separados por comas
    - **Exchanges**: BingX, Binance, y otros
    
    ### 🚀 ¡Comienza Ahora!
    Sube tu archivo en el panel lateral para comenzar el análisis.
    
    ---
    
    ### 🆚 **Versión Web vs Local**
    
    **Esta versión web SUPERA al analizador local con:**
    - 🧠 **Más inteligencia artificial**
    - 📊 **Visualizaciones interactivas**
    - 🔮 **Insights predictivos**
    - ⚡ **Análisis en tiempo real**
    - 🎯 **Recomendaciones accionables**
    
    ### 📁 Sube tu archivo para comenzar
    **Formatos soportados:** Excel (.xlsx, .xls), CSV  
    **Exchanges:** BingX, Binance, y otros  
    """)

def create_file_status_indicator(file_name: str):
    """📄 Indicador de estado del archivo actual"""
    
    st.success(f"📊 **Análisis activo**: {file_name}")
    st.markdown("---")

def create_section_selector():
    """🎛️ Selector de secciones de análisis"""
    
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