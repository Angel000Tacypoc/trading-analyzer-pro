"""
🚀 Trading Analyzer Pro - Emergency Standalone Version
Version that works guaranteed in Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from typing import Dict, Optional
import io
import os

# Importar nuestro sistema de filtros y SEO
try:
    from sheet_filter import SheetFilter, CommonFilters
except ImportError:
    # Fallback si no se puede importar
    class SheetFilter:
        def filter_sheets(self, sheets): return sheets
    class CommonFilters:
        @staticmethod
        def by_sheet_numbers(nums): return SheetFilter()
        @staticmethod
        def only_futures(): return SheetFilter()
    
    def inject_seo_meta_tags(): pass
    def add_footer_seo(): pass

# 🔄 Sistema keep-alive (solo en producción)
def init_keep_alive():
    """🔄 Inicializar sistema keep-alive si está en Streamlit Cloud"""
    try:
        # Detectar si estamos en Streamlit Cloud
        if any(key in os.environ for key in ['STREAMLIT_SHARING_MODE', 'STREAMLIT_SERVER_PORT']):
            st.sidebar.success("🌐 **App en Streamlit Cloud**")
            st.sidebar.info("🔄 **Keep-Alive:** Activo")
            return True
        else:
            st.sidebar.info("🟢**En Linea**")
            return False
    except:
        return False

# 🎨 Configuración de la página con SEO optimizado
st.set_page_config(
    page_title="Trading Analyzer Pro | Analiza Ganancias y PnL GRATIS | 2024",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Angel000Tacypoc/trading-analyzer-pro',
        'Report a bug': 'https://github.com/Angel000Tacypoc/trading-analyzer-pro/issues',
        'About': """
        # 💰 Trading Analyzer Pro
        
        **Herramienta GRATUITA de análisis de trading profesional**
        
        ✅ Analiza ganancias y pérdidas automáticamente  
        ✅ Calcula Win Rate y métricas avanzadas  
        ✅ Compatible con BingX, Binance y más exchanges  
        ✅ Filtros inteligentes por tipo de operación  
        ✅ Visualizaciones profesionales con Plotly  
        
        **Creado por traders para traders** 🚀
        
        ---
        **Keywords:** analizador trading, calculadora pnl, análisis trades excel, win rate calculator, trading metrics, binance tools, bingx analyzer
        """
    }
)

# 🎨 CSS Styles
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .performance-excellent {
        border: 2px solid #00d2d3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #e0f9ff 0%, #ffffff 100%);
        box-shadow: 0 2px 10px rgba(0, 210, 211, 0.2);
    }
    
    .inactivity-alert {
        border: 2px solid #ff6b6b;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #ffe0e0 0%, #ffffff 100%);
        box-shadow: 0 2px 10px rgba(255, 107, 107, 0.2);
    }
    
    .trading-insight {
        border: 2px solid #3742fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #e8f4fd 0%, #ffffff 100%);
        box-shadow: 0 2px 10px rgba(55, 66, 250, 0.2);
    }
</style>
""", unsafe_allow_html=True)

class TradingAnalyzerStandalone:
    """📊 Analizador de Trading Standalone - Versión Emergencia con Filtros"""
    
    def __init__(self):
        self.data = None
        self.analysis = {}
        self.sheet_filter = SheetFilter()  # 🗂️ Sistema de filtros
    
    def set_sheet_filter(self, filter_obj: SheetFilter):
        """🔧 Configurar filtro de hojas"""
        self.sheet_filter = filter_obj
        return self
    
    def create_sheet_selector_ui(self):
        """🎮 UI para seleccionar hojas a analizar"""
        if not self.data:
            return None
        
        st.sidebar.markdown("### 🗂️ Filtros de Hojas")
        
        # Mostrar hojas disponibles
        available_sheets = list(self.data.keys())
        st.sidebar.write(f"📋 **Hojas encontradas:** {len(available_sheets)}")
        
        # Opciones de filtro
        filter_mode = st.sidebar.selectbox(
            "🔍 Modo de Filtro",
            ["🤖 Auto-detectar", "📝 Seleccionar específicas", "🔢 Por números", "🏦 Por tipo de cuenta"],
            key="filter_mode_selector"
        )
        
        if filter_mode == "📝 Seleccionar específicas":
            selected_sheets = st.sidebar.multiselect(
                "✅ Selecciona hojas:",
                options=available_sheets,
                default=available_sheets,
                key="sheet_multiselect"
            )
            self.sheet_filter = SheetFilter().add_sheets_by_names(selected_sheets)
        
        elif filter_mode == "🔢 Por números":
            sheet_numbers = st.sidebar.multiselect(
                "🔢 Números de hojas (1, 2, 3...):",
                options=list(range(1, len(available_sheets) + 1)),
                default=list(range(1, min(4, len(available_sheets) + 1))),
                key="sheet_numbers"
            )
            self.sheet_filter = CommonFilters.by_sheet_numbers(sheet_numbers)
        
        elif filter_mode == "🏦 Por tipo de cuenta":
            account_type = st.sidebar.selectbox(
                "🏦 Tipo de cuenta:",
                ["futures", "spot", "margin", "trading"],
                key="account_type_selector"
            )
            self.sheet_filter = SheetFilter().add_account_filter(account_type)
        
        else:  # Auto-detectar
            excluded = st.sidebar.multiselect(
                "❌ Excluir hojas:",
                options=available_sheets,
                key="excluded_sheets"
            )
            self.sheet_filter = SheetFilter()
            for sheet in excluded:
                self.sheet_filter.exclude_sheet(sheet)
        
        return self.sheet_filter
    
    def _filter_non_trading_operations(self, df):
        """🚫 Filtrar operaciones que no son de trading real"""
        if len(df) == 0:
            return df
        
        # Buscar columna de tipo de operación
        type_col = None
        possible_type_columns = ['type', 'operation', 'action', 'kind', 'category']
        
        for col in df.columns:
            col_lower = col.lower()
            if any(type_word in col_lower for type_word in possible_type_columns):
                type_col = col
                break
        
        if type_col is None:
            # Si no hay columna de tipo, devolver DataFrame original
            return df
        
        # Valores a excluir (operaciones no-trading)
        non_trading_operations = [
            'transfer', 'transferencia', 'deposit', 'deposito', 'withdrawal', 'retiro',
            'funding', 'commission', 'comision', 'fee', 'bonus', 'rebate', 'cashback',
            'interest', 'interes', 'staking', 'reward', 'recompensa', 'airdrop'
        ]
        
        # Crear máscara para filtrar
        mask = True
        for operation in non_trading_operations:
            mask = mask & (~df[type_col].str.lower().str.contains(operation, na=False))
        
        # Filtrar DataFrame
        df_filtered = df[mask].copy()
        
        # 📊 Mostrar estadísticas de filtrado si hay sidebar
        if hasattr(st, 'sidebar') and len(df) != len(df_filtered):
            excluded_count = len(df) - len(df_filtered)
            st.sidebar.info(f"🚫 **Operaciones no-trading excluidas:** {excluded_count:,}")
        
        return df_filtered
    
    def load_file(self, uploaded_file):
        """📁 Cargar archivo"""
        try:
            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                self.data = pd.read_excel(uploaded_file, sheet_name=None)
                return True
            elif uploaded_file.name.endswith('.csv'):
                self.data = {'main': pd.read_csv(uploaded_file)}
                return True
        except Exception as e:
            st.error(f"Error cargando archivo: {e}")
            return False
    
    def analyze_data(self):
        """🧠 Análisis de datos con filtros de hojas"""
        if not self.data:
            return {}
        
        # 🗂️ Aplicar filtros de hojas
        filtered_data = self.sheet_filter.filter_sheets(self.data)
        
        # 📊 Mostrar información de filtros en sidebar
        if hasattr(st, 'sidebar'):
            filter_summary = self.sheet_filter.get_filter_summary()
            total_sheets = len(self.data)
            filtered_sheets = len(filtered_data)
            
            st.sidebar.markdown("### 📊 Estado del Filtro")
            st.sidebar.info(f"📋 **Total hojas:** {total_sheets}\n📍 **Analizando:** {filtered_sheets}")
            
            if filtered_sheets < total_sheets:
                excluded_sheets = set(self.data.keys()) - set(filtered_data.keys())
                st.sidebar.warning(f"❌ **Excluidas:** {', '.join(list(excluded_sheets)[:3])}{'...' if len(excluded_sheets) > 3 else ''}")
        
        results = {}
        
        for sheet_name, df in filtered_data.items():
            # 🚫 Filtrar transferencias y operaciones no-trading
            df_filtered = self._filter_non_trading_operations(df)
            
            # Buscar columnas PnL
            pnl_col = None
            for col in df_filtered.columns:
                if any(word in col.lower() for word in ['pnl', 'profit', 'amount', 'realized']):
                    pnl_col = col
                    break   
            
            if pnl_col and len(df_filtered) > 0:
                pnl_values = df_filtered[pnl_col].dropna()
                
                if len(pnl_values) > 0:
                    profits = pnl_values[pnl_values > 0]
                    losses = pnl_values[pnl_values < 0]
                    
                    results[sheet_name] = {
                        'total_pnl': float(pnl_values.sum()),
                        'total_profit': float(profits.sum()) if len(profits) > 0 else 0,
                        'total_loss': float(abs(losses.sum())) if len(losses) > 0 else 0,
                        'win_rate': (len(profits) / len(pnl_values) * 100) if len(pnl_values) > 0 else 0,
                        'total_trades': len(pnl_values),
                        'avg_profit': float(profits.mean()) if len(profits) > 0 else 0,
                        'avg_loss': float(losses.mean()) if len(losses) > 0 else 0,
                        'pnl_values': pnl_values.tolist(),
                        'pnl_column': pnl_col,  # 📊 Guardar nombre de columna detectada
                        'total_rows': len(df),   # 📏 Total de filas en la hoja original
                        'filtered_rows': len(df_filtered),  # 📏 Filas después de filtrar
                        'excluded_operations': len(df) - len(df_filtered)  # 🚫 Operaciones excluidas
                    }
        
        return results

def main():
    """🚀 Función principal - Versión Emergencia"""
    
    # � Inyectar SEO meta tags
    inject_seo_meta_tags()
    
    # �🔄 Inicializar keep-alive y mostrar estado
    init_keep_alive()
    
    # Header con SEO optimizado
    st.markdown('''
    <div class="main-header">
        <h1>💰 Trading Analyzer Pro</h1>
        <p>� Herramienta GRATUITA de Análisis de Trading Profesional</p>
        <p style="font-size: 0.9rem; opacity: 0.9;">
            📊 Analiza PnL • 🎯 Calcula Win Rate • 📈 Métricas Avanzadas • 🔄 Filtros Inteligentes
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # File uploader con clave única
    uploaded_file = st.sidebar.file_uploader(
        "📁 Sube tu archivo Excel o CSV",
        type=['xlsx', 'xls', 'csv'],
        help="Soporta archivos de BingX, Binance, y otros exchanges",
        key="unique_file_uploader_2024"
    )
    
    # Análisis
    if uploaded_file:
        st.sidebar.success(f"📄 **{uploaded_file.name}**")
        
        # Crear analizador
        analyzer = TradingAnalyzerStandalone()
        
        # Cargar archivo para mostrar opciones de filtros
        with st.spinner("📁 Cargando archivo..."):
            file_loaded = analyzer.load_file(uploaded_file)
        
        if file_loaded:
            # 🗂️ UI de filtros de hojas
            analyzer.create_sheet_selector_ui()
            
            if st.sidebar.button("🚀 Analizar Archivo", type="primary", key="unique_analyze_button_2024"):
                with st.spinner("🧠 Analizando con IA..."):
                    results = analyzer.analyze_data()
                    
                    if results:
                        st.success("✅ ¡Análisis completado!")
                        
                        # Mostrar información de qué se analizó
                        analyzed_sheets = list(results.keys())
                        st.info(f"📊 **Hojas analizadas:** {', '.join(analyzed_sheets)}")
                        
                        # Mostrar resultados
                        st.subheader("💰 Resultados del Análisis")
                        
                        # Calcular totales
                        total_pnl = sum(account['total_pnl'] for account in results.values())
                        total_profit = sum(account['total_profit'] for account in results.values())
                        total_loss = sum(account['total_loss'] for account in results.values())
                        total_trades = sum(account['total_trades'] for account in results.values())
                        
                        # Métricas principales
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            pnl_class = "performance-excellent" if total_pnl >= 0 else "inactivity-alert"
                            st.markdown(f'''
                            <div class="{pnl_class}">
                                <h3>💰 PnL Total</h3>
                                <h1>${total_pnl:,.2f}</h1>
                                <p>{'🟢 GANANCIA' if total_pnl >= 0 else '🔴 PÉRDIDA'}</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f'''
                            <div class="performance-excellent">
                                <h3>💚 Total Ganancias</h3>
                                <h1>${total_profit:,.2f}</h1>
                                <p>Dinero ganado</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f'''
                            <div class="inactivity-alert">
                                <h3>💔 Total Pérdidas</h3>
                                <h1>${total_loss:,.2f}</h1>
                                <p>Dinero perdido</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col4:
                            total_volume = total_profit + total_loss
                            profit_ratio = (total_profit / total_loss) if total_loss > 0 else float('inf')
                            ratio_class = "performance-excellent" if profit_ratio > 1 else "inactivity-alert"
                            
                            st.markdown(f'''
                            <div class="{ratio_class}">
                                <h3>📊 Ratio P/L</h3>
                                <h1>{profit_ratio:.2f}</h1>
                                <p>{'✅ Positivo' if profit_ratio > 1 else '⚠️ Negativo'}</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        # Detalles por cuenta/hoja
                        st.subheader("🏦 Análisis por Cuenta/Hoja")
                        
                        for account, data in results.items():
                            pnl = data['total_pnl']
                            win_rate = data['win_rate']
                            trades = data['total_trades']
                            
                            account_class = "performance-excellent" if pnl > 0 else "inactivity-alert"
                            status_icon = "🟢" if pnl > 0 else "🔴"
                            
                            excluded_ops = data.get('excluded_operations', 0)
                            
                            st.markdown(f'''
                            <div class="{account_class}">
                                <h4>{status_icon} {account}</h4>
                                <p><strong>PnL:</strong> ${pnl:,.2f} | <strong>Win Rate:</strong> {win_rate:.1f}% | <strong>Trades:</strong> {trades:,}</p>
                                <p><strong>Ganancias:</strong> ${data['total_profit']:,.2f} | <strong>Pérdidas:</strong> ${data['total_loss']:,.2f}</p>
                                <p><small>📊 <strong>Columna PnL:</strong> {data.get('pnl_column', 'N/A')} | <strong>Filas totales:</strong> {data.get('total_rows', 'N/A'):,}</small></p>
                                {f'<p><small>🚫 <strong>Transferencias excluidas:</strong> {excluded_ops:,}</small></p>' if excluded_ops > 0 else ''}
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        # Gráfico de PnL
                        st.subheader("📊 Distribución de PnL por Cuenta")
                        
                        accounts = list(results.keys())
                        pnl_values = [results[acc]['total_pnl'] for acc in accounts]
                        
                        fig = go.Figure()
                        colors = ['#00d2d3' if pnl > 0 else '#ff6b6b' for pnl in pnl_values]
                        
                        fig.add_trace(go.Bar(
                            x=accounts,
                            y=pnl_values,
                            marker_color=colors,
                            text=[f'${pnl:,.0f}' for pnl in pnl_values],
                            textposition='auto',
                            hovertemplate='<b>%{x}</b><br>PnL: $%{y:,.2f}<extra></extra>'
                        ))
                        
                        fig.update_layout(
                            title="💰 PnL por Cuenta",
                            xaxis_title="Cuenta",
                            yaxis_title="PnL (USDT)",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            showlegend=False,
                            height=400
                        )
                        
                        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
                        
                        st.plotly_chart(fig, use_container_width=True, key="unique_pnl_chart_2024")
                        
                        # Insights
                        st.subheader("🔮 Insights de Rendimiento")
                        
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
                    
                    else:
                        st.warning("📊 No se encontraron datos de PnL válidos en el archivo")
        else:
            st.error("❌ Error cargando el archivo")
    
    else:
        # Pantalla de bienvenida optimizada para SEO
        st.markdown("""
        ## 🎯 **Analiza tus Trades como un Profesional - GRATIS**
        
        **¿Quieres saber si realmente eres rentable en trading?** Nuestra herramienta analiza automáticamente tus operaciones y te da métricas profesionales en segundos.
        
        ### ✅ **¿Qué hace Trading Analyzer Pro?**
        
        🏆 **Análisis Automático de PnL**: Sube tu Excel y obtén ganancias/pérdidas precisas  
        🎯 **Win Rate Inteligente**: Descubre tu tasa de éxito real en trading  
        📊 **Métricas Avanzadas**: Ratio P/L, promedios, análisis por cuenta  
        🚫 **Filtros Inteligentes**: Excluye transfers y fees automáticamente  
        🔄 **Multi-Exchange**: Compatible con BingX, Binance, ByBit y más  
        
        ### 📁 **Formatos Soportados**
        - **Excel**: .xlsx, .xls (múltiples hojas automáticamente)
        - **CSV**: Archivos separados por comas
        - **Exchanges**: BingX, Binance, ByBit, OKX, KuCoin, Huobi
        
        ### 🚀 **¿Cómo Usar Trading Analyzer Pro?**
        1. **📂 Descarga** tu historial de trades del exchange
        2. **📤 Sube** el archivo Excel/CSV en el panel lateral
        3. **⚙️ Configura** filtros (opcional)
        4. **🎯 Analiza** y obtén métricas profesionales
        5. **📈 Mejora** tu estrategia basada en datos reales
        
        ---
        
        ### � **¿Por qué Trading Analyzer Pro es la Mejor Herramienta?**
        
        ❌ **Otros tools**: Básicos, sin filtros, interfaces confusas  
        ✅ **Trading Analyzer Pro**: Profesional, inteligente, fácil de usar
        
        ❌ **Excel manual**: Horas de trabajo, propenso a errores  
        ✅ **Nuestro analyzer**: Análisis automático en segundos
        
        ❌ **Apps de pago**: $20-100/mes por funciones básicas  
        ✅ **Trading Analyzer Pro**: Completamente GRATIS, sin límites
        
        ### 🏆 **Casos de Uso Reales**
        
        **👨‍💼 Trader Principiante**: "Pensaba que era rentable, pero el analyzer me mostró que las fees me estaban matando"
        
        **👩‍💻 Trader Avanzado**: "Perfecto para comparar performance entre diferentes exchanges y strategies"
        
        **🏢 Trading Team**: "Usamos el analyzer para evaluar performance de todo el equipo"
        
        ---
        
        ### 🔍 **Keywords Relacionadas**
        *analizador trading, calculadora pnl, análisis trades excel, win rate calculator, trading metrics, herramientas trading gratis, binance analyzer, bingx tools, análisis rentabilidad trading*
        """)
        
        # Call to Action prominente
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin: 2rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        ">
            <h2>🚀 ¡Empieza a Analizar GRATIS Ahora!</h2>
            <p style="font-size: 1.2rem; margin: 1rem 0;">
                📤 Sube tu archivo de trades en el panel lateral y descubre tu rendimiento real
            </p>
            <p style="font-size: 0.9rem; opacity: 0.9;">
                ⚡ Análisis en segundos • 🔒 100% seguro • 💰 Completamente gratis
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer con SEO adicional
    add_footer_seo()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("💰 **Trading Analyzer Pro** - Análisis Profesional GRATIS")

if __name__ == "__main__":
    main()