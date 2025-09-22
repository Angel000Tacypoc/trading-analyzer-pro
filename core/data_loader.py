"""
📁 Trading Analyzer Pro - Data Loader
Módulo para carga y validación de datos de trading
"""

import pandas as pd
import streamlit as st
from typing import Dict, Optional
from ..config.settings import SUPPORTED_FILE_TYPES

class DataLoader:
    """🔄 Cargador de datos de trading con validación"""
    
    def __init__(self):
        self.sheets = {}
        self.metadata = {}
    
    def load_from_upload(self, uploaded_file) -> bool:
        """
        Cargar datos desde archivo subido con validación avanzada
        
        Args:
            uploaded_file: Archivo subido por Streamlit
            
        Returns:
            bool: True si la carga fue exitosa
        """
        try:
            st.info("📁 Procesando archivo...")
            
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension in ['xlsx', 'xls']:
                return self._load_excel(uploaded_file)
            elif file_extension == 'csv':
                return self._load_csv(uploaded_file)
            else:
                st.error("❌ **Formato no soportado**")
                st.error("📋 Formatos aceptados: Excel (.xlsx, .xls), CSV (.csv)")
                return False
                
        except Exception as e:
            st.error(f"❌ **Error cargando archivo**: {str(e)}")
            st.error("💡 **Posibles soluciones:**")
            st.error("  • Verifica que el archivo no esté corrupto")
            st.error("  • Asegúrate de que sea un archivo de trading válido")
            st.error("  • Intenta con un formato diferente (Excel ↔ CSV)")
            return False
    
    def _load_excel(self, uploaded_file) -> bool:
        """Cargar archivo Excel con múltiples hojas"""
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
            
        # Guardar metadata
        self.metadata = {
            'file_type': 'excel',
            'file_name': uploaded_file.name,
            'total_sheets': len(excel_sheets),
            'total_rows': sum(len(data) for data in excel_sheets.values())
        }
        
        progress.empty()
        return True
    
    def _load_csv(self, uploaded_file) -> bool:
        """Cargar archivo CSV"""
        progress = st.progress(0)
        progress.progress(30)
        
        csv_data = pd.read_csv(uploaded_file)
        progress.progress(80)
        
        self.sheets = {'main': csv_data}
        progress.progress(100)
        
        st.success(f"✅ CSV cargado exitosamente:")
        st.info(f"📊 **{len(csv_data):,} transacciones detectadas**")
        
        # Mostrar columnas detectadas
        columns_preview = ', '.join(csv_data.columns[:5])
        if len(csv_data.columns) > 5:
            columns_preview += '...'
        st.write(f"  • **Columnas**: {columns_preview}")
        
        # Guardar metadata
        self.metadata = {
            'file_type': 'csv',
            'file_name': uploaded_file.name,
            'total_sheets': 1,
            'total_rows': len(csv_data),
            'total_columns': len(csv_data.columns)
        }
        
        progress.empty()
        return True
    
    def get_sheets(self) -> Dict[str, pd.DataFrame]:
        """Obtener todas las hojas cargadas"""
        return self.sheets
    
    def get_metadata(self) -> Dict:
        """Obtener metadata del archivo cargado"""
        return self.metadata
    
    def validate_data(self) -> Dict[str, bool]:
        """
        Validar que los datos cargados sean válidos para análisis
        
        Returns:
            Dict con resultados de validación
        """
        validation_results = {}
        
        for sheet_name, data in self.sheets.items():
            validation_results[sheet_name] = {
                'has_data': len(data) > 0,
                'has_numeric_columns': any(data.dtypes == 'float64') or any(data.dtypes == 'int64'),
                'has_date_columns': any('date' in col.lower() or 'time' in col.lower() for col in data.columns),
                'has_amount_columns': any('amount' in col.lower() or 'pnl' in col.lower() or 'profit' in col.lower() for col in data.columns),
                'min_rows': len(data) >= 10  # Mínimo 10 filas para análisis significativo
            }
        
        return validation_results
    
    def get_summary(self) -> str:
        """Obtener resumen del archivo cargado"""
        if not self.sheets:
            return "No hay datos cargados"
        
        total_rows = sum(len(data) for data in self.sheets.values())
        total_sheets = len(self.sheets)
        
        summary = f"📊 **Archivo cargado**: {self.metadata.get('file_name', 'Desconocido')}\n"
        summary += f"📄 **Hojas**: {total_sheets}\n"
        summary += f"📈 **Total transacciones**: {total_rows:,}\n"
        
        return summary