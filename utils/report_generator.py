"""
📄 Trading Analyzer Pro - Report Generator
Generador de reportes comprehensivos
"""

from datetime import datetime
from typing import Dict

def create_comprehensive_report(analysis: Dict) -> str:
    """
    Generar reporte completo en texto
    
    Args:
        analysis: Diccionario con análisis completo
        
    Returns:
        str: Reporte formateado en texto
    """
    report = "🚀 TRADING ANALYZER PRO - REPORTE AVANZADO CON IA\n"
    report += "=" * 80 + "\n"
    report += f"📅 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Información del archivo
    metadata = analysis.get('metadata', {})
    if metadata:
        report += "📁 INFORMACIÓN DEL ARCHIVO\n"
        report += "-" * 40 + "\n"
        report += f"Archivo: {metadata.get('file_name', 'Desconocido')}\n"
        report += f"Tipo: {metadata.get('file_type', 'Desconocido').upper()}\n"
        report += f"Hojas/Tablas: {metadata.get('total_sheets', 0)}\n"
        report += f"Total de filas: {metadata.get('total_rows', 0):,}\n\n"
    
    # Métricas principales
    trading_performance = analysis.get('trading_performance', {})
    overall = trading_performance.get('overall_metrics', {})
    
    if overall:
        report += "💰 MÉTRICAS PRINCIPALES\n"
        report += "-" * 40 + "\n"
        report += f"PnL Total: ${overall.get('total_pnl_all_accounts', 0):,.2f}\n"
        report += f"Total Trades: {overall.get('total_trades_all_accounts', 0):,}\n"
        report += f"Cuentas Analizadas: {overall.get('total_accounts', 0)}\n"
        report += f"Win Rate Global: {overall.get('global_win_rate', 0):.1f}%\n"
        report += f"Cuentas Rentables: {overall.get('profitable_accounts', 0)}\n"
        report += f"Cuentas con Pérdidas: {overall.get('losing_accounts', 0)}\n"
        
        best_account = overall.get('best_performing_account')
        worst_account = overall.get('worst_performing_account')
        if best_account:
            report += f"Mejor Cuenta: {best_account}\n"
        if worst_account:
            report += f"Peor Cuenta: {worst_account}\n"
        report += "\n"
    
    # Detalles por cuenta
    financial_summary = analysis.get('financial_summary', {})
    if financial_summary:
        report += "🏦 ANÁLISIS DETALLADO POR CUENTA\n"
        report += "-" * 50 + "\n"
        
        for account, data in financial_summary.items():
            report += f"\n📊 {account.upper()}:\n"
            report += f"  PnL Total: ${data.get('pnl_total', 0):,.2f}\n"
            
            if 'win_rate' in data:
                report += f"  Win Rate: {data['win_rate']:.1f}%\n"
            if 'total_trades' in data:
                report += f"  Total Trades: {data['total_trades']:,}\n"
            if 'profit_factor' in data:
                report += f"  Profit Factor: {data['profit_factor']:.2f}\n"
            if 'max_drawdown' in data:
                report += f"  Max Drawdown: ${data['max_drawdown']:,.2f}\n"
            if 'total_profit' in data:
                report += f"  Ganancias Totales: ${data['total_profit']:,.2f}\n"
            if 'total_loss' in data:
                report += f"  Pérdidas Totales: ${abs(data['total_loss']):,.2f}\n"
        report += "\n"
    
    # Análisis temporal
    temporal = analysis.get('temporal_analysis', {})
    global_patterns = temporal.get('global_activity_patterns', {})
    if global_patterns:
        report += "📅 ANÁLISIS TEMPORAL\n"
        report += "-" * 30 + "\n"
        report += f"Período Total: {global_patterns.get('total_period_days', 0)} días\n"
        report += f"Día Más Activo: {global_patterns.get('most_active_day', 'N/A')}\n"
        report += f"Hora Pico: {global_patterns.get('peak_hour', 'N/A')}:00\n\n"
    
    # Análisis de riesgo
    risk_metrics = analysis.get('risk_metrics', {})
    portfolio_risk = risk_metrics.get('portfolio_risk', {})
    if portfolio_risk:
        report += "⚠️ ANÁLISIS DE RIESGO\n"
        report += "-" * 30 + "\n"
        report += f"Volatilidad del Portafolio: {portfolio_risk.get('total_portfolio_volatility', 0):.4f}\n"
        report += f"Ratio Sharpe: {portfolio_risk.get('portfolio_sharpe_ratio', 0):.4f}\n"
        report += f"Nivel de Riesgo: {portfolio_risk.get('portfolio_risk_level', 'N/A').upper()}\n\n"
    
    # Insights predictivos
    predictive = analysis.get('predictive_insights', {})
    if predictive:
        report += "🔮 INSIGHTS PREDICTIVOS CON IA\n"
        report += "-" * 40 + "\n"
        report += f"Predicción de Rendimiento: {predictive.get('performance_prediction', 'N/A').upper()}\n"
        report += f"Potencial de Crecimiento: {predictive.get('growth_potential', 'N/A').upper()}\n"
        report += f"Evaluación de Riesgo: {predictive.get('risk_assessment', 'N/A').upper()}\n"
        
        recommendations = predictive.get('recommendations', [])
        if recommendations:
            report += "\n🎯 RECOMENDACIONES:\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"  {i}. {rec}\n"
        report += "\n"
    
    # Alertas críticas
    alerts = analysis.get('smart_alerts', [])
    if alerts:
        report += "🚨 ALERTAS INTELIGENTES\n"
        report += "-" * 35 + "\n"
        for i, alert in enumerate(alerts, 1):
            # Limpiar emojis para el reporte de texto
            clean_alert = alert.replace('🚨', '[CRÍTICO]').replace('⚠️', '[AVISO]').replace('⏰', '[TIEMPO]')
            report += f"  {i}. {clean_alert}\n"
        report += "\n"
    
    # Patrones de inactividad
    inactivity = analysis.get('inactivity_patterns', {})
    account_inactivity = inactivity.get('account_inactivity', {})
    if account_inactivity:
        report += "⏰ ANÁLISIS DE INACTIVIDAD\n"
        report += "-" * 35 + "\n"
        report += f"Evaluación Global: {inactivity.get('severity_assessment', 'N/A').upper()}\n\n"
        
        for account, data in account_inactivity.items():
            report += f"  {account}:\n"
            report += f"    Máximo período inactivo: {data['max_inactivity_days']} días\n"
            report += f"    Nivel de riesgo: {data['risk_level'].upper()}\n"
            report += f"    Total de gaps: {data['total_gaps']}\n\n"
    
    # Footer
    report += "=" * 80 + "\n"
    report += "💡 Este reporte fue generado automáticamente por Trading Analyzer Pro\n"
    report += "🤖 Powered by Inteligencia Artificial y Análisis de Datos Avanzado\n"
    report += "📊 Para análisis más detallados, visita la aplicación web interactiva\n"
    
    return report

def create_summary_report(analysis: Dict) -> str:
    """
    Generar reporte resumen más corto
    
    Args:
        analysis: Diccionario con análisis completo
        
    Returns:
        str: Reporte resumen
    """
    trading_performance = analysis.get('trading_performance', {})
    overall = trading_performance.get('overall_metrics', {})
    
    summary = f"📊 RESUMEN EJECUTIVO - {datetime.now().strftime('%Y-%m-%d')}\n"
    summary += "=" * 50 + "\n\n"
    
    total_pnl = overall.get('total_pnl_all_accounts', 0)
    total_accounts = overall.get('total_accounts', 0)
    win_rate = overall.get('global_win_rate', 0)
    
    summary += f"💰 PnL Total: ${total_pnl:,.2f}\n"
    summary += f"🏦 Cuentas: {total_accounts}\n"
    summary += f"🎯 Win Rate: {win_rate:.1f}%\n\n"
    
    # Estado general
    if total_pnl > 1000:
        summary += "📈 ESTADO: EXCELENTE RENDIMIENTO\n"
    elif total_pnl > 0:
        summary += "📊 ESTADO: RENDIMIENTO POSITIVO\n"
    else:
        summary += "📉 ESTADO: REQUIERE ATENCIÓN\n"
    
    # Alertas críticas
    alerts = analysis.get('smart_alerts', [])
    critical_alerts = [a for a in alerts if "🚨" in a]
    if critical_alerts:
        summary += f"\n⚠️ ALERTAS CRÍTICAS: {len(critical_alerts)}\n"
    
    summary += f"\n📅 Generado: {datetime.now().strftime('%H:%M')}\n"
    
    return summary