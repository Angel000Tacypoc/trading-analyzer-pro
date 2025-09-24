"""
🔍 Trading Analyzer - Debug Script
Script para verificar exactamente qué datos se están procesando
"""

import pandas as pd
import streamlit as st

def debug_pnl_calculation(file_path):
    """🧐 Debuggear cálculos de PnL"""
    
    print("🔍 DEBUGGING PNL CALCULATION")
    print("=" * 50)
    
    # Leer archivo
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            data = pd.read_excel(file_path, sheet_name=None)
        else:
            data = {'main': pd.read_csv(file_path)}
        
        for sheet_name, df in data.items():
            print(f"\n📋 SHEET: {sheet_name}")
            print(f"📏 Filas: {len(df)}")
            print(f"📊 Columnas: {list(df.columns)}")
            
            # Buscar columna PnL
            pnl_col = None
            for col in df.columns:
                if any(word in col.lower() for word in ['pnl', 'profit', 'amount', 'realized']):
                    pnl_col = col
                    break
            
            if pnl_col:
                print(f"💰 Columna PnL encontrada: '{pnl_col}'")
                
                pnl_values = df[pnl_col].dropna()
                profits = pnl_values[pnl_values > 0]
                losses = pnl_values[pnl_values < 0]
                
                print(f"📈 Total operaciones: {len(pnl_values)}")
                print(f"✅ Operaciones ganadoras: {len(profits)}")
                print(f"❌ Operaciones perdedoras: {len(losses)}")
                
                print(f"\n💰 CÁLCULOS:")
                print(f"Total PnL: ${pnl_values.sum():,.2f}")
                print(f"Total Ganancias: ${profits.sum():,.2f}")  # ← AQUÍ ESTÁ TU $6,500.53
                print(f"Total Pérdidas: ${abs(losses.sum()):,.2f}")
                
                print(f"\n🔢 PRIMERAS 10 GANANCIAS:")
                for i, profit in enumerate(profits.head(10)):
                    print(f"  {i+1}. ${profit:,.2f}")
                
                if len(profits) > 10:
                    print(f"  ... y {len(profits)-10} más operaciones ganadoras")
            
            else:
                print("❌ No se encontró columna PnL")
                print("🔍 Columnas disponibles:", list(df.columns))
    
    except Exception as e:
        print(f"❌ Error: {e}")

# Para usar:
# debug_pnl_calculation("tu_archivo.xlsx")