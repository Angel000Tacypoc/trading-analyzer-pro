import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
import io
import base64
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="🚀 Trading Analyzer Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para un diseño profesional
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        font-weight: bold;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .success-metric {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    }
    
    .warning-metric {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .info-metric {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #FF6B6B;
    }
    
    .upload-section {
        border: 2px dashed #4ECDC4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class TradingAnalyzerWeb:
    """🚀 Analizador de Trading Web Avanzado con IA"""
    
    def __init__(self):
        self.data = None
        self.sheets = {}
        self.analysis_results = {}
        
    def load_data_from_upload(self, uploaded_file) -> bool:
        """Cargar datos desde archivo subido"""
        try:
            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                # Leer Excel con múltiples hojas
                excel_sheets = pd.read_excel(uploaded_file, sheet_name=None)
                self.sheets = excel_sheets
                return True
            elif uploaded_file.name.endswith('.csv'):
                # Leer CSV
                csv_data = pd.read_csv(uploaded_file)
                self.sheets = {'main': csv_data}
                return True
            else:
                st.error("❌ Formato de archivo no soportado")
                return False
        except Exception as e:
            st.error(f"❌ Error cargando archivo: {str(e)}")
            return False
    
    def generate_comprehensive_analysis(self) -> Dict:
        """🧠 Análisis comprehensivo con IA"""
        if not self.sheets:
            return {}
        
        analysis = {
            'financial_summary': {},
            'performance_metrics': {},
            'trading_analysis': {},
            'risk_analysis': {},
            'temporal_analysis': {},
            'alerts': []
        }
        
        total_pnl = 0
        total_trades = 0
        all_dates = []
        
        for sheet_name, sheet_data in self.sheets.items():
            if sheet_data is None or sheet_data.empty:
                continue
            
            sheet_analysis = self._analyze_sheet(sheet_data, sheet_name)
            analysis['financial_summary'][sheet_name] = sheet_analysis
            
            # Acumular métricas globales
            if 'pnl_total' in sheet_analysis:
                total_pnl += sheet_analysis['pnl_total']
            if 'total_trades' in sheet_analysis:
                total_trades += sheet_analysis['total_trades']
            if 'dates' in sheet_analysis:
                all_dates.extend(sheet_analysis['dates'])
        
        # Métricas globales
        analysis['performance_metrics'] = {
            'total_pnl': total_pnl,
            'total_trades': total_trades,
            'total_accounts': len([s for s in self.sheets.values() if not s.empty]),
            'date_range': self._get_date_range(all_dates) if all_dates else None
        }
        
        # Generar alertas inteligentes
        analysis['alerts'] = self._generate_smart_alerts(analysis)
        
        return analysis
    
    def _analyze_sheet(self, data: pd.DataFrame, sheet_name: str) -> Dict:
        """Análisis detallado de una hoja/cuenta"""
        analysis = {'sheet_name': sheet_name}
        
        # Análisis temporal
        date_cols = [col for col in data.columns if any(word in col.lower() for word in ['time', 'date', 'utc'])]
        if date_cols:
            try:
                dates = pd.to_datetime(data[date_cols[0]])
                analysis['dates'] = dates.tolist()
                analysis['period_days'] = (dates.max() - dates.min()).days
                analysis['first_transaction'] = dates.min()
                analysis['last_transaction'] = dates.max()
                
                # Actividad por mes
                monthly_activity = dates.dt.to_period('M').value_counts().sort_index()
                analysis['monthly_activity'] = monthly_activity.to_dict()
            except:
                pass
        
        # Análisis financiero
        amount_cols = [col for col in data.columns if any(word in col.lower() for word in ['amount', 'pnl', 'balance'])]
        for col in amount_cols:
            if data[col].dtype in ['float64', 'int64']:
                analysis[f'{col}_total'] = float(data[col].sum())
                analysis[f'{col}_mean'] = float(data[col].mean())
                analysis[f'{col}_std'] = float(data[col].std())
                
                if 'amount' in col.lower() and 'pnl' in col.lower():
                    analysis['pnl_total'] = float(data[col].sum())
        
        # Análisis de tipos de transacción
        type_cols = [col for col in data.columns if 'type' in col.lower()]
        if type_cols:
            types = data[type_cols[0]].value_counts()
            analysis['transaction_types'] = types.to_dict()
            
            # Detectar trading
            trading_keywords = ['realized', 'pnl', 'fee', 'trade']
            trading_transactions = data[data[type_cols[0]].str.contains('|'.join(trading_keywords), case=False, na=False)]
            if not trading_transactions.empty:
                analysis['total_trades'] = len(trading_transactions)
                
                # Win rate calculation
                if amount_cols:
                    pnl_values = trading_transactions[amount_cols[0]]
                    wins = (pnl_values > 0).sum()
                    losses = (pnl_values < 0).sum()
                    total = len(pnl_values)
                    
                    if total > 0:
                        analysis['win_rate'] = (wins / total) * 100
                        analysis['wins'] = wins
                        analysis['losses'] = losses
                        analysis['avg_win'] = float(pnl_values[pnl_values > 0].mean()) if wins > 0 else 0
                        analysis['avg_loss'] = float(pnl_values[pnl_values < 0].mean()) if losses > 0 else 0
        
        # Análisis de activos
        asset_cols = [col for col in data.columns if any(word in col.lower() for word in ['asset', 'symbol', 'coin'])]
        if asset_cols:
            assets = data[asset_cols[0]].value_counts()
            analysis['assets'] = assets.to_dict()
            analysis['unique_assets'] = len(assets)
        
        return analysis
    
    def _get_date_range(self, dates: List) -> Dict:
        """Obtener rango de fechas"""
        if not dates:
            return None
        
        dates_series = pd.to_datetime(dates)
        return {
            'start': dates_series.min(),
            'end': dates_series.max(),
            'duration_days': (dates_series.max() - dates_series.min()).days
        }
    
    def _generate_smart_alerts(self, analysis: Dict) -> List[str]:
        """Generar alertas inteligentes"""
        alerts = []
        
        # Alertas de rendimiento
        total_pnl = analysis['performance_metrics'].get('total_pnl', 0)
        if total_pnl > 1000:
            alerts.append(f"🎉 Excelente rendimiento: +${total_pnl:,.2f} de ganancia total")
        elif total_pnl < -500:
            alerts.append(f"⚠️ Pérdidas significativas: ${total_pnl:,.2f}")
        
        # Alertas de win rate
        for account, data in analysis['financial_summary'].items():
            if 'win_rate' in data:
                win_rate = data['win_rate']
                if win_rate > 70:
                    alerts.append(f"🏆 {account}: Excelente win rate ({win_rate:.1f}%)")
                elif win_rate < 40:
                    alerts.append(f"🔴 {account}: Win rate bajo ({win_rate:.1f}%)")
        
        return alerts

def create_performance_dashboard(analysis: Dict):
    """📊 Dashboard principal de rendimiento"""
    
    st.markdown('<div class="main-header"><h1>📊 Trading Performance Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Métricas principales
    metrics = analysis.get('performance_metrics', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_pnl = metrics.get('total_pnl', 0)
        delta_color = "normal" if total_pnl >= 0 else "inverse"
        st.metric(
            label="💰 PnL Total",
            value=f"${total_pnl:,.2f}",
            delta=f"{'📈' if total_pnl >= 0 else '📉'} {'Ganancia' if total_pnl >= 0 else 'Pérdida'}"
        )
    
    with col2:
        total_trades = metrics.get('total_trades', 0)
        st.metric(
            label="🔄 Total Trades",
            value=f"{total_trades:,}",
            delta="Transacciones ejecutadas"
        )
    
    with col3:
        total_accounts = metrics.get('total_accounts', 0)
        st.metric(
            label="🏦 Cuentas Activas",
            value=f"{total_accounts}",
            delta="Cuentas analizadas"
        )
    
    with col4:
        date_range = metrics.get('date_range')
        if date_range:
            days = date_range.get('duration_days', 0)
            st.metric(
                label="📅 Período",
                value=f"{days} días",
                delta=f"Desde {date_range['start'].strftime('%Y-%m-%d')}"
            )

def create_account_comparison(analysis: Dict):
    """📈 Comparación entre cuentas"""
    
    st.subheader("🏦 Análisis por Cuenta")
    
    financial_data = analysis.get('financial_summary', {})
    
    if not financial_data:
        st.info("No hay datos de cuentas para mostrar")
        return
    
    # Preparar datos para gráficos
    accounts = []
    pnl_values = []
    win_rates = []
    trade_counts = []
    
    for account, data in financial_data.items():
        accounts.append(account)
        pnl_values.append(data.get('pnl_total', 0))
        win_rates.append(data.get('win_rate', 0))
        trade_counts.append(data.get('total_trades', 0))
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de PnL por cuenta
        fig_pnl = px.bar(
            x=accounts,
            y=pnl_values,
            title="💰 PnL por Cuenta",
            color=pnl_values,
            color_continuous_scale=['red', 'yellow', 'green'],
            labels={'x': 'Cuenta', 'y': 'PnL (USDT)'}
        )
        fig_pnl.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig_pnl, use_container_width=True)
    
    with col2:
        # Gráfico de Win Rate
        fig_winrate = px.bar(
            x=accounts,
            y=win_rates,
            title="🎯 Win Rate por Cuenta",
            color=win_rates,
            color_continuous_scale=['red', 'orange', 'green'],
            labels={'x': 'Cuenta', 'y': 'Win Rate (%)'}
        )
        fig_winrate.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig_winrate, use_container_width=True)
    
    # Tabla detallada
    st.subheader("📋 Detalle por Cuenta")
    
    detail_data = []
    for account, data in financial_data.items():
        detail_data.append({
            'Cuenta': account,
            'PnL Total': f"${data.get('pnl_total', 0):,.2f}",
            'Win Rate': f"{data.get('win_rate', 0):.1f}%",
            'Total Trades': data.get('total_trades', 0),
            'Período (días)': data.get('period_days', 0),
            'Activos Únicos': data.get('unique_assets', 0)
        })
    
    if detail_data:
        df_detail = pd.DataFrame(detail_data)
        st.dataframe(df_detail, use_container_width=True)

def create_advanced_charts(analysis: Dict):
    """📈 Gráficos avanzados"""
    
    st.subheader("📊 Análisis Avanzado")
    
    financial_data = analysis.get('financial_summary', {})
    
    # Gráfico de distribución de PnL
    all_pnl = [data.get('pnl_total', 0) for data in financial_data.values()]
    
    if all_pnl:
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución de resultados
            fig_dist = px.histogram(
                x=all_pnl,
                title="📊 Distribución de Resultados",
                nbins=10,
                labels={'x': 'PnL (USDT)', 'y': 'Frecuencia'},
                color_discrete_sequence=['#FF6B6B']
            )
            fig_dist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            # Métricas de riesgo
            pnl_array = np.array(all_pnl)
            max_gain = np.max(pnl_array) if len(pnl_array) > 0 else 0
            max_loss = np.min(pnl_array) if len(pnl_array) > 0 else 0
            volatility = np.std(pnl_array) if len(pnl_array) > 0 else 0
            
            st.markdown("### 📈 Métricas de Riesgo")
            st.markdown(f"**Máxima Ganancia:** ${max_gain:,.2f}")
            st.markdown(f"**Máxima Pérdida:** ${max_loss:,.2f}")
            st.markdown(f"**Volatilidad:** ${volatility:,.2f}")
            
            # Ratio Sharpe simplificado
            if volatility > 0:
                sharpe_ratio = np.mean(pnl_array) / volatility
                st.markdown(f"**Ratio Sharpe:** {sharpe_ratio:.2f}")

def create_alerts_section(analysis: Dict):
    """🚨 Sección de alertas"""
    
    st.subheader("🚨 Alertas Inteligentes")
    
    alerts = analysis.get('alerts', [])
    
    if alerts:
        for alert in alerts:
            if "🎉" in alert or "🏆" in alert:
                st.success(alert)
            elif "⚠️" in alert or "🔴" in alert:
                st.warning(alert)
            else:
                st.info(alert)
    else:
        st.info("✅ No hay alertas en este momento")

def main():
    """🚀 Función principal de la aplicación"""
    
    # Sidebar
    st.sidebar.markdown("## 🎛️ Control Panel")
    st.sidebar.markdown("---")
    
    # Inicializar analizador
    analyzer = TradingAnalyzerWeb()
    
    # Sección de carga de archivos
    st.sidebar.markdown("### 📁 Cargar Archivo")
    uploaded_file = st.sidebar.file_uploader(
        "Selecciona tu archivo Excel o CSV",
        type=['xlsx', 'xls', 'csv'],
        help="Soporta archivos de BingX, Binance y otros exchanges"
    )
    
    if uploaded_file is not None:
        # Cargar datos
        with st.spinner("🔄 Cargando y analizando datos..."):
            if analyzer.load_data_from_upload(uploaded_file):
                st.sidebar.success(f"✅ Archivo cargado: {uploaded_file.name}")
                
                # Generar análisis
                analysis = analyzer.generate_comprehensive_analysis()
                
                # Guardar en session state para persistencia
                st.session_state['analysis'] = analysis
                st.session_state['analyzer'] = analyzer
            else:
                st.sidebar.error("❌ Error cargando archivo")
    
    # Mostrar análisis si existe
    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        
        # Opciones del sidebar
        st.sidebar.markdown("### 📊 Secciones")
        show_dashboard = st.sidebar.checkbox("📈 Dashboard Principal", value=True)
        show_accounts = st.sidebar.checkbox("🏦 Análisis por Cuenta", value=True)
        show_charts = st.sidebar.checkbox("📊 Gráficos Avanzados", value=True)
        show_alerts = st.sidebar.checkbox("🚨 Alertas", value=True)
        
        # Renderizar secciones
        if show_dashboard:
            create_performance_dashboard(analysis)
            st.markdown("---")
        
        if show_accounts:
            create_account_comparison(analysis)
            st.markdown("---")
        
        if show_charts:
            create_advanced_charts(analysis)
            st.markdown("---")
        
        if show_alerts:
            create_alerts_section(analysis)
        
        # Botón de descarga de reporte
        st.sidebar.markdown("### 📄 Exportar")
        if st.sidebar.button("📥 Descargar Reporte"):
            report_content = generate_report(analysis)
            st.sidebar.download_button(
                label="💾 Guardar Reporte",
                data=report_content,
                file_name=f"trading_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    else:
        # Pantalla de bienvenida
        st.markdown("""
        <div class="main-header">
            <h1>🚀 Trading Analyzer Pro</h1>
            <p>Análisis Avanzado de Trading con Inteligencia Artificial</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        """)

def generate_report(analysis: Dict) -> str:
    """Generar reporte en texto"""
    report = "🚀 TRADING ANALYZER PRO - REPORTE AVANZADO\n"
    report += "=" * 60 + "\n"
    report += f"📅 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Métricas principales
    metrics = analysis.get('performance_metrics', {})
    report += "💰 MÉTRICAS PRINCIPALES\n"
    report += "-" * 30 + "\n"
    report += f"PnL Total: ${metrics.get('total_pnl', 0):,.2f}\n"
    report += f"Total Trades: {metrics.get('total_trades', 0):,}\n"
    report += f"Cuentas Activas: {metrics.get('total_accounts', 0)}\n\n"
    
    # Detalles por cuenta
    financial_data = analysis.get('financial_summary', {})
    if financial_data:
        report += "🏦 ANÁLISIS POR CUENTA\n"
        report += "-" * 30 + "\n"
        for account, data in financial_data.items():
            report += f"\n📊 {account}:\n"
            report += f"  PnL: ${data.get('pnl_total', 0):,.2f}\n"
            if 'win_rate' in data:
                report += f"  Win Rate: {data['win_rate']:.1f}%\n"
            if 'total_trades' in data:
                report += f"  Trades: {data['total_trades']}\n"
    
    # Alertas
    alerts = analysis.get('alerts', [])
    if alerts:
        report += "\n🚨 ALERTAS\n"
        report += "-" * 20 + "\n"
        for alert in alerts:
            report += f"• {alert}\n"
    
    return report

if __name__ == "__main__":
    main()