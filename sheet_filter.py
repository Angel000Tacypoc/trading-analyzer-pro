"""
🗂️ Trading Analyzer Pro - Sheet Filter System
Sistema de filtros inteligente para hojas de Excel
"""

import re
from typing import List, Dict, Set, Optional

class SheetFilter:
    """🔍 Filtro inteligente para hojas de Excel"""
    
    def __init__(self):
        self.included_sheets = set()  # Hojas específicas a incluir
        self.excluded_sheets = set()  # Hojas específicas a excluir
        self.sheet_patterns = []      # Patrones regex para nombres
        self.account_filters = []     # Filtros por tipo de cuenta
        self.auto_detect = True       # Auto-detectar hojas relevantes
    
    def add_sheet_by_name(self, sheet_name: str):
        """➕ Agregar hoja específica por nombre"""
        self.included_sheets.add(sheet_name.lower())
        return self
    
    def add_sheets_by_names(self, sheet_names: List[str]):
        """➕ Agregar múltiples hojas por nombre"""
        for name in sheet_names:
            self.add_sheet_by_name(name)
        return self
    
    def exclude_sheet(self, sheet_name: str):
        """➖ Excluir hoja específica"""
        self.excluded_sheets.add(sheet_name.lower())
        return self
    
    def add_pattern(self, pattern: str):
        """🎯 Agregar patrón regex para nombres de hojas"""
        self.sheet_patterns.append(re.compile(pattern, re.IGNORECASE))
        return self
    
    def add_account_filter(self, account_type: str):
        """🏦 Filtrar por tipo de cuenta"""
        account_patterns = {
            'futures': r'.*futures?.*|.*derivat.*|.*perp.*',
            'spot': r'.*spot.*|.*cash.*|.*wallet.*',
            'margin': r'.*margin.*|.*leverage.*',
            'savings': r'.*saving.*|.*earn.*|.*stake.*',
            'trading': r'.*trad.*|.*order.*|.*position.*'
        }
        
        if account_type.lower() in account_patterns:
            self.add_pattern(account_patterns[account_type.lower()])
        return self
    
    def filter_sheets(self, all_sheets: Dict) -> Dict:
        """🔍 Filtrar hojas según criterios configurados"""
        filtered_sheets = {}
        
        for sheet_name, sheet_data in all_sheets.items():
            if self._should_include_sheet(sheet_name):
                filtered_sheets[sheet_name] = sheet_data
        
        return filtered_sheets
    
    def _should_include_sheet(self, sheet_name: str) -> bool:
        """🤔 Determinar si una hoja debe incluirse"""
        sheet_lower = sheet_name.lower()
        
        # 1. Si está excluida explícitamente
        if sheet_lower in self.excluded_sheets:
            return False
        
        # 2. Si está incluida explícitamente
        if sheet_lower in self.included_sheets:
            return True
        
        # 3. Si coincide con algún patrón
        for pattern in self.sheet_patterns:
            if pattern.search(sheet_name):
                return True
        
        # 4. Auto-detección si está habilitada y no hay filtros específicos
        if self.auto_detect and not self.included_sheets and not self.sheet_patterns:
            return self._auto_detect_relevant_sheet(sheet_name)
        
        # 5. Si hay filtros específicos pero no coincide
        if self.included_sheets or self.sheet_patterns:
            return False
        
        # 6. Por defecto incluir si no hay filtros
        return True
    
    def _auto_detect_relevant_sheet(self, sheet_name: str) -> bool:
        """🤖 Auto-detectar si una hoja es relevante para trading"""
        sheet_lower = sheet_name.lower()
        
        # Patrones que indican datos de trading
        trading_indicators = [
            'trade', 'trading', 'order', 'position', 'pnl', 'profit',
            'futures', 'spot', 'margin', 'wallet', 'balance',
            'history', 'transaction', 'account'
        ]
        
        # Patrones que indican hojas irrelevantes
        irrelevant_patterns = [
            'sheet1', 'sheet2', 'sheet3', 'hoja1', 'hoja2', 'hoja3',
            'template', 'example', 'readme', 'instructions', 'guide'
        ]
        
        # Excluir hojas irrelevantes
        for pattern in irrelevant_patterns:
            if pattern in sheet_lower:
                return False
        
        # Incluir hojas con indicadores de trading
        for indicator in trading_indicators:
            if indicator in sheet_lower:
                return True
        
        # Por defecto incluir (mejor analizar de más que de menos)
        return True
    
    def get_filter_summary(self) -> Dict:
        """📋 Resumen de filtros activos"""
        return {
            'included_sheets': list(self.included_sheets),
            'excluded_sheets': list(self.excluded_sheets),
            'patterns': [p.pattern for p in self.sheet_patterns],
            'auto_detect': self.auto_detect,
            'has_specific_filters': bool(self.included_sheets or self.sheet_patterns)
        }

# 🎯 Filtros predefinidos comunes
class CommonFilters:
    """📋 Filtros predefinidos para casos comunes"""
    
    @staticmethod
    def only_futures() -> SheetFilter:
        """📈 Solo hojas de futuros"""
        return SheetFilter().add_account_filter('futures')
    
    @staticmethod
    def only_spot() -> SheetFilter:
        """💰 Solo hojas de spot trading"""
        return SheetFilter().add_account_filter('spot')
    
    @staticmethod
    def main_accounts_only() -> SheetFilter:
        """🏦 Solo cuentas principales (excluir demos/test)"""
        return (SheetFilter()
                .exclude_sheet('demo')
                .exclude_sheet('test')
                .exclude_sheet('sandbox')
                .add_pattern(r'^((?!demo|test|sandbox).)*$'))
    
    @staticmethod
    def by_sheet_numbers(sheet_numbers: List[int]) -> SheetFilter:
        """🔢 Solo hojas específicas por número"""
        filter_obj = SheetFilter()
        for num in sheet_numbers:
            filter_obj.add_pattern(f'.*{num}.*|sheet{num}|hoja{num}')
        return filter_obj
    
    @staticmethod
    def recent_data_only() -> SheetFilter:
        """📅 Solo datos recientes (excluir historical)"""
        return (SheetFilter()
                .exclude_sheet('historical')
                .exclude_sheet('archive')
                .exclude_sheet('backup')
                .add_pattern(r'^((?!historical|archive|backup|old).)*$'))

# 🧪 Ejemplos de uso
def create_filter_examples():
    """📝 Ejemplos de cómo usar los filtros"""
    
    examples = {
        # Ejemplo 1: Solo hojas específicas
        'specific_sheets': (SheetFilter()
                           .add_sheets_by_names(['Account1', 'MainTrading', 'Futures'])
                           .exclude_sheet('Demo')),
        
        # Ejemplo 2: Solo cuentas de futuros
        'futures_only': CommonFilters.only_futures(),
        
        # Ejemplo 3: Solo hojas 1, 2 y 3
        'first_three_sheets': CommonFilters.by_sheet_numbers([1, 2, 3]),
        
        # Ejemplo 4: Patrón personalizado
        'custom_pattern': (SheetFilter()
                          .add_pattern(r'.*account.*')
                          .add_pattern(r'.*trading.*')
                          .exclude_sheet('test')),
        
        # Ejemplo 5: Auto-detect con exclusiones
        'auto_with_exclusions': (SheetFilter()
                                .exclude_sheet('template')
                                .exclude_sheet('example')
                                .exclude_sheet('readme'))
    }
    
    return examples

if __name__ == "__main__":
    # 🧪 Prueba rápida
    sheet_filter = SheetFilter().add_sheets_by_names(['Account1', 'Futures']).exclude_sheet('Demo')
    print("📋 Filtro configurado:")
    print(sheet_filter.get_filter_summary())