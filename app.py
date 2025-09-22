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
import json
from collections import defaultdict
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="🧠 Trading Analyzer Pro - IA Avanzada",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        font-weight: bold;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .insight-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .alert-critical {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        border-left: 5px solid #e55039;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
        border-left: 5px solid #ff6348;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%);
        border-left: 5px solid #006ba6;
    }
    
    .metric-premium {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        color: #2c3e50;
        font-weight: bold;
    }
    
    .trading-insight {
        border: 2px solid #3742fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #e8f4fd 0%, #ffffff 100%);
    }
    
    .inactivity-alert {
        border: 2px solid #ff6b6b;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #ffe0e0 0%, #ffffff 100%);
    }
    
    .performance-excellent {
        border: 2px solid #00d2d3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #e0f9ff 0%, #ffffff 100%);
    }
</style>
""", unsafe_allow_html=True)

class AdvancedTradingAnalyzer:
    """🧠 Analizador de Trading Avanzado con IA - Versión Mejorada"""
    
    def __init__(self):
        self.sheets = {}
        self.analysis_results = {}
        self.comprehensive_insights = {}
        
    def load_data_from_upload(self, uploaded_file) -> bool:
        """Cargar datos desde archivo subido con validación avanzada"""
        try:
            st.info("📁 Procesando archivo...")
            
            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                # Mostrar progreso
                progress = st.progress(0)
                progress.progress(20)
                
                excel_sheets = pd.read_excel(uploaded_file, sheet_name=None)
                progress.progress(60)
                
                self.sheets = excel_sheets
                progress.progress(100)
                
                st.success(f"✅ Excel cargado exitosamente:")
                st.info(f"📊 **{len(excel_sheets)} hojas detectadas**")
                
                # Mostrar resumen de cada hoja
                for sheet_name, data in excel_sheets.items():
                    st.write(f"  • **{sheet_name}**: {len(data):,} transacciones")
                    
                # Limpiar barra de progreso
                progress.empty()
                return True
                
            elif uploaded_file.name.endswith('.csv'):
                progress = st.progress(0)
                progress.progress(30)
                
                csv_data = pd.read_csv(uploaded_file)
                progress.progress(80)
                
                self.sheets = {'main': csv_data}
                progress.progress(100)
                
                st.success(f"✅ CSV cargado exitosamente:")
                st.info(f"📊 **{len(csv_data):,} transacciones detectadas**")
                
                # Mostrar columnas detectadas
                st.write(f"  • **Columnas**: {', '.join(csv_data.columns[:5])}{'...' if len(csv_data.columns) > 5 else ''}")
                
                progress.empty()
                return True
            else:
                st.error("❌ **Formato no soportado**")
                st.error("📋 Formatos aceptados: Excel (.xlsx, .xls) o CSV (.csv)")
                return False
                
        except Exception as e:
            st.error(f"❌ **Error cargando archivo**: {str(e)}")
            st.error("💡 **Posibles soluciones:**")
            st.error("  • Verifica que el archivo no esté corrupto")
            st.error("  • Asegúrate de que sea un archivo de trading válido")
            st.error("  • Intenta con un formato diferente (Excel ↔ CSV)")
            return False

    def generate_comprehensive_analysis(self) -> Dict:
        """🧠 ANÁLISIS COMPREHENSIVO MEJORADO CON IA AVANZADA"""
        if not self.sheets:
            return {}
        
        st.info("🧠 Ejecutando análisis con IA avanzada...")
        progress_bar = st.progress(0)
        
        analysis = {
            'financial_insights': {},
            'temporal_analysis': {},
            'inactivity_patterns': {},
            'trading_performance': {},
            'risk_metrics': {},
            'smart_alerts': [],
            'predictive_insights': {},
            'comparative_analysis': {}
        }
        
        total_pnl = 0
        total_trades = 0
        all_transactions = []
        accounts_data = {}
        
        progress_bar.progress(10)
        
        # Análisis por cuenta con IA
        for idx, (sheet_name, sheet_data) in enumerate(self.sheets.items()):
            if sheet_data is None or sheet_data.empty:
                continue
            
            progress_bar.progress(20 + (idx * 30 // len(self.sheets)))
            
            # Análisis profundo por cuenta
            account_analysis = self._deep_account_analysis(sheet_data, sheet_name)
            analysis['financial_insights'][sheet_name] = account_analysis
            
            # Recopilar datos globales
            if 'pnl_total' in account_analysis:
                total_pnl += account_analysis['pnl_total']
            if 'total_trades' in account_analysis:
                total_trades += account_analysis['total_trades']
            if 'all_transactions' in account_analysis:
                all_transactions.extend(account_analysis['all_transactions'])
            
            accounts_data[sheet_name] = account_analysis
        
        progress_bar.progress(60)
        
        # Análisis temporal avanzado
        analysis['temporal_analysis'] = self._advanced_temporal_analysis(accounts_data)
        
        progress_bar.progress(70)
        
        # Análisis de inactividad inteligente
        analysis['inactivity_patterns'] = self._intelligent_inactivity_analysis(accounts_data)
        
        progress_bar.progress(80)
        
        # Análisis de rendimiento de trading
        analysis['trading_performance'] = self._advanced_trading_performance(accounts_data)
        
        progress_bar.progress(90)
        
        # Métricas de riesgo avanzadas
        analysis['risk_metrics'] = self._calculate_advanced_risk_metrics(accounts_data, total_pnl, total_trades)
        
        # Alertas inteligentes mejoradas
        analysis['smart_alerts'] = self._generate_smart_alerts_advanced(analysis)
        
        # Insights predictivos
        analysis['predictive_insights'] = self._generate_predictive_insights(accounts_data, all_transactions)
        
        # Análisis comparativo
        analysis['comparative_analysis'] = self._comparative_analysis(accounts_data)
        
        progress_bar.progress(100)
        self.comprehensive_insights = analysis
        
        return analysis
    
    def _deep_account_analysis(self, data: pd.DataFrame, sheet_name: str) -> Dict:
        """🔍 Análisis profundo por cuenta con IA"""
        analysis = {
            'sheet_name': sheet_name,
            'raw_transactions': len(data),
            'all_transactions': []
        }
        
        # Análisis temporal mejorado
        date_cols = [col for col in data.columns if any(word in col.lower() for word in ['time', 'date', 'utc', 'timestamp'])]
        if date_cols:
            try:
                dates = pd.to_datetime(data[date_cols[0]])
                analysis['dates'] = dates.tolist()
                analysis['period_days'] = (dates.max() - dates.min()).days
                analysis['first_transaction'] = dates.min()
                analysis['last_transaction'] = dates.max()
                analysis['transaction_frequency'] = len(data) / max(analysis['period_days'], 1)
                
                # Análisis de actividad por día de la semana
                weekday_activity = dates.dt.day_name().value_counts()
                analysis['most_active_weekday'] = weekday_activity.index[0]
                analysis['weekday_distribution'] = weekday_activity.to_dict()
                
                # Análisis de actividad por hora
                if hasattr(dates.dt, 'hour'):
                    hourly_activity = dates.dt.hour.value_counts().sort_index()
                    peak_hour = hourly_activity.idxmax()
                    analysis['peak_trading_hour'] = f"{peak_hour}:00"
                    analysis['hourly_distribution'] = hourly_activity.to_dict()
                
                # Análisis mensual detallado
                monthly_activity = dates.dt.to_period('M').value_counts().sort_index()
                if len(monthly_activity) > 0:
                    analysis['most_active_month'] = str(monthly_activity.idxmax())
                    analysis['monthly_activity'] = {str(k): v for k, v in monthly_activity.to_dict().items()}
                    
                    # Tendencia mensual
                    if len(monthly_activity) > 1:
                        monthly_trend = np.polyfit(range(len(monthly_activity)), monthly_activity.values, 1)[0]
                        analysis['monthly_trend'] = 'increasing' if monthly_trend > 0 else 'decreasing'
                        analysis['trend_strength'] = abs(monthly_trend)
                
            except Exception as e:
                st.warning(f"⚠️ Error en análisis temporal para {sheet_name}: {e}")
        
        # Análisis financiero avanzado
        amount_cols = [col for col in data.columns if any(word in col.lower() for word in ['amount', 'pnl', 'balance', 'profit', 'loss'])]
        
        for col in amount_cols:
            if data[col].dtype in ['float64', 'int64']:
                values = data[col].dropna()
                if len(values) > 0:
                    analysis[f'{col}_total'] = float(values.sum())
                    analysis[f'{col}_mean'] = float(values.mean())
                    analysis[f'{col}_median'] = float(values.median())
                    analysis[f'{col}_std'] = float(values.std())
                    analysis[f'{col}_min'] = float(values.min())
                    analysis[f'{col}_max'] = float(values.max())
                    
                    # Detectar PnL principal
                    if any(keyword in col.lower() for keyword in ['amount', 'pnl', 'profit']):
                        if 'pnl' in col.lower() or 'profit' in col.lower():
                            analysis['pnl_total'] = float(values.sum())
                            analysis['pnl_values'] = values.tolist()
                            
                            # Análisis de rachas
                            positive_streak, negative_streak = self._calculate_streaks(values)
                            analysis['max_winning_streak'] = positive_streak
                            analysis['max_losing_streak'] = negative_streak
                            
                            # Análisis de drawdown
                            cumulative = values.cumsum()
                            running_max = cumulative.expanding().max()
                            drawdown = cumulative - running_max
                            analysis['max_drawdown'] = float(drawdown.min())
                            analysis['current_drawdown'] = float(drawdown.iloc[-1])
        
        # Análisis de tipos de transacción mejorado
        type_cols = [col for col in data.columns if any(word in col.lower() for word in ['type', 'side', 'action', 'operation'])]
        if type_cols:
            types = data[type_cols[0]].value_counts()
            analysis['transaction_types'] = types.to_dict()
            analysis['unique_transaction_types'] = len(types)
            
            # Detección inteligente de trading
            trading_keywords = ['realized', 'pnl', 'fee', 'trade', 'buy', 'sell', 'long', 'short', 'open', 'close']
            trading_mask = data[type_cols[0]].str.contains('|'.join(trading_keywords), case=False, na=False)
            trading_data = data[trading_mask]
            
            if not trading_data.empty and amount_cols:
                analysis['total_trades'] = len(trading_data)
                analysis['trading_percentage'] = (len(trading_data) / len(data)) * 100
                
                # Win rate mejorado
                pnl_values = trading_data[amount_cols[0]].dropna()
                if len(pnl_values) > 0:
                    wins = (pnl_values > 0).sum()
                    losses = (pnl_values < 0).sum()
                    neutral = (pnl_values == 0).sum()
                    total = len(pnl_values)
                    
                    analysis['win_rate'] = (wins / total) * 100
                    analysis['loss_rate'] = (losses / total) * 100
                    analysis['neutral_rate'] = (neutral / total) * 100
                    analysis['wins'] = wins
                    analysis['losses'] = losses
                    analysis['neutral'] = neutral
                    
                    if wins > 0:
                        winning_trades = pnl_values[pnl_values > 0]
                        analysis['avg_win'] = float(winning_trades.mean())
                        analysis['largest_win'] = float(winning_trades.max())
                        analysis['median_win'] = float(winning_trades.median())
                    
                    if losses > 0:
                        losing_trades = pnl_values[pnl_values < 0]
                        analysis['avg_loss'] = float(losing_trades.mean())
                        analysis['largest_loss'] = float(losing_trades.min())
                        analysis['median_loss'] = float(losing_trades.median())
                    
                    # Profit factor
                    gross_profit = pnl_values[pnl_values > 0].sum()
                    gross_loss = abs(pnl_values[pnl_values < 0].sum())
                    if gross_loss > 0:
                        analysis['profit_factor'] = gross_profit / gross_loss
                    
                    # Expectancy
                    if total > 0:
                        win_rate_decimal = wins / total
                        loss_rate_decimal = losses / total
                        avg_win = analysis.get('avg_win', 0)
                        avg_loss = abs(analysis.get('avg_loss', 0))
                        if loss_rate_decimal > 0 and avg_loss > 0:
                            analysis['expectancy'] = (win_rate_decimal * avg_win) - (loss_rate_decimal * avg_loss)
                
                # Análisis de tamaños de posición
                if len(pnl_values) > 0:
                    abs_values = pnl_values.abs()
                    analysis['avg_position_size'] = float(abs_values.mean())
                    analysis['position_size_std'] = float(abs_values.std())
                    analysis['largest_position'] = float(abs_values.max())
                    analysis['smallest_position'] = float(abs_values.min())
        
        # Análisis de activos avanzado
        asset_cols = [col for col in data.columns if any(word in col.lower() for word in ['asset', 'symbol', 'coin', 'currency', 'pair', 'instrument'])]
        if asset_cols:
            assets = data[asset_cols[0]].value_counts()
            analysis['assets'] = assets.to_dict()
            analysis['unique_assets'] = len(assets)
            analysis['most_traded_asset'] = assets.index[0] if len(assets) > 0 else None
            analysis['asset_concentration'] = (assets.iloc[0] / len(data)) * 100 if len(assets) > 0 else 0
            
            # Diversificación
            if len(assets) > 1:
                # Índice de Herfindahl para medir concentración
                proportions = assets / assets.sum()
                herfindahl_index = (proportions ** 2).sum()
                analysis['diversification_index'] = 1 - herfindahl_index
                analysis['is_diversified'] = herfindahl_index < 0.5
        
        # Recopilar todas las transacciones para análisis global
        analysis['all_transactions'] = []
        if amount_cols and date_cols:
            for idx, row in data.iterrows():
                try:
                    transaction = {
                        'date': pd.to_datetime(row[date_cols[0]]),
                        'amount': float(row[amount_cols[0]]),
                        'account': sheet_name
                    }
                    if type_cols:
                        transaction['type'] = str(row[type_cols[0]])
                    if asset_cols:
                        transaction['asset'] = str(row[asset_cols[0]])
                    analysis['all_transactions'].append(transaction)
                except:
                    continue
        
        return analysis
    
    def generate_comprehensive_analysis(self) -> Dict:
        """🧠 ANÁLISIS COMPREHENSIVO MEJORADO CON IA AVANZADA"""
        if not self.sheets:
            return {}
        
        st.info("🧠 Ejecutando análisis con IA avanzada...")
        progress_bar = st.progress(0)
        
        analysis = {
            'financial_insights': {},
            'temporal_analysis': {},
            'inactivity_patterns': {},
            'trading_performance': {},
            'risk_metrics': {},
            'smart_alerts': [],
            'predictive_insights': {},
            'comparative_analysis': {}
        }
        
        total_pnl = 0
        total_trades = 0
        all_transactions = []
        accounts_data = {}
        
        progress_bar.progress(10)
        
        # Análisis por cuenta con IA
        for idx, (sheet_name, sheet_data) in enumerate(self.sheets.items()):
            if sheet_data is None or sheet_data.empty:
                continue
            
            progress_bar.progress(20 + (idx * 30 // len(self.sheets)))
            
            # Análisis profundo por cuenta
            account_analysis = self._deep_account_analysis(sheet_data, sheet_name)
            analysis['financial_insights'][sheet_name] = account_analysis
            
            # Recopilar datos globales
            if 'pnl_total' in account_analysis:
                total_pnl += account_analysis['pnl_total']
            if 'total_trades' in account_analysis:
                total_trades += account_analysis['total_trades']
            if 'all_transactions' in account_analysis:
                all_transactions.extend(account_analysis['all_transactions'])
            
            accounts_data[sheet_name] = account_analysis
        
        progress_bar.progress(60)
        
        # Análisis temporal avanzado
        analysis['temporal_analysis'] = self._advanced_temporal_analysis(accounts_data)
        
        progress_bar.progress(70)
        
        # Análisis de inactividad inteligente
        analysis['inactivity_patterns'] = self._intelligent_inactivity_analysis(accounts_data)
        
        progress_bar.progress(80)
        
        # Análisis de rendimiento de trading
        analysis['trading_performance'] = self._advanced_trading_performance(accounts_data)
        
        progress_bar.progress(90)
        
        # Métricas de riesgo avanzadas
        analysis['risk_metrics'] = self._calculate_advanced_risk_metrics(accounts_data, total_pnl, total_trades)
        
        # Alertas inteligentes mejoradas
        analysis['smart_alerts'] = self._generate_smart_alerts_advanced(analysis)
        
        # Insights predictivos
        analysis['predictive_insights'] = self._generate_predictive_insights(accounts_data, all_transactions)
        
        # Análisis comparativo
        analysis['comparative_analysis'] = self._comparative_analysis(accounts_data)
        
        progress_bar.progress(100)
        self.comprehensive_insights = analysis
        
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
                        
                        # Métricas adicionales de trading
                        if wins > 0 and losses > 0:
                            gross_profit = pnl_values[pnl_values > 0].sum()
                            gross_loss = abs(pnl_values[pnl_values < 0].sum())
                            analysis['profit_factor'] = gross_profit / gross_loss if gross_loss > 0 else 0
                            
                            # Expectancy
                            win_rate_decimal = wins / total
                            loss_rate_decimal = losses / total
                            avg_win = analysis['avg_win']
                            avg_loss = abs(analysis['avg_loss'])
                            analysis['expectancy'] = (win_rate_decimal * avg_win) - (loss_rate_decimal * avg_loss)
                        
                        # Análisis de rachas
                        positive_streak, negative_streak = self._calculate_streaks(pnl_values)
                        analysis['max_winning_streak'] = positive_streak
                        analysis['max_losing_streak'] = negative_streak
                        
                        # Análisis de drawdown
                        cumulative = pnl_values.cumsum()
                        running_max = cumulative.expanding().max()
                        drawdown = cumulative - running_max
                        analysis['max_drawdown'] = float(drawdown.min())
                        analysis['current_drawdown'] = float(drawdown.iloc[-1])
        
        # Análisis de activos avanzado
        asset_cols = [col for col in data.columns if any(word in col.lower() for word in ['asset', 'symbol', 'coin', 'currency', 'pair'])]
        if asset_cols:
            assets = data[asset_cols[0]].value_counts()
            analysis['assets'] = assets.to_dict()
            analysis['unique_assets'] = len(assets)
            analysis['most_traded_asset'] = assets.index[0] if len(assets) > 0 else None
            analysis['asset_concentration'] = (assets.iloc[0] / len(data)) * 100 if len(assets) > 0 else 0
        
        # Recopilar transacciones para análisis global
        analysis['all_transactions'] = []
        if amount_cols and date_cols:
            for idx, row in data.iterrows():
                try:
                    transaction = {
                        'date': pd.to_datetime(row[date_cols[0]]),
                        'amount': float(row[amount_cols[0]]),
                        'account': sheet_name
                    }
                    if type_cols:
                        transaction['type'] = str(row[type_cols[0]])
                    if asset_cols:
                        transaction['asset'] = str(row[asset_cols[0]])
                    analysis['all_transactions'].append(transaction)
                except:
                    continue
        
        return analysis
    
    def _calculate_streaks(self, values: pd.Series) -> Tuple[int, int]:
        """Calcular rachas de ganancias y pérdidas"""
        current_positive_streak = 0
        current_negative_streak = 0
        max_positive_streak = 0
        max_negative_streak = 0
        
        for value in values:
            if value > 0:
                current_positive_streak += 1
                current_negative_streak = 0
                max_positive_streak = max(max_positive_streak, current_positive_streak)
            elif value < 0:
                current_negative_streak += 1
                current_positive_streak = 0
                max_negative_streak = max(max_negative_streak, current_negative_streak)
            else:
                current_positive_streak = 0
                current_negative_streak = 0
        
        return max_positive_streak, max_negative_streak
    
    def _advanced_temporal_analysis(self, accounts_data: Dict) -> Dict:
        """🕐 Análisis temporal avanzado"""
        temporal_insights = {
            'global_activity_patterns': {},
            'seasonality_analysis': {},
            'time_performance_correlation': {}
        }
        
        all_dates = []
        hourly_performance = defaultdict(list)
        weekday_performance = defaultdict(list)
        monthly_performance = defaultdict(list)
        
        for account, data in accounts_data.items():
            if 'dates' in data and 'all_transactions' in data:
                all_dates.extend(data['dates'])
                
                for transaction in data['all_transactions']:
                    if 'date' in transaction and 'amount' in transaction:
                        date = transaction['date']
                        amount = transaction['amount']
                        
                        hourly_performance[date.hour].append(amount)
                        weekday_performance[date.strftime('%A')].append(amount)
                        monthly_performance[date.strftime('%B')].append(amount)
        
        if all_dates:
            dates_series = pd.Series(all_dates)
            
            # Análisis de patrones globales
            temporal_insights['global_activity_patterns'] = {
                'total_period_days': (dates_series.max() - dates_series.min()).days,
                'average_daily_transactions': len(all_dates) / max((dates_series.max() - dates_series.min()).days, 1),
                'most_active_day': dates_series.dt.day_name().mode().iloc[0] if len(dates_series) > 0 else None,
                'peak_hour': dates_series.dt.hour.mode().iloc[0] if len(dates_series) > 0 else None
            }
            
            # Análisis de estacionalidad
            if len(set(dates_series.dt.month)) > 1:
                monthly_activity = dates_series.dt.month.value_counts().sort_index()
                temporal_insights['seasonality_analysis'] = {
                    'seasonal_pattern': 'detected' if monthly_activity.std() > monthly_activity.mean() * 0.3 else 'stable',
                    'peak_season': monthly_activity.idxmax(),
                    'low_season': monthly_activity.idxmin()
                }
        
        return temporal_insights
    
    def _intelligent_inactivity_analysis(self, accounts_data: Dict) -> Dict:
        """🚫 Análisis inteligente de períodos de inactividad"""
        inactivity_insights = {
            'account_inactivity': {},
            'risk_assessment': {}
        }
        
        for account, data in accounts_data.items():
            if 'dates' in data and len(data['dates']) > 1:
                dates_sorted = sorted(data['dates'])
                gaps = []
                
                for i in range(1, len(dates_sorted)):
                    gap_days = (dates_sorted[i] - dates_sorted[i-1]).days
                    if gap_days > 3:  # Más de 3 días sin actividad
                        gaps.append({
                            'start_date': dates_sorted[i-1],
                            'end_date': dates_sorted[i],
                            'duration_days': gap_days,
                            'severity': 'critical' if gap_days > 30 else 'moderate' if gap_days > 7 else 'minor'
                        })
                
                if gaps:
                    max_gap = max(gap['duration_days'] for gap in gaps)
                    inactivity_insights['account_inactivity'][account] = {
                        'total_gaps': len(gaps),
                        'max_inactivity_days': max_gap,
                        'avg_inactivity_days': float(np.mean([gap['duration_days'] for gap in gaps])),
                        'gaps_detail': gaps,
                        'risk_level': 'high' if max_gap > 30 else 'medium' if max_gap > 7 else 'low'
                    }
        
        return inactivity_insights
    
    def _advanced_trading_performance(self, accounts_data: Dict) -> Dict:
        """🎯 Análisis avanzado de rendimiento de trading"""
        performance_insights = {
            'overall_metrics': {},
            'account_comparison': {}
        }
        
        total_trades = 0
        total_wins = 0
        total_pnl = 0
        account_performances = {}
        
        for account, data in accounts_data.items():
            if 'win_rate' in data:
                account_performances[account] = {
                    'win_rate': data.get('win_rate', 0),
                    'total_trades': data.get('total_trades', 0),
                    'pnl': data.get('pnl_total', 0),
                    'profit_factor': data.get('profit_factor', 0),
                    'max_drawdown': data.get('max_drawdown', 0),
                    'expectancy': data.get('expectancy', 0)
                }
                
                total_trades += data.get('total_trades', 0)
                total_wins += data.get('wins', 0)
                total_pnl += data.get('pnl_total', 0)
        
        if total_trades > 0:
            performance_insights['overall_metrics'] = {
                'global_win_rate': (total_wins / total_trades) * 100,
                'total_trades_all_accounts': total_trades,
                'total_pnl_all_accounts': total_pnl,
                'best_performing_account': max(account_performances.items(), key=lambda x: x[1]['pnl'])[0] if account_performances else None
            }
        
        performance_insights['account_comparison'] = account_performances
        return performance_insights
    
    def _calculate_advanced_risk_metrics(self, accounts_data: Dict, total_pnl: float, total_trades: int) -> Dict:
        """⚠️ Cálculo de métricas de riesgo avanzadas"""
        risk_metrics = {
            'portfolio_risk': {},
            'individual_risks': {}
        }
        
        all_pnl_values = []
        
        for account, data in accounts_data.items():
            if 'pnl_values' in data:
                pnl_values = data['pnl_values']
                all_pnl_values.extend(pnl_values)
                
                if len(pnl_values) > 1:
                    volatility = np.std(pnl_values)
                    mean_return = np.mean(pnl_values)
                    sharpe_ratio = mean_return / volatility if volatility > 0 else 0
                    
                    risk_metrics['individual_risks'][account] = {
                        'volatility': float(volatility),
                        'sharpe_ratio': float(sharpe_ratio),
                        'risk_level': 'high' if volatility > abs(mean_return) else 'low'
                    }
        
        if all_pnl_values:
            portfolio_volatility = np.std(all_pnl_values)
            portfolio_mean = np.mean(all_pnl_values)
            
            risk_metrics['portfolio_risk'] = {
                'total_portfolio_volatility': float(portfolio_volatility),
                'portfolio_sharpe_ratio': float(portfolio_mean / portfolio_volatility) if portfolio_volatility > 0 else 0
            }
        
        return risk_metrics
    
    def _generate_smart_alerts_advanced(self, analysis: Dict) -> List[str]:
        """🚨 Sistema de alertas inteligentes avanzado"""
        alerts = []
        
        # Alertas de rendimiento
        if 'trading_performance' in analysis:
            overall_metrics = analysis['trading_performance'].get('overall_metrics', {})
            global_win_rate = overall_metrics.get('global_win_rate', 0)
            total_pnl = overall_metrics.get('total_pnl_all_accounts', 0)
            
            if global_win_rate > 70:
                alerts.append(f"🏆 Excelente win rate global: {global_win_rate:.1f}%")
            elif global_win_rate < 40:
                alerts.append(f"⚠️ Win rate global bajo: {global_win_rate:.1f}% - Revisar estrategia")
            
            if total_pnl > 1000:
                alerts.append(f"💰 Rendimiento excepcional: +${total_pnl:,.2f}")
            elif total_pnl < -500:
                alerts.append(f"🔴 Pérdidas significativas: ${total_pnl:,.2f}")
        
        # Alertas de inactividad
        if 'inactivity_patterns' in analysis:
            for account, inactivity in analysis['inactivity_patterns'].get('account_inactivity', {}).items():
                if inactivity['risk_level'] == 'high':
                    alerts.append(f"⏰ {account}: Inactividad crítica ({inactivity['max_inactivity_days']} días)")
        
        return alerts
    
    def _generate_predictive_insights(self, accounts_data: Dict, all_transactions: List) -> Dict:
        """🔮 Generar insights predictivos"""
        predictive = {
            'trend_analysis': {},
            'recommendations': []
        }
        
        # Recomendaciones basadas en análisis
        for account, data in accounts_data.items():
            win_rate = data.get('win_rate', 0)
            max_drawdown = data.get('max_drawdown', 0)
            
            if win_rate < 50 and abs(max_drawdown) > 500:
                predictive['recommendations'].append(f"🎯 {account}: Considerar revisar estrategia - Win rate bajo y drawdown alto")
            elif win_rate > 70:
                predictive['recommendations'].append(f"✅ {account}: Estrategia efectiva - Mantener enfoque actual")
        
        return predictive
    
    def _comparative_analysis(self, accounts_data: Dict) -> Dict:
        """📊 Análisis comparativo entre cuentas"""
        comparative = {
            'performance_ranking': {},
            'diversification_score': 0
        }
        
        account_metrics = {}
        for account, data in accounts_data.items():
            if 'pnl_total' in data and 'win_rate' in data:
                account_metrics[account] = {
                    'pnl': data['pnl_total'],
                    'win_rate': data['win_rate'],
                    'total_trades': data.get('total_trades', 0)
                }
        
        if account_metrics:
            # Ranking por PnL
            ranked_by_pnl = sorted(account_metrics.items(), key=lambda x: x[1]['pnl'], reverse=True)
            comparative['performance_ranking'] = {
                'by_pnl': [{'account': acc, 'pnl': data['pnl']} for acc, data in ranked_by_pnl]
            }
        
        return comparative
        
        return analysis
    

# ============================================================================
# FUNCIONES DE VISUALIZACIÓN AVANZADA
# ============================================================================

def create_comprehensive_dashboard(analysis: Dict):
    """🚀 Dashboard Comprehensivo con IA Avanzada"""
    
    st.markdown('''
    <div class="main-header">
        <h1>🧠 Trading Analyzer Pro - IA Avanzada</h1>
        <p>Análisis inteligente de trading con insights predictivos</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Métricas principales mejoradas
    if 'trading_performance' in analysis:
        create_advanced_metrics_section(analysis)
    
    # Alertas inteligentes destacadas
    if 'smart_alerts' in analysis:
        create_smart_alerts_section(analysis)
    
    # Análisis de inactividad
    if 'inactivity_patterns' in analysis:
        create_inactivity_analysis_section(analysis)
    
    # Análisis temporal avanzado
    if 'temporal_analysis' in analysis:
        create_temporal_analysis_section(analysis)
    
    # Insights predictivos
    if 'predictive_insights' in analysis:
        create_predictive_insights_section(analysis)

def create_advanced_metrics_section(analysis: Dict):
    """📊 Sección de métricas avanzadas"""
    
    st.subheader("📊 Métricas de Rendimiento Avanzadas")
    
    performance = analysis.get('trading_performance', {})
    overall = performance.get('overall_metrics', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_pnl = overall.get('total_pnl_all_accounts', 0)
        st.markdown(f'''
        <div class="metric-premium">
            <h3>💰 PnL Total</h3>
            <h2>${total_pnl:,.2f}</h2>
            <p>{'📈 Positivo' if total_pnl >= 0 else '📉 Negativo'}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        global_win_rate = overall.get('global_win_rate', 0)
        color_class = "performance-excellent" if global_win_rate > 60 else "trading-insight" if global_win_rate > 40 else "inactivity-alert"
        st.markdown(f'''
        <div class="{color_class}">
            <h3>🎯 Win Rate Global</h3>
            <h2>{global_win_rate:.1f}%</h2>
            <p>{'🏆 Excelente' if global_win_rate > 60 else '⚖️ Balanceado' if global_win_rate > 40 else '⚠️ Bajo'}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        total_trades = overall.get('total_trades_all_accounts', 0)
        st.markdown(f'''
        <div class="metric-premium">
            <h3>🔄 Total Trades</h3>
            <h2>{total_trades:,}</h2>
            <p>Operaciones ejecutadas</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        best_account = overall.get('best_performing_account', 'N/A')
        st.markdown(f'''
        <div class="performance-excellent">
            <h3>🏆 Mejor Cuenta</h3>
            <h2>{best_account}</h2>
            <p>Mayor rendimiento</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Gráfico de rendimiento por cuenta
    if 'account_comparison' in performance:
        create_account_performance_chart(performance['account_comparison'])

def create_account_performance_chart(account_data: Dict):
    """📈 Gráfico de rendimiento por cuenta"""
    
    if not account_data:
        return
    
    # Preparar datos
    accounts = list(account_data.keys())
    pnl_values = [account_data[acc]['pnl'] for acc in accounts]
    win_rates = [account_data[acc]['win_rate'] for acc in accounts]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de PnL
        fig_pnl = go.Figure()
        
        colors = ['#00d2d3' if pnl > 0 else '#ff6b6b' for pnl in pnl_values]
        
        fig_pnl.add_trace(go.Bar(
            x=accounts,
            y=pnl_values,
            marker_color=colors,
            text=[f'${pnl:,.0f}' for pnl in pnl_values],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>PnL: $%{y:,.2f}<extra></extra>'
        ))
        
        fig_pnl.update_layout(
            title="💰 PnL por Cuenta",
            xaxis_title="Cuenta",
            yaxis_title="PnL (USDT)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            showlegend=False
        )
        
        fig_pnl.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        st.plotly_chart(fig_pnl, use_container_width=True)
    
    with col2:
        # Gráfico de Win Rate
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
            font=dict(color='#2c3e50'),
            showlegend=False
        )
        
        fig_wr.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5, annotation_text="Break Even")
        
        st.plotly_chart(fig_wr, use_container_width=True)

def create_smart_alerts_section(analysis: Dict):
    """🚨 Sección de alertas inteligentes"""
    
    st.subheader("🚨 Alertas Inteligentes")
    
    alerts = analysis.get('smart_alerts', [])
    
    if alerts:
        for alert in alerts:
            if "🏆" in alert or "💰" in alert or "📈" in alert:
                st.markdown(f'''
                <div class="alert-success">
                    <h4>{alert}</h4>
                </div>
                ''', unsafe_allow_html=True)
            elif "⚠️" in alert or "🔴" in alert:
                st.markdown(f'''
                <div class="alert-critical">
                    <h4>{alert}</h4>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="alert-warning">
                    <h4>{alert}</h4>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="alert-success">
            <h4>✅ No hay alertas críticas en este momento</h4>
        </div>
        ''', unsafe_allow_html=True)

def create_inactivity_analysis_section(analysis: Dict):
    """⏰ Sección de análisis de inactividad"""
    
    st.subheader("⏰ Análisis de Períodos de Inactividad")
    
    inactivity = analysis.get('inactivity_patterns', {})
    account_inactivity = inactivity.get('account_inactivity', {})
    
    if account_inactivity:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Resumen de Inactividad")
            
            for account, data in account_inactivity.items():
                risk_level = data['risk_level']
                max_gap = data['max_inactivity_days']
                total_gaps = data['total_gaps']
                
                risk_color = "inactivity-alert" if risk_level == 'high' else "trading-insight" if risk_level == 'medium' else "performance-excellent"
                
                st.markdown(f'''
                <div class="{risk_color}">
                    <h4>🏦 {account}</h4>
                    <p><strong>Máximo período inactivo:</strong> {max_gap} días</p>
                    <p><strong>Total de gaps:</strong> {total_gaps}</p>
                    <p><strong>Nivel de riesgo:</strong> {risk_level.upper()}</p>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            # Gráfico de inactividad
            accounts = list(account_inactivity.keys())
            max_gaps = [account_inactivity[acc]['max_inactivity_days'] for acc in accounts]
            
            fig_gaps = go.Figure()
            
            colors_gaps = ['#ff6b6b' if gap > 30 else '#feca57' if gap > 7 else '#00d2d3' for gap in max_gaps]
            
            fig_gaps.add_trace(go.Bar(
                x=accounts,
                y=max_gaps,
                marker_color=colors_gaps,
                text=[f'{gap}d' for gap in max_gaps],
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Máximo gap: %{y} días<extra></extra>'
            ))
            
            fig_gaps.update_layout(
                title="📊 Máximos Períodos de Inactividad",
                xaxis_title="Cuenta",
                yaxis_title="Días",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(fig_gaps, use_container_width=True)
    else:
        st.markdown('''
        <div class="performance-excellent">
            <h4>✅ Excelente actividad constante - No se detectaron períodos significativos de inactividad</h4>
        </div>
        ''', unsafe_allow_html=True)

def create_temporal_analysis_section(analysis: Dict):
    """🕐 Sección de análisis temporal"""
    
    st.subheader("🕐 Análisis Temporal Avanzado")
    
    temporal = analysis.get('temporal_analysis', {})
    global_patterns = temporal.get('global_activity_patterns', {})
    seasonality = temporal.get('seasonality_analysis', {})
    
    if global_patterns:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            most_active_day = global_patterns.get('most_active_day', 'N/A')
            st.markdown(f'''
            <div class="trading-insight">
                <h4>📅 Día Más Activo</h4>
                <h3>{most_active_day}</h3>
                <p>Mayor frecuencia de trading</p>
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
                <h4>📊 Período Total</h4>
                <h3>{total_period} días</h3>
                <p>Duración del análisis</p>
            </div>
            ''', unsafe_allow_html=True)
    
    if seasonality and 'seasonal_pattern' in seasonality:
        pattern = seasonality['seasonal_pattern']
        peak_season = seasonality.get('peak_season', 'N/A')
        low_season = seasonality.get('low_season', 'N/A')
        
        st.markdown(f'''
        <div class="insight-card">
            <h4>🌟 Análisis de Estacionalidad</h4>
            <p><strong>Patrón detectado:</strong> {pattern}</p>
            <p><strong>Temporada alta:</strong> Mes {peak_season}</p>
            <p><strong>Temporada baja:</strong> Mes {low_season}</p>
        </div>
        ''', unsafe_allow_html=True)

def create_predictive_insights_section(analysis: Dict):
    """🔮 Sección de insights predictivos"""
    
    st.subheader("🔮 Insights Predictivos con IA")
    
    predictive = analysis.get('predictive_insights', {})
    recommendations = predictive.get('recommendations', [])
    
    if recommendations:
        st.markdown("### 🎯 Recomendaciones Inteligentes")
        
        for recommendation in recommendations:
            if "✅" in recommendation:
                st.markdown(f'''
                <div class="performance-excellent">
                    <h4>{recommendation}</h4>
                </div>
                ''', unsafe_allow_html=True)
            elif "🎯" in recommendation:
                st.markdown(f'''
                <div class="inactivity-alert">
                    <h4>{recommendation}</h4>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="trading-insight">
                    <h4>{recommendation}</h4>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="performance-excellent">
            <h4>✅ Todas las cuentas muestran patrones de trading saludables</h4>
        </div>
        ''', unsafe_allow_html=True)

def create_advanced_risk_analysis(analysis: Dict):
    """⚠️ Análisis avanzado de riesgo"""
    
    st.subheader("⚠️ Análisis de Riesgo Avanzado")
    
    risk_metrics = analysis.get('risk_metrics', {})
    portfolio_risk = risk_metrics.get('portfolio_risk', {})
    individual_risks = risk_metrics.get('individual_risks', {})
    
    if portfolio_risk:
        col1, col2 = st.columns(2)
        
        with col1:
            volatility = portfolio_risk.get('total_portfolio_volatility', 0)
            sharpe = portfolio_risk.get('portfolio_sharpe_ratio', 0)
            
            st.markdown(f'''
            <div class="metric-premium">
                <h4>📊 Riesgo de Cartera</h4>
                <p><strong>Volatilidad:</strong> {volatility:.2f}</p>
                <p><strong>Ratio Sharpe:</strong> {sharpe:.2f}</p>
                <p><strong>Clasificación:</strong> {'🟢 Bajo' if sharpe > 1 else '🟡 Medio' if sharpe > 0.5 else '🔴 Alto'}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            if individual_risks:
                st.markdown("### 🏦 Riesgo por Cuenta")
                for account, risk_data in individual_risks.items():
                    risk_level = risk_data.get('risk_level', 'unknown')
                    sharpe_individual = risk_data.get('sharpe_ratio', 0)
                    
                    color_class = "performance-excellent" if risk_level == 'low' else "inactivity-alert"
                    
                    st.markdown(f'''
                    <div class="{color_class}">
                        <h5>{account}</h5>
                        <p>Sharpe: {sharpe_individual:.2f} | Riesgo: {risk_level.upper()}</p>
                    </div>
                    ''', unsafe_allow_html=True)

def create_comprehensive_report(analysis: Dict) -> str:
    """📄 Generar reporte comprehensivo"""
    
    report = "🧠 TRADING ANALYZER PRO - REPORTE IA AVANZADO\n"
    report += "=" * 80 + "\n"
    report += f"📅 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Resumen ejecutivo
    if 'trading_performance' in analysis:
        performance = analysis['trading_performance']
        overall = performance.get('overall_metrics', {})
        
        report += "💼 RESUMEN EJECUTIVO\n"
        report += "-" * 40 + "\n"
        report += f"PnL Total: ${overall.get('total_pnl_all_accounts', 0):,.2f}\n"
        report += f"Win Rate Global: {overall.get('global_win_rate', 0):.1f}%\n"
        report += f"Total Trades: {overall.get('total_trades_all_accounts', 0):,}\n"
        report += f"Mejor Cuenta: {overall.get('best_performing_account', 'N/A')}\n\n"
    
    # Alertas críticas
    if 'smart_alerts' in analysis:
        alerts = analysis['smart_alerts']
        if alerts:
            report += "🚨 ALERTAS CRÍTICAS\n"
            report += "-" * 30 + "\n"
            for alert in alerts:
                report += f"• {alert}\n"
            report += "\n"
    
    # Análisis de inactividad
    if 'inactivity_patterns' in analysis:
        inactivity = analysis['inactivity_patterns']
        account_inactivity = inactivity.get('account_inactivity', {})
        
        if account_inactivity:
            report += "⏰ ANÁLISIS DE INACTIVIDAD\n"
            report += "-" * 35 + "\n"
            for account, data in account_inactivity.items():
                report += f"{account}:\n"
                report += f"  Máximo período inactivo: {data['max_inactivity_days']} días\n"
                report += f"  Nivel de riesgo: {data['risk_level'].upper()}\n"
                report += f"  Total gaps: {data['total_gaps']}\n\n"
    
    # Recomendaciones
    if 'predictive_insights' in analysis:
        recommendations = analysis['predictive_insights'].get('recommendations', [])
        if recommendations:
            report += "🎯 RECOMENDACIONES IA\n"
            report += "-" * 30 + "\n"
            for rec in recommendations:
                report += f"• {rec}\n"
            report += "\n"
    
    return report

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """🚀 Función principal mejorada"""
    
    # Sidebar avanzado
    st.sidebar.markdown("## 🧠 Control Panel IA")
    st.sidebar.markdown("---")
    
    # Inicializar analizador
    analyzer = AdvancedTradingAnalyzer()
    
    # Sección de carga de archivos mejorada
    st.sidebar.markdown("### 📁 Cargar Archivo de Trading")
    uploaded_file = st.sidebar.file_uploader(
        "Arrastra tu archivo Excel o CSV",
        type=['xlsx', 'xls', 'csv'],
        help="Soporta archivos de BingX, Binance, y otros exchanges"
    )
    
    # Botón manual para analizar
    analyze_button = st.sidebar.button("🚀 Analizar Archivo", type="primary", disabled=(uploaded_file is None))
    
    # Procesar archivo automáticamente o con botón
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
        
        # Mostrar info del archivo cargado
        st.sidebar.success(f"📄 **{uploaded_file.name}**")
        st.sidebar.info(f"📏 Tamaño: {uploaded_file.size / 1024:.1f} KB")
    
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
        
        st.success(f"📊 **Análisis activo**: {file_name}")
        st.markdown("---")
        
        # Opciones del sidebar
        st.sidebar.markdown("### 📊 Secciones de Análisis")
        show_dashboard = st.sidebar.checkbox("🚀 Dashboard Principal", value=True)
        show_inactivity = st.sidebar.checkbox("⏰ Análisis de Inactividad", value=True)
        show_temporal = st.sidebar.checkbox("🕐 Análisis Temporal", value=True)
        show_risk = st.sidebar.checkbox("⚠️ Análisis de Riesgo", value=True)
        show_predictions = st.sidebar.checkbox("🔮 Insights Predictivos", value=True)
        
        # Renderizar secciones
        if show_dashboard:
            create_comprehensive_dashboard(analysis)
            st.markdown("---")
        
        if show_inactivity:
            create_inactivity_analysis_section(analysis)
            st.markdown("---")
        
        if show_temporal:
            create_temporal_analysis_section(analysis)
            st.markdown("---")
        
        if show_risk:
            create_advanced_risk_analysis(analysis)
            st.markdown("---")
        
        if show_predictions:
            create_predictive_insights_section(analysis)
        
        # Exportación avanzada
        st.sidebar.markdown("### 📄 Exportar Análisis")
        if st.sidebar.button("📥 Generar Reporte IA"):
            report_content = create_comprehensive_report(analysis)
            st.sidebar.download_button(
                label="💾 Descargar Reporte Completo",
                data=report_content,
                file_name=f"trading_ai_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        # Botón para limpiar análisis
        st.sidebar.markdown("### 🔄 Nuevo Análisis")
        if st.sidebar.button("🗑️ Limpiar y Empezar de Nuevo", type="secondary"):
            # Limpiar session state
            for key in ['analysis', 'analyzer', 'current_file']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    elif uploaded_file is not None:
        # Archivo subido pero no analizado
        st.info("📄 Archivo cargado. Presiona '🚀 Analizar Archivo' para comenzar el análisis.")
    
    else:
        # Pantalla de bienvenida mejorada
        st.markdown('''
        <div class="main-header">
            <h1>🧠 Trading Analyzer Pro - IA Avanzada</h1>
            <p>Análisis inteligente de trading con machine learning</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("""
        ## 🎯 Funcionalidades IA Avanzadas
        
        ### 🧠 Análisis Inteligente
        ✅ **Detección automática de patrones** de trading  
        ✅ **Win Rate calculation avanzado** con análisis por tipo  
        ✅ **Períodos de inactividad inteligentes** con severidad  
        ✅ **Análisis temporal profundo** (estacionalidad, tendencias)  
        ✅ **Métricas de riesgo avanzadas** (Sharpe, VaR, drawdown)  
        
        ### 🚨 Sistema de Alertas IA
        ✅ **Alertas predictivas** basadas en patrones  
        ✅ **Detección de anomalías** en rendimiento  
        ✅ **Recomendaciones automáticas** de estrategia  
        ✅ **Evaluación de riesgo dinámica**  
        
        ### 📊 Visualizaciones Avanzadas
        ✅ **Gráficos interactivos** con insights automáticos  
        ✅ **Heatmaps temporales** de actividad  
        ✅ **Análisis comparativo** entre cuentas  
        ✅ **Dashboards predictivos** con IA  
        
        ### 🔮 Insights Predictivos
        ✅ **Análisis de tendencias** con machine learning  
        ✅ **Predicción de rendimiento** basada en patrones  
        ✅ **Recomendaciones personalizadas** por cuenta  
        ✅ **Evaluación de consistencia** algorítmica  
        
        ### 📄 Reportes Comprehensivos
        ✅ **Reportes con IA** más detallados que la versión local  
        ✅ **Exportación avanzada** con insights automáticos  
        ✅ **Análisis comparativo** temporal  
        ✅ **Recomendaciones accionables**  
        
        ---
        
        ## 🚀 ¡VERSIÓN MEJORADA!
        
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

if __name__ == "__main__":
    main()

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

# ============================================================================
# FUNCIÓN PRINCIPAL (ÚNICA)
# ============================================================================

if __name__ == "__main__":
    main()