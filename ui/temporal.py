"""
📅 Trading Analyzer Pro - Temporal Analysis UI
Componentes para análisis temporal y patrones de tiempo
"""

import streamlit as st
from typing import Dict

def create_temporal_analysis_section(analysis: Dict):
    """🕐 Sección de análisis temporal centrado en rendimiento"""
    
    st.subheader("📅 Rendimiento por Tiempo")
    
    temporal = analysis.get('temporal_analysis', {})
    global_patterns = temporal.get('global_activity_patterns', {})
    performance = analysis.get('trading_performance', {})
    account_comparison = performance.get('account_comparison', {})
    
    if global_patterns:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            most_active_day = global_patterns.get('most_active_day', 'N/A')
            st.markdown(f'''
            <div class="trading-insight">
                <h4>📅 Día Más Activo</h4>
                <h3>{most_active_day}</h3>
                <p>Mayor volumen de trading</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            peak_hour = global_patterns.get('peak_hour', 'N/A')
            st.markdown(f'''
            <div class="trading-insight">
                <h4>🕐 Hora Pico</h4>
                <h3>{peak_hour}:00</h3>
                <p>Mayor actividad horaria</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            total_period = global_patterns.get('total_period_days', 0)
            st.markdown(f'''
            <div class="trading-insight">
                <h4>📊 Período Analizado</h4>
                <h3>{total_period} días</h3>
                <p>Duración del análisis</p>
            </div>
            ''', unsafe_allow_html=True)
    
    # Insights de rendimiento temporal
    if account_comparison:
        st.markdown("### 📈 Patrones de Rendimiento")
        
        best_performer = max(account_comparison.items(), key=lambda x: x[1].get('pnl', 0))
        worst_performer = min(account_comparison.items(), key=lambda x: x[1].get('pnl', 0))
        
        st.markdown(f'''
        <div class="performance-excellent">
            <h4>🏆 Mejor Rendimiento: {best_performer[0]}</h4>
            <p>PnL: ${best_performer[1].get('pnl', 0):,.2f} | Win Rate: {best_performer[1].get('win_rate', 0):.1f}%</p>
        </div>
        ''', unsafe_allow_html=True)
        
        if worst_performer[1].get('pnl', 0) < 0:
            st.markdown(f'''
            <div class="inactivity-alert">
                <h4>⚠️ Menor Rendimiento: {worst_performer[0]}</h4>
                <p>PnL: ${worst_performer[1].get('pnl', 0):,.2f} | Win Rate: {worst_performer[1].get('win_rate', 0):.1f}%</p>
            </div>
            ''', unsafe_allow_html=True)