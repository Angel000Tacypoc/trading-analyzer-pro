"""
📈 Trading Analyzer Pro - Performance Analysis UI
Componentes para análisis de rendimiento y PnL
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict
from .styles import get_status_color, format_currency, format_percentage, get_trend_icon, get_status_icon

def create_performance_analysis_section(analysis: Dict):
    """💰 Análisis de rendimiento y PnL"""
    
    st.subheader("💰 Análisis de Ganancias y Pérdidas")
    
    performance = analysis.get('trading_performance', {})
    overall = performance.get('overall_metrics', {})
    account_comparison = performance.get('account_comparison', {})
    
    if not account_comparison:
        st.warning("📊 No hay datos de rendimiento disponibles")
        return
    
    # Métricas globales de PnL
    col1, col2, col3 = st.columns(3)
    
    total_pnl = overall.get('total_pnl_all_accounts', 0)
    positive_accounts = len([acc for acc, data in account_comparison.items() if data.get('pnl', 0) > 0])
    total_accounts = len(account_comparison)
    
    with col1:
        st.markdown(f'''
        <div class="{'performance-excellent' if total_pnl > 0 else 'inactivity-alert'}">
            <h3>💰 PnL Total</h3>
            <h1>${total_pnl:,.2f}</h1>
            <p>{'🟢 GANANCIA' if total_pnl > 0 else '🔴 PÉRDIDA'}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        success_rate = (positive_accounts / total_accounts * 100) if total_accounts > 0 else 0
        st.markdown(f'''
        <div class="{'performance-excellent' if success_rate > 50 else 'trading-insight'}">
            <h3>📈 Cuentas Rentables</h3>
            <h1>{positive_accounts}/{total_accounts}</h1>
            <p>{success_rate:.1f}% exitosas</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        global_win_rate = overall.get('global_win_rate', 0)
        st.markdown(f'''
        <div class="{get_status_color(global_win_rate, {'excellent': 60, 'good': 40, 'poor': 30})}">
            <h3>🎯 Win Rate Global</h3>
            <h1>{global_win_rate:.1f}%</h1>
            <p>{'🏆 Excelente' if global_win_rate > 60 else '⚖️ Balanceado' if global_win_rate > 40 else '⚠️ Mejorable'}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Gráfico de distribución de PnL
    _create_pnl_distribution_chart(account_comparison)
    
    # Análisis de rentabilidad por cuenta
    _create_account_profitability_analysis(account_comparison)

def _create_pnl_distribution_chart(account_comparison: Dict):
    """📊 Gráfico de distribución de PnL"""
    
    st.subheader("📊 Distribución de Ganancias por Cuenta")
    
    accounts = list(account_comparison.keys())
    pnl_values = [account_comparison[acc]['pnl'] for acc in accounts]
    
    # Crear gráfico único sin duplicados
    fig_pnl_dist = go.Figure()
    
    colors = ['#00d2d3' if pnl > 0 else '#ff6b6b' for pnl in pnl_values]
    
    fig_pnl_dist.add_trace(go.Bar(
        x=accounts,
        y=pnl_values,
        marker_color=colors,
        text=[f'${pnl:,.0f}' for pnl in pnl_values],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>PnL: $%{y:,.2f}<extra></extra>',
        name='PnL por Cuenta'
    ))
    
    fig_pnl_dist.update_layout(
        title="💰 PnL por Cuenta - Vista General",
        xaxis_title="Cuenta",
        yaxis_title="PnL (USDT)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        showlegend=False,
        height=400
    )
    
    fig_pnl_dist.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, annotation_text="Break Even")
    
    st.plotly_chart(fig_pnl_dist, use_container_width=True, key="pnl_distribution_performance")

def _create_account_profitability_analysis(account_comparison: Dict):
    """📈 Análisis detallado de rentabilidad"""
    
    st.subheader("📈 Detalles de Rentabilidad")
    
    for account, data in account_comparison.items():
        pnl = data.get('pnl', 0)
        win_rate = data.get('win_rate', 0)
        total_trades = data.get('total_trades', 0)
        profit_factor = data.get('profit_factor', 0)
        
        status_class = "performance-excellent" if pnl > 0 else "inactivity-alert"
        status_icon = get_status_icon(pnl)
        
        st.markdown(f'''
        <div class="{status_class}">
            <h4>{status_icon} {account}</h4>
            <div style="display: flex; justify-content: space-between;">
                <div><strong>PnL:</strong> ${pnl:,.2f}</div>
                <div><strong>Win Rate:</strong> {win_rate:.1f}%</div>
                <div><strong>Trades:</strong> {total_trades:,}</div>
                <div><strong>Profit Factor:</strong> {profit_factor:.2f}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def create_account_pnl_comparison(analysis: Dict):
    """🏦 Comparación detallada de PnL entre cuentas"""
    
    st.subheader("🏦 Comparación Detallada de Cuentas")
    
    performance = analysis.get('trading_performance', {})
    account_comparison = performance.get('account_comparison', {})
    
    if not account_comparison:
        st.warning("📊 No hay datos de cuentas para comparar")
        return
    
    # Crear tabs para diferentes vistas
    tab1, tab2, tab3 = st.tabs(["💰 PnL", "🎯 Win Rate", "📊 Métricas Completas"])
    
    accounts = list(account_comparison.keys())
    
    with tab1:
        _create_pnl_comparison_tab(account_comparison)
    
    with tab2:
        _create_win_rate_comparison_tab(account_comparison, accounts)
    
    with tab3:
        _create_complete_metrics_tab(account_comparison)

def _create_pnl_comparison_tab(account_comparison: Dict):
    """💰 Tab de comparación de PnL"""
    
    st.markdown("### 💰 Análisis de PnL")
    
    pnl_data = []
    for account, data in account_comparison.items():
        pnl = data.get('pnl', 0)
        pnl_data.append({
            'Cuenta': account,
            'PnL (USDT)': f"${pnl:,.2f}",
            'Estado': f"{get_status_icon(pnl)} {'Ganancia' if pnl > 0 else 'Pérdida'}",
            'Rendimiento': f"{((pnl / abs(pnl)) * 100) if pnl != 0 else 0:.1f}%"
        })
    
    # Ordenar por PnL descendente
    pnl_data.sort(key=lambda x: float(x['PnL (USDT)'].replace('$', '').replace(',', '')), reverse=True)
    
    df_pnl = pd.DataFrame(pnl_data)
    st.dataframe(df_pnl, use_container_width=True, hide_index=True)

def _create_win_rate_comparison_tab(account_comparison: Dict, accounts: list):
    """🎯 Tab de comparación de Win Rate"""
    
    st.markdown("### 🎯 Análisis de Win Rate")
    
    col1, col2 = st.columns(2)
    
    win_rates = [account_comparison[acc]['win_rate'] for acc in accounts]
    
    with col1:
        # Gráfico de barras Win Rate
        fig_wr = go.Figure()
        
        colors_wr = ['#00d2d3' if wr > 50 else '#feca57' if wr > 40 else '#ff6b6b' for wr in win_rates]
        
        fig_wr.add_trace(go.Bar(
            x=accounts,
            y=win_rates,
            marker_color=colors_wr,
            text=[f'{wr:.1f}%' for wr in win_rates],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>'
        ))
        
        fig_wr.update_layout(
            title="🎯 Win Rate por Cuenta",
            xaxis_title="Cuenta",
            yaxis_title="Win Rate (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=400
        )
        
        fig_wr.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5, annotation_text="Break Even")
        
        st.plotly_chart(fig_wr, use_container_width=True, key="win_rate_comparison_performance")
    
    with col2:
        # Tabla de Win Rate
        wr_data = []
        for account, data in account_comparison.items():
            win_rate = data.get('win_rate', 0)
            total_trades = data.get('total_trades', 0)
            wr_data.append({
                'Cuenta': account,
                'Win Rate': f"{win_rate:.1f}%",
                'Total Trades': f"{total_trades:,}",
                'Calificación': '🏆 Excelente' if win_rate > 70 else '✅ Bueno' if win_rate > 50 else '⚠️ Mejorable'
            })
        
        # Ordenar por Win Rate descendente
        wr_data.sort(key=lambda x: float(x['Win Rate'].replace('%', '')), reverse=True)
        
        df_wr = pd.DataFrame(wr_data)
        st.dataframe(df_wr, use_container_width=True, hide_index=True)

def _create_complete_metrics_tab(account_comparison: Dict):
    """📊 Tab de métricas completas"""
    
    st.markdown("### 📊 Métricas Completas")
    
    complete_data = []
    for account, data in account_comparison.items():
        complete_data.append({
            'Cuenta': account,
            'PnL': f"${data.get('pnl', 0):,.2f}",
            'Win Rate': f"{data.get('win_rate', 0):.1f}%",
            'Total Trades': f"{data.get('total_trades', 0):,}",
            'Profit Factor': f"{data.get('profit_factor', 0):.2f}",
            'Max Drawdown': f"${data.get('max_drawdown', 0):,.2f}",
            'Expectancy': f"{data.get('expectancy', 0):.2f}"
        })
    
    df_complete = pd.DataFrame(complete_data)
    st.dataframe(df_complete, use_container_width=True, hide_index=True)

def create_pnl_insights_section(analysis: Dict):
    """🔮 Insights centrados en PnL"""
    
    st.subheader("🔮 Insights de Rendimiento")
    
    performance = analysis.get('trading_performance', {})
    account_comparison = performance.get('account_comparison', {})
    predictive = analysis.get('predictive_insights', {})
    
    if not account_comparison:
        return
    
    # Análisis automático de rendimiento
    total_pnl = sum(data.get('pnl', 0) for data in account_comparison.values())
    profitable_accounts = [acc for acc, data in account_comparison.items() if data.get('pnl', 0) > 0]
    loss_accounts = [acc for acc, data in account_comparison.items() if data.get('pnl', 0) < 0]
    
    # Insights automáticos
    if total_pnl > 1000:
        st.markdown('''
        <div class="performance-excellent">
            <h4>🎉 ¡RENDIMIENTO EXCEPCIONAL!</h4>
            <p>Tu cartera está generando ganancias significativas. ¡Excelente trabajo!</p>
        </div>
        ''', unsafe_allow_html=True)
    elif total_pnl > 0:
        st.markdown('''
        <div class="trading-insight">
            <h4>📈 Rendimiento Positivo</h4>
            <p>Tu cartera está en verde. Mantén la estrategia actual.</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="inactivity-alert">
            <h4>⚠️ Rendimiento Negativo</h4>
            <p>Considera revisar tu estrategia de trading. Hay oportunidades de mejora.</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Recomendaciones específicas
    if profitable_accounts:
        best_account = max(profitable_accounts, key=lambda x: account_comparison[x]['pnl'])
        st.markdown(f'''
        <div class="performance-excellent">
            <h4>✅ Cuentas Rentables: {len(profitable_accounts)}</h4>
            <p><strong>Mejor cuenta:</strong> {best_account}</p>
            <p><strong>Recomendación:</strong> Analiza qué hace exitosa esta cuenta y replica en otras.</p>
        </div>
        ''', unsafe_allow_html=True)
    
    if loss_accounts:
        worst_account = min(loss_accounts, key=lambda x: account_comparison[x]['pnl'])
        worst_loss = account_comparison[worst_account]['pnl']
        st.markdown(f'''
        <div class="inactivity-alert">
            <h4>⚠️ Cuentas con Pérdidas: {len(loss_accounts)}</h4>
            <p><strong>Mayor pérdida:</strong> {worst_account} (${worst_loss:,.2f})</p>
            <p><strong>Recomendación:</strong> Revisa la estrategia de esta cuenta o considera pausar el trading.</p>
        </div>
        ''', unsafe_allow_html=True)