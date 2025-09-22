"""
🎨 Trading Analyzer Pro - UI Styles
Estilos CSS centralizados para la interfaz
"""

import streamlit as st

def apply_custom_styles():
    """Aplicar estilos CSS personalizados a la aplicación"""
    
    st.markdown("""
<style>
    /* 🎨 Main App Styling */
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
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* 📊 Metric Cards */
    .metric-premium {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease;
    }
    
    .metric-premium:hover {
        transform: translateY(-5px);
    }
    
    .metric-premium h2, .metric-premium h3 {
        margin: 0.2rem 0;
    }
    
    .metric-premium h2 {
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    /* 💚 Success/Performance Cards */
    .performance-excellent {
        border: 2px solid #00d2d3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #e0f9ff 0%, #ffffff 100%);
        box-shadow: 0 2px 10px rgba(0, 210, 211, 0.2);
    }
    
    .performance-excellent h1, .performance-excellent h2, .performance-excellent h3, .performance-excellent h4 {
        color: #006666;
        margin: 0.3rem 0;
    }
    
    /* 📈 Trading Insights */
    .trading-insight {
        border: 2px solid #3742fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #e8f4fd 0%, #ffffff 100%);
        box-shadow: 0 2px 10px rgba(55, 66, 250, 0.2);
    }
    
    .trading-insight h1, .trading-insight h2, .trading-insight h3, .trading-insight h4 {
        color: #2c3e50;
        margin: 0.3rem 0;
    }
    
    /* ⚠️ Alert/Warning Cards */
    .inactivity-alert {
        border: 2px solid #ff6b6b;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #ffe0e0 0%, #ffffff 100%);
        box-shadow: 0 2px 10px rgba(255, 107, 107, 0.2);
    }
    
    .inactivity-alert h1, .inactivity-alert h2, .inactivity-alert h3, .inactivity-alert h4 {
        color: #c0392b;
        margin: 0.3rem 0;
    }
    
    /* 📱 Sidebar Styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* 🔄 Buttons */
    .stButton > button {
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* 📊 Dataframe Styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* 📈 Chart Container */
    .js-plotly-plot {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* 💫 Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* 📱 Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .metric-premium h2 {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def get_status_color(value, thresholds=None):
    """
    Obtener color basado en el valor y umbrales
    
    Args:
        value: Valor a evaluar
        thresholds: Dict con umbrales {excellent, good, poor}
    
    Returns:
        str: Clase CSS correspondiente
    """
    if thresholds is None:
        thresholds = {"excellent": 70, "good": 50, "poor": 40}
    
    if value >= thresholds["excellent"]:
        return "performance-excellent"
    elif value >= thresholds["good"]:
        return "trading-insight"
    else:
        return "inactivity-alert"

def format_currency(amount, currency="USDT"):
    """Formatear cantidad como moneda"""
    if amount >= 0:
        return f"${amount:,.2f} {currency}"
    else:
        return f"-${abs(amount):,.2f} {currency}"

def format_percentage(value, decimals=1):
    """Formatear valor como porcentaje"""
    return f"{value:.{decimals}f}%"

def get_trend_icon(value):
    """Obtener icono de tendencia basado en valor"""
    if value > 0:
        return "📈"
    elif value < 0:
        return "📉"
    else:
        return "➡️"

def get_status_icon(value, positive_threshold=0):
    """Obtener icono de estado basado en valor"""
    if value > positive_threshold:
        return "🟢"
    elif value < positive_threshold:
        return "🔴"
    else:
        return "🟡"