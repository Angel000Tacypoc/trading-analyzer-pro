"""
🧪 Trading Analyzer Pro - Test Runner
Script para verificar que la refactorización funcionó correctamente
"""

import sys
import os

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Probar que todos los imports funcionen correctamente"""
    print("🧪 Probando imports...")
    
    try:
        # Core imports
        from core.analyzer import AdvancedTradingAnalyzer
        from core.data_loader import DataLoader
        from core.calculations import FinancialCalculator
        print("✅ Core modules imported successfully")
        
        # Config imports
        from config.settings import PAGE_CONFIG, SUPPORTED_FILE_TYPES
        print("✅ Config modules imported successfully")
        
        # UI imports
        from ui.styles import apply_custom_styles
        from ui.dashboard import create_comprehensive_dashboard
        from ui.metrics import create_advanced_metrics_section
        from ui.sidebar import create_sidebar_header
        from ui.performance import create_performance_analysis_section
        from ui.temporal import create_temporal_analysis_section
        from ui.risk import create_advanced_risk_analysis
        print("✅ UI modules imported successfully")
        
        # Utils imports
        from utils.report_generator import create_comprehensive_report
        print("✅ Utils modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_analyzer_creation():
    """Probar que el analizador se pueda crear correctamente"""
    print("🧪 Probando creación del analizador...")
    
    try:
        from core.analyzer import AdvancedTradingAnalyzer
        analyzer = AdvancedTradingAnalyzer()
        print("✅ AdvancedTradingAnalyzer created successfully")
        
        # Verificar que tiene los métodos necesarios
        assert hasattr(analyzer, 'load_data_from_upload')
        assert hasattr(analyzer, 'generate_comprehensive_analysis')
        print("✅ Required methods exist")
        
        return True
        
    except Exception as e:
        print(f"❌ Analyzer creation error: {e}")
        return False

def test_configuration():
    """Probar que las configuraciones se carguen correctamente"""
    print("🧪 Probando configuraciones...")
    
    try:
        from config.settings import PAGE_CONFIG, SUPPORTED_FILE_TYPES, UI_KEYS
        
        # Verificar PAGE_CONFIG
        assert 'page_title' in PAGE_CONFIG
        assert 'page_icon' in PAGE_CONFIG
        print("✅ PAGE_CONFIG is valid")
        
        # Verificar SUPPORTED_FILE_TYPES
        assert isinstance(SUPPORTED_FILE_TYPES, list)
        assert 'xlsx' in SUPPORTED_FILE_TYPES
        print("✅ SUPPORTED_FILE_TYPES is valid")
        
        # Verificar UI_KEYS
        assert 'file_uploader' in UI_KEYS
        assert 'checkboxes' in UI_KEYS
        print("✅ UI_KEYS is valid")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando tests de la refactorización...\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Analyzer Creation", test_analyzer_creation),
        ("Configuration Tests", test_configuration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 RESULTADOS: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡TODOS LOS TESTS PASARON! La refactorización fue exitosa.")
        print("✅ La aplicación está lista para usar con la nueva estructura modular.")
    else:
        print("⚠️ Algunos tests fallaron. Revisar los errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)