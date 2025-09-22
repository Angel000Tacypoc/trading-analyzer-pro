"""
⚠️ Trading Analyzer Pro - Risk Analysis UI
Componentes para análisis de riesgo y volatilidad
"""

import streamlit as st
from typing import Dict

def create_advanced_risk_analysis(analysis: Dict):
    """⚠️ Análisis avanzado de riesgo simplificado"""
    
    st.subheader("⚠️ Análisis de Riesgo")
    
    risk_metrics = analysis.get('risk_metrics', {})
    portfolio_risk = risk_metrics.get('portfolio_risk', {})
    individual_risks = risk_metrics.get('individual_risks', {})
    performance = analysis.get('trading_performance', {})
    account_comparison = performance.get('account_comparison', {})
    
    if portfolio_risk:
        col1, col2 = st.columns(2)
        
        with col1:
            volatility = portfolio_risk.get('total_portfolio_volatility', 0)
            sharpe = portfolio_risk.get('portfolio_sharpe_ratio', 0)
            
            risk_level = "Bajo" if sharpe > 1 else "Medio" if sharpe > 0.5 else "Alto"
            risk_color = "performance-excellent" if sharpe > 1 else "trading-insight" if sharpe > 0.5 else "inactivity-alert"
            
            st.markdown(f'''
            <div class="{risk_color}">
                <h4>📊 Riesgo de Cartera</h4>
                <p><strong>Volatilidad:</strong> {volatility:.2f}</p>
                <p><strong>Ratio Sharpe:</strong> {sharpe:.2f}</p>
                <p><strong>Nivel de Riesgo:</strong> {risk_level}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            if account_comparison:
                # Mostrar cuentas por nivel de riesgo
                high_risk_accounts = []
                low_risk_accounts = []
                
                for account, data in account_comparison.items():
                    max_drawdown = abs(data.get('max_drawdown', 0))
                    if max_drawdown > 1000:
                        high_risk_accounts.append(f"{account} (${max_drawdown:,.0f})")
                    else:
                        low_risk_accounts.append(f"{account} (${max_drawdown:,.0f})")
                
                if high_risk_accounts:
                    st.markdown(f'''
                    <div class="inactivity-alert">
                        <h4>⚠️ Cuentas de Alto Riesgo</h4>
                        <p>{", ".join(high_risk_accounts[:3])}</p>
                        <p><small>Drawdown elevado</small></p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                if low_risk_accounts:
                    st.markdown(f'''
                    <div class="performance-excellent">
                        <h4>✅ Cuentas de Bajo Riesgo</h4>
                        <p>{", ".join(low_risk_accounts[:3])}</p>
                        <p><small>Drawdown controlado</small></p>
                    </div>
                    ''', unsafe_allow_html=True)
    
    else:
        st.info("📊 Análisis de riesgo no disponible con los datos actuales")