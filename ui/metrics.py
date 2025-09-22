"""
📈 Trading Analyzer Pro - Metrics Components
Componentes para mostrar métricas y KPIs
"""

import streamlit as st
import numpy as np
from typing import Dict
from .styles import get_status_color, format_currency, format_percentage, get_trend_icon, get_status_icon

def create_advanced_metrics_section(analysis: Dict):
    """📊 Sección de métricas avanzadas - CON VALORES ABSOLUTOS"""
    
    st.subheader("💰 Métricas de Rendimiento Detalladas")
    
    # Obtener datos financieros de cada cuenta
    financial_summary = analysis.get('financial_summary', {})
    performance = analysis.get('trading_performance', {})
    overall = performance.get('overall_metrics', {})
    
    # Calcular totales globales reales
    metrics = _calculate_global_metrics(financial_summary)
    
    # Primera fila - Métricas principales
    _create_main_metrics_row(metrics)
    
    # Segunda fila - Desglose detallado
    _create_detailed_breakdown_row(metrics)

def _calculate_global_metrics(financial_summary: Dict) -> Dict:
    """Calcular métricas globales a partir de los datos de las cuentas"""
    
    metrics = {
        'total_pnl': 0,
        'total_profit': 0,
        'total_loss': 0,
        'total_trades': 0,
        'win_rates': [],
        'account_count': len(financial_summary)
    }
    
    for account, data in financial_summary.items():
        metrics['total_pnl'] += data.get('pnl_total', 0)
        metrics['total_profit'] += data.get('total_profit', 0)
        metrics['total_loss'] += abs(data.get('total_loss', 0))  # Valor absoluto
        metrics['total_trades'] += data.get('total_trades', 0)
        
        win_rate = data.get('win_rate', 0)
        if win_rate > 0:
            metrics['win_rates'].append(win_rate)
    
    # Calcular métricas derivadas
    metrics['avg_win_rate'] = np.mean(metrics['win_rates']) if metrics['win_rates'] else 0
    metrics['profit_loss_ratio'] = (metrics['total_profit'] / metrics['total_loss']) if metrics['total_loss'] > 0 else float('inf')
    metrics['total_volume'] = metrics['total_profit'] + metrics['total_loss']
    metrics['profit_percentage'] = (metrics['total_profit'] / metrics['total_volume'] * 100) if metrics['total_volume'] > 0 else 0
    metrics['loss_percentage'] = (metrics['total_loss'] / metrics['total_volume'] * 100) if metrics['total_volume'] > 0 else 0
    
    return metrics

def _create_main_metrics_row(metrics: Dict):
    """Crear primera fila con métricas principales"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pnl_color = "performance-excellent" if metrics['total_pnl'] >= 0 else "inactivity-alert"
        pnl_icon = get_trend_icon(metrics['total_pnl'])
        pnl_status = 'GANANCIA' if metrics['total_pnl'] >= 0 else 'PÉRDIDA'
        
        st.markdown(f'''
        <div class="{pnl_color}">
            <h3>💰 PnL Total</h3>
            <h1>${metrics['total_pnl']:,.2f}</h1>
            <p>{pnl_icon} {pnl_status}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        wr_color = get_status_color(metrics['avg_win_rate'], {"excellent": 60, "good": 40, "poor": 30})
        wr_status = '🏆 Excelente' if metrics['avg_win_rate'] > 60 else '⚖️ Balanceado' if metrics['avg_win_rate'] > 40 else '⚠️ Mejorable'
        
        st.markdown(f'''
        <div class="{wr_color}">
            <h3>🎯 Win Rate Promedio</h3>
            <h1>{metrics['avg_win_rate']:.1f}%</h1>
            <p>{wr_status}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="trading-insight">
            <h3>🔄 Total Operaciones</h3>
            <h1>{metrics['total_trades']:,}</h1>
            <p>Trades ejecutados</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        ratio_color = "performance-excellent" if metrics['profit_loss_ratio'] > 1 else "inactivity-alert"
        ratio_status = '✅ Positivo' if metrics['profit_loss_ratio'] > 1 else '⚠️ Negativo'
        ratio_display = f"{metrics['profit_loss_ratio']:.2f}" if metrics['profit_loss_ratio'] != float('inf') else "∞"
        
        st.markdown(f'''
        <div class="{ratio_color}">
            <h3>📊 Ratio P/L</h3>
            <h1>{ratio_display}</h1>
            <p>{ratio_status}</p>
        </div>
        ''', unsafe_allow_html=True)

def _create_detailed_breakdown_row(metrics: Dict):
    """Crear segunda fila con desglose detallado"""
    
    st.subheader("📈 Desglose Detallado de Ganancias y Pérdidas")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.markdown(f'''
        <div class="performance-excellent">
            <h4>💚 Total Ganancias</h4>
            <h2>${metrics['total_profit']:,.2f}</h2>
            <p>Dinero ganado</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col6:
        st.markdown(f'''
        <div class="inactivity-alert">
            <h4>💔 Total Pérdidas</h4>
            <h2>-${metrics['total_loss']:,.2f}</h2>
            <p>Dinero perdido</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col7:
        st.markdown(f'''
        <div class="trading-insight">
            <h4>📊 % Ganancias</h4>
            <h2>{metrics['profit_percentage']:.1f}%</h2>
            <p>Del total movido</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col8:
        st.markdown(f'''
        <div class="trading-insight">
            <h4>📊 % Pérdidas</h4>
            <h2>{metrics['loss_percentage']:.1f}%</h2>
            <p>Del total movido</p>
        </div>
        ''', unsafe_allow_html=True)

def create_account_summary_metrics(analysis: Dict):
    """📋 Métricas resumen por cuenta"""
    
    financial_summary = analysis.get('financial_summary', {})
    
    if not financial_summary:
        st.warning("📊 No hay datos de cuentas disponibles")
        return
    
    st.subheader("🏦 Resumen por Cuenta")
    
    # Crear tabla de resumen
    summary_data = []
    for account, data in financial_summary.items():
        pnl = data.get('pnl_total', 0)
        win_rate = data.get('win_rate', 0)
        total_trades = data.get('total_trades', 0)
        profit_factor = data.get('profit_factor', 0)
        
        status_icon = get_status_icon(pnl)
        status_text = 'Ganancia' if pnl > 0 else 'Pérdida' if pnl < 0 else 'Neutral'
        
        summary_data.append({
            'Cuenta': account,
            'Estado': f"{status_icon} {status_text}",
            'PnL': format_currency(pnl),
            'Win Rate': format_percentage(win_rate),
            'Trades': f"{total_trades:,}",
            'Profit Factor': f"{profit_factor:.2f}"
        })
    
    # Ordenar por PnL descendente
    summary_data.sort(key=lambda x: float(x['PnL'].replace('$', '').replace(',', '').replace(' USDT', '')), reverse=True)
    
    # Mostrar como tabla
    import pandas as pd
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

def create_performance_indicators(analysis: Dict):
    """📊 Indicadores de rendimiento visual"""
    
    performance = analysis.get('trading_performance', {})
    overall = performance.get('overall_metrics', {})
    
    if not overall:
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        profitable_accounts = overall.get('profitable_accounts', 0)
        total_accounts = overall.get('total_accounts', 1)
        success_rate = (profitable_accounts / total_accounts * 100) if total_accounts > 0 else 0
        
        success_color = "performance-excellent" if success_rate > 50 else "trading-insight" if success_rate > 25 else "inactivity-alert"
        
        st.markdown(f'''
        <div class="{success_color}">
            <h4>📈 Cuentas Rentables</h4>
            <h2>{profitable_accounts}/{total_accounts}</h2>
            <p>{success_rate:.1f}% exitosas</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        best_account = overall.get('best_performing_account', 'N/A')
        
        st.markdown(f'''
        <div class="performance-excellent">
            <h4>🏆 Mejor Cuenta</h4>
            <h2>{best_account}</h2>
            <p>Mayor rendimiento</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        global_win_rate = overall.get('global_win_rate', 0)
        wr_color = get_status_color(global_win_rate)
        
        st.markdown(f'''
        <div class="{wr_color}">
            <h4>🎯 Win Rate Global</h4>
            <h2>{global_win_rate:.1f}%</h2>
            <p>Promedio ponderado</p>
        </div>
        ''', unsafe_allow_html=True)