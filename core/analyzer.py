"""
🧠 Trading Analyzer Pro - Main Analyzer
Clase principal del analizador de trading con IA avanzada
"""

import streamlit as st
from typing import Dict, Any
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.data_loader import DataLoader
    from core.calculations import FinancialCalculator
    from config.settings import WIN_RATE_THRESHOLDS, PNL_THRESHOLDS
except ImportError:
    # Fallback imports for different environments
    from .data_loader import DataLoader
    from .calculations import FinancialCalculator
    try:
        from config.settings import WIN_RATE_THRESHOLDS, PNL_THRESHOLDS
    except ImportError:
        WIN_RATE_THRESHOLDS = {"excellent": 70, "good": 50, "poor": 40}
        PNL_THRESHOLDS = {"significant_profit": 1000, "significant_loss": -500}

class AdvancedTradingAnalyzer:
    """🚀 Analizador de Trading Avanzado con IA - Versión Modular"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.financial_calculator = FinancialCalculator()
        self.analysis_results = {}
        self.comprehensive_insights = {}
        
    def load_data_from_upload(self, uploaded_file) -> bool:
        """
        Cargar datos desde archivo subido
        
        Args:
            uploaded_file: Archivo subido por Streamlit
            
        Returns:
            bool: True si la carga fue exitosa
        """
        return self.data_loader.load_from_upload(uploaded_file)
    
    def generate_comprehensive_analysis(self) -> Dict[str, Any]:
        """
        🧠 ANÁLISIS COMPREHENSIVO MEJORADO CON IA AVANZADA
        
        Returns:
            Dict con análisis completo
        """
        sheets = self.data_loader.get_sheets()
        if not sheets:
            return {}
        
        st.info("🧠 Ejecutando análisis con IA avanzada...")
        progress_bar = st.progress(0)
        
        analysis = {
            'financial_insights': {},
            'temporal_analysis': {},
            'inactivity_patterns': {},
            'trading_performance': {},
            'risk_metrics': {},
            'predictive_insights': {},
            'smart_alerts': [],
            'comprehensive_summary': {},
            'metadata': self.data_loader.get_metadata()
        }
        
        try:
            # Análisis por hoja
            progress_bar.progress(20)
            financial_summary = {}
            
            for i, (sheet_name, data) in enumerate(sheets.items()):
                sheet_analysis = self.financial_calculator.analyze_sheet(data, sheet_name)
                financial_summary[sheet_name] = sheet_analysis
                progress_bar.progress(20 + (i + 1) * 30 // len(sheets))
            
            analysis['financial_summary'] = financial_summary
            
            # Análisis de rendimiento del portafolio
            progress_bar.progress(60)
            portfolio_metrics = self.financial_calculator.calculate_portfolio_metrics(financial_summary)
            analysis['trading_performance'] = {
                'overall_metrics': portfolio_metrics,
                'account_comparison': self._create_account_comparison(financial_summary)
            }
            
            # Análisis temporal global
            progress_bar.progress(70)
            analysis['temporal_analysis'] = self._analyze_global_temporal_patterns(financial_summary)
            
            # Análisis de patrones de inactividad
            progress_bar.progress(80)
            analysis['inactivity_patterns'] = self._analyze_inactivity_patterns(financial_summary)
            
            # Métricas de riesgo
            progress_bar.progress(85)
            analysis['risk_metrics'] = self._calculate_risk_metrics(financial_summary)
            
            # Insights predictivos con IA
            progress_bar.progress(90)
            analysis['predictive_insights'] = self._generate_predictive_insights(analysis)
            
            # Alertas inteligentes
            progress_bar.progress(95)
            analysis['smart_alerts'] = self._generate_smart_alerts(analysis)
            
            progress_bar.progress(100)
            st.success("✅ Análisis completado con éxito!")
            
            progress_bar.empty()
            return analysis
            
        except Exception as e:
            st.error(f"❌ Error durante el análisis: {str(e)}")
            progress_bar.empty()
            return {}
    
    def _create_account_comparison(self, financial_summary: Dict) -> Dict:
        """Crear comparación detallada entre cuentas"""
        comparison = {}
        
        for account, data in financial_summary.items():
            comparison[account] = {
                'pnl': data.get('pnl_total', 0),
                'win_rate': data.get('win_rate', 0),
                'total_trades': data.get('total_trades', 0),
                'profit_factor': data.get('profit_factor', 0),
                'max_drawdown': data.get('max_drawdown', 0),
                'expectancy': data.get('expectancy', 0),
                'total_profit': data.get('total_profit', 0),
                'total_loss': data.get('total_loss', 0),
                'avg_profit': data.get('avg_profit', 0),
                'avg_loss': data.get('avg_loss', 0)
            }
        
        return comparison
    
    def _analyze_global_temporal_patterns(self, financial_summary: Dict) -> Dict:
        """Analizar patrones temporales globales"""
        temporal_analysis = {
            'global_activity_patterns': {},
            'seasonality_analysis': {},
            'trend_analysis': {}
        }
        
        all_dates = []
        all_weekdays = []
        all_hours = []
        
        for account, data in financial_summary.items():
            if 'dates' in data:
                all_dates.extend(data['dates'])
            if 'weekday_distribution' in data:
                all_weekdays.extend(data['weekday_distribution'].keys())
            if 'hourly_distribution' in data:
                all_hours.extend(data['hourly_distribution'].keys())
        
        if all_dates:
            import pandas as pd
            dates_series = pd.to_datetime(all_dates)
            temporal_analysis['global_activity_patterns'] = {
                'total_period_days': (dates_series.max() - dates_series.min()).days,
                'most_active_day': dates_series.dt.day_name().mode().iloc[0] if len(dates_series) > 0 else 'N/A',
                'peak_hour': dates_series.dt.hour.mode().iloc[0] if len(dates_series) > 0 else 'N/A'
            }
        
        return temporal_analysis
    
    def _analyze_inactivity_patterns(self, financial_summary: Dict) -> Dict:
        """Analizar patrones de inactividad"""
        inactivity_analysis = {
            'account_inactivity': {},
            'global_gaps': [],
            'severity_assessment': 'low'
        }
        
        high_risk_accounts = 0
        
        for account, data in financial_summary.items():
            if 'dates' in data and len(data['dates']) > 1:
                import pandas as pd
                dates = pd.to_datetime(data['dates']).sort_values()
                gaps = dates.diff().dt.days.dropna()
                
                if len(gaps) > 0:
                    max_gap = gaps.max()
                    avg_gap = gaps.mean()
                    
                    # Determinar nivel de riesgo
                    if max_gap > 30:
                        risk_level = 'high'
                        high_risk_accounts += 1
                    elif max_gap > 7:
                        risk_level = 'medium'
                    else:
                        risk_level = 'low'
                    
                    inactivity_analysis['account_inactivity'][account] = {
                        'max_inactivity_days': int(max_gap),
                        'avg_inactivity_days': float(avg_gap),
                        'total_gaps': len(gaps),
                        'risk_level': risk_level
                    }
        
        # Evaluación global de severidad
        total_accounts = len(financial_summary)
        if high_risk_accounts > total_accounts * 0.5:
            inactivity_analysis['severity_assessment'] = 'high'
        elif high_risk_accounts > 0:
            inactivity_analysis['severity_assessment'] = 'medium'
        
        return inactivity_analysis
    
    def _calculate_risk_metrics(self, financial_summary: Dict) -> Dict:
        """Calcular métricas de riesgo del portafolio"""
        import numpy as np
        
        risk_metrics = {
            'portfolio_risk': {},
            'individual_risks': {}
        }
        
        all_pnls = []
        individual_sharpes = {}
        
        for account, data in financial_summary.items():
            pnl_values = data.get('pnl_values', [])
            if len(pnl_values) > 1:
                pnl_array = np.array(pnl_values)
                volatility = np.std(pnl_array)
                mean_return = np.mean(pnl_array)
                
                # Sharpe ratio simplificado
                sharpe_ratio = mean_return / volatility if volatility > 0 else 0
                individual_sharpes[account] = sharpe_ratio
                
                risk_level = 'low' if sharpe_ratio > 1 else 'medium' if sharpe_ratio > 0.5 else 'high'
                
                risk_metrics['individual_risks'][account] = {
                    'volatility': float(volatility),
                    'sharpe_ratio': float(sharpe_ratio),
                    'risk_level': risk_level
                }
                
                all_pnls.extend(pnl_values)
        
        # Métricas del portafolio
        if all_pnls:
            portfolio_array = np.array(all_pnls)
            portfolio_volatility = np.std(portfolio_array)
            portfolio_mean = np.mean(portfolio_array)
            portfolio_sharpe = portfolio_mean / portfolio_volatility if portfolio_volatility > 0 else 0
            
            risk_metrics['portfolio_risk'] = {
                'total_portfolio_volatility': float(portfolio_volatility),
                'portfolio_sharpe_ratio': float(portfolio_sharpe),
                'portfolio_risk_level': 'low' if portfolio_sharpe > 1 else 'medium' if portfolio_sharpe > 0.5 else 'high'
            }
        
        return risk_metrics
    
    def _generate_predictive_insights(self, analysis: Dict) -> Dict:
        """Generar insights predictivos con IA"""
        insights = {
            'performance_prediction': 'stable',
            'recommendations': [],
            'growth_potential': 'medium',
            'risk_assessment': 'medium'
        }
        
        trading_performance = analysis.get('trading_performance', {})
        overall_metrics = trading_performance.get('overall_metrics', {})
        
        total_pnl = overall_metrics.get('total_pnl_all_accounts', 0)
        global_win_rate = overall_metrics.get('global_win_rate', 0)
        
        # Generar recomendaciones basadas en métricas
        if total_pnl > PNL_THRESHOLDS['significant_profit']:
            insights['recommendations'].append("✅ Excelente rendimiento: Considera aumentar el capital de trading")
            insights['performance_prediction'] = 'bullish'
            insights['growth_potential'] = 'high'
        elif total_pnl < PNL_THRESHOLDS['significant_loss']:
            insights['recommendations'].append("🎯 Revisa tu estrategia: Las pérdidas requieren ajustes")
            insights['performance_prediction'] = 'bearish'
            insights['risk_assessment'] = 'high'
        
        if global_win_rate < WIN_RATE_THRESHOLDS['poor']:
            insights['recommendations'].append("🎯 Win rate bajo: Considera revisar puntos de entrada y salida")
        elif global_win_rate > WIN_RATE_THRESHOLDS['excellent']:
            insights['recommendations'].append("✅ Excelente win rate: Mantén la estrategia actual")
        
        return insights
    
    def _generate_smart_alerts(self, analysis: Dict) -> list:
        """Generar alertas inteligentes basadas en el análisis"""
        alerts = []
        
        trading_performance = analysis.get('trading_performance', {})
        overall_metrics = trading_performance.get('overall_metrics', {})
        inactivity = analysis.get('inactivity_patterns', {})
        risk_metrics = analysis.get('risk_metrics', {})
        
        # Alertas de rendimiento
        total_pnl = overall_metrics.get('total_pnl_all_accounts', 0)
        if total_pnl < PNL_THRESHOLDS['significant_loss']:
            alerts.append("🚨 ALERTA: Pérdidas significativas detectadas")
        
        global_win_rate = overall_metrics.get('global_win_rate', 0)
        if global_win_rate < WIN_RATE_THRESHOLDS['poor']:
            alerts.append("⚠️ ALERTA: Win rate global por debajo del 40%")
        
        # Alertas de inactividad
        severity = inactivity.get('severity_assessment', 'low')
        if severity == 'high':
            alerts.append("⏰ ALERTA: Múltiples cuentas con períodos de inactividad prolongados")
        
        # Alertas de riesgo
        portfolio_risk = risk_metrics.get('portfolio_risk', {})
        if portfolio_risk.get('portfolio_risk_level') == 'high':
            alerts.append("⚠️ ALERTA: Alto nivel de riesgo en el portafolio")
        
        return alerts
    
    def get_sheets(self):
        """Obtener hojas cargadas (compatibilidad)"""
        return self.data_loader.get_sheets()
    
    @property
    def sheets(self):
        """Propiedad para compatibilidad con código existente"""
        return self.data_loader.get_sheets()