"""
⚙️ Trading Analyzer Pro - Settings & Configuration
Configuraciones centralizadas de la aplicación
"""

# 📊 App Configuration
APP_TITLE = "Trading Analyzer Pro"
APP_ICON = "💰"
PAGE_CONFIG = {
    "page_title": "Trading Analyzer Pro",
    "page_icon": "💰", 
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# 📁 File Upload Settings
SUPPORTED_FILE_TYPES = ['xlsx', 'xls', 'csv']
MAX_FILE_SIZE_MB = 50

# 📈 Trading Analysis Settings
DEFAULT_CURRENCY = "USDT"
WIN_RATE_THRESHOLDS = {
    "excellent": 70,
    "good": 50,
    "poor": 40
}

PNL_THRESHOLDS = {
    "significant_profit": 1000,
    "significant_loss": -500
}

# 🔍 Data Detection Keywords
PNL_KEYWORDS = ['realized_pnl', 'realized pnl', 'pnl', 'profit_loss', 'net_profit', 'amount']
DATE_KEYWORDS = ['time', 'date', 'utc', 'timestamp']
TYPE_KEYWORDS = ['type', 'side', 'action', 'operation']
AMOUNT_KEYWORDS = ['amount', 'pnl', 'balance', 'profit', 'loss', 'realized', 'unrealized', 'total', 'net']

# 🤖 Trading Detection Keywords
TRADING_KEYWORDS = ['realized', 'pnl', 'fee', 'trade', 'buy', 'sell', 'long', 'short', 'open', 'close']

# 📊 Chart Configuration
CHART_CONFIG = {
    "plot_bgcolor": 'rgba(0,0,0,0)',
    "paper_bgcolor": 'rgba(0,0,0,0)',
    "font_color": '#2c3e50',
    "height": 400
}

# 🎨 Color Schemes
COLORS = {
    "profit": "#00d2d3",
    "loss": "#ff6b6b", 
    "neutral": "#feca57",
    "excellent": "#00d2d3",
    "good": "#3742fa",
    "warning": "#feca57",
    "danger": "#ff6b6b"
}

# 📱 UI Keys (para evitar duplicados en Streamlit)
UI_KEYS = {
    "file_uploader": "main_file_uploader",
    "analyze_button": "analyze_button_main",
    "checkboxes": {
        "dashboard": "main_cb_dashboard",
        "performance": "main_cb_performance", 
        "accounts": "main_cb_accounts",
        "temporal": "main_cb_temporal",
        "risk": "main_cb_risk"
    },
    "buttons": {
        "export": "btn_export",
        "download": "btn_download",
        "clear": "btn_clear"
    }
}