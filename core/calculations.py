"""
🔢 Trading Analyzer Pro - Financial Calculations
Módulo para cálculos financieros y métricas de trading
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.settings import PNL_KEYWORDS, DATE_KEYWORDS, TYPE_KEYWORDS, AMOUNT_KEYWORDS, TRADING_KEYWORDS
except ImportError:
    # Fallback for direct execution
    PNL_KEYWORDS = ['realized_pnl', 'realized pnl', 'pnl', 'profit_loss', 'net_profit', 'amount']
    DATE_KEYWORDS = ['time', 'date', 'utc', 'timestamp']
    TYPE_KEYWORDS = ['type', 'side', 'action', 'operation']
    AMOUNT_KEYWORDS = ['amount', 'pnl', 'balance', 'profit', 'loss', 'realized', 'unrealized', 'total', 'net']
    TRADING_KEYWORDS = ['realized', 'pnl', 'fee', 'trade', 'buy', 'sell', 'long', 'short', 'open', 'close']

class FinancialCalculator:
    """💰 Calculadora de métricas financieras avanzadas"""
    
    @staticmethod
    def analyze_sheet(data: pd.DataFrame, sheet_name: str) -> Dict:
        """
        Análizar una hoja de datos y extraer métricas financieras
        
        Args:
            data: DataFrame con datos de trading
            sheet_name: Nombre de la hoja
            
        Returns:
            Dict con análisis completo
        """
        analysis = {
            'sheet_name': sheet_name,
            'raw_transactions': len(data),
            'all_transactions': []
        }
        
        # Análisis temporal
        analysis.update(FinancialCalculator._analyze_temporal_data(data))
        
        # Análisis financiero principal
        analysis.update(FinancialCalculator._analyze_financial_data(data))
        
        # Análisis de tipos de transacción
        analysis.update(FinancialCalculator._analyze_transaction_types(data))
        
        # Análisis de trading específico
        analysis.update(FinancialCalculator._analyze_trading_performance(data))
        
        return analysis
    
    @staticmethod
    def _analyze_temporal_data(data: pd.DataFrame) -> Dict:
        """Análisis temporal de los datos"""
        temporal_analysis = {}
        
        # Buscar columnas de fecha
        date_cols = [col for col in data.columns 
                    if any(word in col.lower() for word in DATE_KEYWORDS)]
        
        if date_cols:
            try:
                dates = pd.to_datetime(data[date_cols[0]])
                temporal_analysis.update({
                    'dates': dates.tolist(),
                    'period_days': (dates.max() - dates.min()).days,
                    'first_transaction': dates.min(),
                    'last_transaction': dates.max(),
                    'transaction_frequency': len(data) / max((dates.max() - dates.min()).days, 1)
                })
                
                # Análisis de actividad por día de la semana
                weekday_activity = dates.dt.day_name().value_counts()
                temporal_analysis.update({
                    'most_active_weekday': weekday_activity.index[0],
                    'weekday_distribution': weekday_activity.to_dict()
                })
                
                # Análisis horario
                if hasattr(dates.dt, 'hour'):
                    hourly_activity = dates.dt.hour.value_counts().sort_index()
                    peak_hour = hourly_activity.idxmax()
                    temporal_analysis.update({
                        'peak_trading_hour': f"{peak_hour}:00",
                        'hourly_distribution': hourly_activity.to_dict()
                    })
                
                # Análisis mensual
                monthly_activity = dates.dt.to_period('M').value_counts().sort_index()
                if len(monthly_activity) > 0:
                    temporal_analysis.update({
                        'most_active_month': str(monthly_activity.idxmax()),
                        'monthly_activity': {str(k): v for k, v in monthly_activity.to_dict().items()}
                    })
                    
                    # Tendencia mensual
                    if len(monthly_activity) > 1:
                        monthly_trend = np.polyfit(range(len(monthly_activity)), monthly_activity.values, 1)[0]
                        temporal_analysis.update({
                            'monthly_trend': 'increasing' if monthly_trend > 0 else 'decreasing',
                            'trend_strength': abs(monthly_trend)
                        })
                        
            except Exception as e:
                print(f"⚠️ Error en análisis temporal para {data}: {e}")
        
        return temporal_analysis
    
    @staticmethod
    def _analyze_financial_data(data: pd.DataFrame) -> Dict:
        """Análisis financiero principal - MEJORADO para coincidencia exacta"""
        financial_analysis = {}
        
        # Buscar columnas de montos
        amount_cols = [col for col in data.columns 
                      if any(word in col.lower() for word in AMOUNT_KEYWORDS)]
        
        # Detectar columna principal de PnL (prioridad específica)
        main_pnl_col = FinancialCalculator._detect_main_pnl_column(data, amount_cols)
        
        if main_pnl_col:
            values = data[main_pnl_col].dropna()
            if len(values) > 0:
                financial_analysis.update(FinancialCalculator._calculate_pnl_metrics(values, main_pnl_col))
        
        # Procesar todas las columnas numéricas para estadísticas adicionales
        for col in amount_cols:
            if data[col].dtype in ['float64', 'int64']:
                values = data[col].dropna()
                if len(values) > 0:
                    financial_analysis.update({
                        f'{col}_total': float(values.sum()),
                        f'{col}_mean': float(values.mean()),
                        f'{col}_median': float(values.median()),
                        f'{col}_std': float(values.std()),
                        f'{col}_min': float(values.min()),
                        f'{col}_max': float(values.max())
                    })
        
        return financial_analysis
    
    @staticmethod
    def _detect_main_pnl_column(data: pd.DataFrame, amount_cols: List[str]) -> Optional[str]:
        """Detectar la columna principal de PnL"""
        # Prioridad específica para detectar PnL
        for keyword in PNL_KEYWORDS:
            for col in data.columns:
                if keyword.replace('_', ' ').lower() in col.lower():
                    return col
        
        # Si no se encontró columna específica, usar la primera columna numérica realista
        for col in amount_cols:
            if data[col].dtype in ['float64', 'int64']:
                values = data[col].dropna()
                if len(values) > 0 and (values.abs().max() > 0.01):  # Valores realistas
                    return col
        
        return None
    
    @staticmethod
    def _calculate_pnl_metrics(values: pd.Series, column_name: str) -> Dict:
        """Calcular métricas de PnL completas"""
        total_pnl = float(values.sum())
        profits = values[values > 0]
        losses = values[values < 0]
        
        metrics = {
            'pnl_total': total_pnl,
            'pnl_mean': float(values.mean()),
            'pnl_median': float(values.median()),
            'pnl_std': float(values.std()),
            'pnl_min': float(values.min()),
            'pnl_max': float(values.max()),
            'pnl_values': values.tolist(),
            'main_pnl_column': column_name,
            
            # Información detallada de ganancias y pérdidas
            'total_profit': float(profits.sum()) if len(profits) > 0 else 0,
            'total_loss': float(losses.sum()) if len(losses) > 0 else 0,
            'gross_profit': float(profits.sum()) if len(profits) > 0 else 0,
            'gross_loss': float(abs(losses.sum())) if len(losses) > 0 else 0,
            
            # Contadores
            'profitable_trades': len(profits),
            'losing_trades': len(losses),
            'neutral_trades': len(values[values == 0]),
            
            # Promedios
            'avg_profit': float(profits.mean()) if len(profits) > 0 else 0,
            'avg_loss': float(losses.mean()) if len(losses) > 0 else 0,
        }
        
        # Análisis de rachas
        positive_streak, negative_streak = FinancialCalculator._calculate_streaks(values)
        metrics.update({
            'max_winning_streak': positive_streak,
            'max_losing_streak': negative_streak
        })
        
        # Análisis de drawdown
        cumulative = values.cumsum()
        running_max = cumulative.expanding().max()
        drawdown = cumulative - running_max
        metrics.update({
            'max_drawdown': float(drawdown.min()),
            'current_drawdown': float(drawdown.iloc[-1])
        })
        
        return metrics
    
    @staticmethod
    def _analyze_transaction_types(data: pd.DataFrame) -> Dict:
        """Análisis de tipos de transacción"""
        type_analysis = {}
        
        type_cols = [col for col in data.columns 
                    if any(word in col.lower() for word in TYPE_KEYWORDS)]
        
        if type_cols:
            types = data[type_cols[0]].value_counts()
            type_analysis.update({
                'transaction_types': types.to_dict(),
                'unique_transaction_types': len(types)
            })
        
        return type_analysis
    
    @staticmethod
    def _analyze_trading_performance(data: pd.DataFrame) -> Dict:
        """Análisis específico de rendimiento de trading"""
        trading_analysis = {}
        
        type_cols = [col for col in data.columns 
                    if any(word in col.lower() for word in TYPE_KEYWORDS)]
        amount_cols = [col for col in data.columns 
                      if any(word in col.lower() for word in AMOUNT_KEYWORDS)]
        
        if type_cols and amount_cols:
            # Filtrar datos de trading
            trading_mask = data[type_cols[0]].str.contains(
                '|'.join(TRADING_KEYWORDS), case=False, na=False
            )
            trading_data = data[trading_mask]
            
            if not trading_data.empty:
                pnl_values = trading_data[amount_cols[0]].dropna()
                if len(pnl_values) > 0:
                    wins = (pnl_values > 0).sum()
                    losses = (pnl_values < 0).sum()
                    neutral = (pnl_values == 0).sum()
                    total = len(pnl_values)
                    
                    trading_analysis.update({
                        'total_trades': len(trading_data),
                        'trading_percentage': (len(trading_data) / len(data)) * 100,
                        'win_rate': (wins / total) * 100 if total > 0 else 0,
                        'loss_rate': (losses / total) * 100 if total > 0 else 0,
                        'neutral_rate': (neutral / total) * 100 if total > 0 else 0,
                        'total_wins': int(wins),
                        'total_losses': int(losses),
                        'total_neutral': int(neutral)
                    })
                    
                    # Profit factor
                    gross_profit = pnl_values[pnl_values > 0].sum()
                    gross_loss = abs(pnl_values[pnl_values < 0].sum())
                    if gross_loss > 0:
                        trading_analysis['profit_factor'] = gross_profit / gross_loss
                    else:
                        trading_analysis['profit_factor'] = float('inf') if gross_profit > 0 else 0
                    
                    # Expectancy
                    if total > 0:
                        trading_analysis['expectancy'] = pnl_values.mean()
        
        return trading_analysis
    
    @staticmethod
    def _calculate_streaks(values: pd.Series) -> Tuple[int, int]:
        """
        Calcular rachas de ganancias y pérdidas consecutivas
        
        Returns:
            Tuple[int, int]: (max_winning_streak, max_losing_streak)
        """
        if len(values) == 0:
            return 0, 0
        
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
    
    @staticmethod
    def calculate_portfolio_metrics(account_analyses: Dict[str, Dict]) -> Dict:
        """
        Calcular métricas del portafolio completo
        
        Args:
            account_analyses: Dict con análisis de cada cuenta
            
        Returns:
            Dict con métricas del portafolio
        """
        portfolio_metrics = {
            'total_accounts': len(account_analyses),
            'total_pnl_all_accounts': 0,
            'total_trades_all_accounts': 0,
            'profitable_accounts': 0,
            'losing_accounts': 0,
            'account_pnls': {},
            'account_win_rates': {},
            'best_performing_account': None,
            'worst_performing_account': None
        }
        
        # Calcular métricas agregadas
        all_win_rates = []
        account_pnls = {}
        
        for account, analysis in account_analyses.items():
            pnl = analysis.get('pnl_total', 0)
            portfolio_metrics['total_pnl_all_accounts'] += pnl
            portfolio_metrics['total_trades_all_accounts'] += analysis.get('total_trades', 0)
            
            if pnl > 0:
                portfolio_metrics['profitable_accounts'] += 1
            elif pnl < 0:
                portfolio_metrics['losing_accounts'] += 1
            
            account_pnls[account] = pnl
            
            win_rate = analysis.get('win_rate', 0)
            if win_rate > 0:
                all_win_rates.append(win_rate)
            portfolio_metrics['account_win_rates'][account] = win_rate
        
        # Mejores y peores cuentas
        if account_pnls:
            portfolio_metrics['best_performing_account'] = max(account_pnls, key=account_pnls.get)
            portfolio_metrics['worst_performing_account'] = min(account_pnls, key=account_pnls.get)
            portfolio_metrics['account_pnls'] = account_pnls
        
        # Win rate global
        if all_win_rates:
            portfolio_metrics['global_win_rate'] = np.mean(all_win_rates)
        else:
            portfolio_metrics['global_win_rate'] = 0
        
        return portfolio_metrics