#!/usr/bin/env python3
"""
🔧 Trading Analyzer Pro - Deployment Fix
Script para verificar y arreglar problemas de despliegue
"""

import os
import sys

def check_file_structure():
    """Verificar que la estructura de archivos sea correcta"""
    print("🔍 Verificando estructura de archivos...")
    
    required_files = [
        "app.py",
        "config/settings.py",
        "core/analyzer.py", 
        "ui/sidebar.py",
        "ui/dashboard.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - FALTA")
            return False
    
    return True

def check_unique_keys():
    """Verificar que no haya claves duplicadas"""
    print("\n🔑 Verificando claves únicas...")
    
    # Leer archivo de configuración
    try:
        with open("config/settings.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "UI_KEYS" in content:
                print("✅ UI_KEYS encontrado en configuración")
            else:
                print("❌ UI_KEYS no encontrado")
                return False
    except Exception as e:
        print(f"❌ Error leyendo configuración: {e}")
        return False
    
    # Verificar que sidebar.py use las claves
    try:
        with open("ui/sidebar.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "key=UI_KEYS" in content:
                print("✅ Sidebar usa claves únicas")
            else:
                print("❌ Sidebar no usa claves únicas")
                return False
    except Exception as e:
        print(f"❌ Error leyendo sidebar: {e}")
        return False
    
    return True

def check_app_py():
    """Verificar que app.py sea la versión modular"""
    print("\n📱 Verificando app.py...")
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
            
            # Verificar que sea la versión modular
            if "from ui.sidebar import" in content:
                print("✅ app.py es la versión modular")
                
                # Contar líneas
                lines = len(content.split('\n'))
                print(f"📏 Líneas de código: {lines}")
                
                if lines < 200:
                    print("✅ Tamaño apropiado para versión modular")
                else:
                    print("⚠️ Archivo muy grande, podría ser versión antigua")
                
            else:
                print("❌ app.py parece ser la versión monolítica")
                return False
                
    except Exception as e:
        print(f"❌ Error leyendo app.py: {e}")
        return False
    
    return True

def create_streamlit_config():
    """Crear configuración de Streamlit para evitar errores"""
    print("\n⚙️ Creando configuración de Streamlit...")
    
    config_dir = ".streamlit"
    config_file = os.path.join(config_dir, "config.toml")
    
    os.makedirs(config_dir, exist_ok=True)
    
    config_content = """[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#00d2d3"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[client]
showErrorDetails = true
"""
    
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(config_content)
        print(f"✅ Configuración creada en {config_file}")
        return True
    except Exception as e:
        print(f"❌ Error creando configuración: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🚀 Trading Analyzer Pro - Verificación de Despliegue")
    print("=" * 60)
    
    checks = [
        ("Estructura de archivos", check_file_structure),
        ("Claves únicas", check_unique_keys), 
        ("App.py modular", check_app_py),
        ("Configuración Streamlit", create_streamlit_config)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n--- {check_name} ---")
        if check_func():
            passed += 1
        else:
            print(f"❌ Falló: {check_name}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADO: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("✅ ¡Todo listo! La aplicación debería funcionar correctamente.")
        print("🚀 La versión modular está correctamente configurada.")
    else:
        print("⚠️ Hay problemas que necesitan resolverse.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)