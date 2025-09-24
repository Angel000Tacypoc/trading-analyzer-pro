# 🗂️ Trading Analyzer Pro - Sistema de Filtros de Hojas

## 🎯 **NUEVA FUNCIONALIDAD: FILTROS INTELIGENTES**

### ✅ **¿QUÉ HACE?**
- **Filtrar hojas específicas** del Excel antes del análisis
- **Auto-detectar** hojas relevantes para trading
- **Patrones regex** para nombres complejos
- **Filtros predefinidos** para casos comunes

---

## 🎮 **MODOS DE FILTRO DISPONIBLES:**

### **🤖 1. Auto-detectar (Recomendado)**
- **Incluye automáticamente:** Hojas con "trading", "account", "futures", etc.
- **Excluye automáticamente:** "Sheet1", "template", "example", etc.
- **Personalizable:** Puedes excluir hojas manualmente

### **📝 2. Seleccionar Específicas**
- **Control total:** Elige exactamente qué hojas analizar
- **Multi-selección:** Checkboxes para cada hoja
- **Visualización clara:** Ve todas las hojas disponibles

### **🔢 3. Por Números**
- **Hojas 1, 2, 3:** Filtra por posición en el archivo
- **Útil para:** Archivos con nombres genéricos
- **Flexible:** Selecciona cualquier combinación

### **🏦 4. Por Tipo de Cuenta**
- **Futures:** Solo hojas de derivados/futuros
- **Spot:** Solo trading al contado
- **Margin:** Solo cuentas con apalancamiento
- **Trading:** Solo operaciones activas

---

## 📊 **EJEMPLOS PRÁCTICOS:**

### **Caso 1: Análisis Solo de Futuros**
```python
# El filtro detectará hojas como:
✅ "Futures_Account"
✅ "DERIVATIVES_TRADING"
✅ "Perpetual_Swaps"
❌ "Spot_Wallet" (excluida)
❌ "Savings_Account" (excluida)
```

### **Caso 2: Hojas Específicas**
```python
# Usuario selecciona:
✅ "Cuenta_Principal"
✅ "Trading_2024"
❌ "Demo_Account" (no seleccionada)
❌ "Historical_Data" (no seleccionada)
```

### **Caso 3: Solo Primeras 3 Hojas**
```python
# Analiza independientemente del nombre:
✅ Hoja 1: "Sheet1" → Analizada
✅ Hoja 2: "Accounts" → Analizada  
✅ Hoja 3: "Trading" → Analizada
❌ Hoja 4: "BackupData" → Ignorada
```

---

## 🚀 **BENEFICIOS:**

### **⚡ Rendimiento:**
- **Análisis más rápido** - solo procesa lo necesario
- **Menos memoria** - no carga hojas irrelevantes
- **Resultados limpios** - sin ruido de datos irrelevantes

### **🎯 Precisión:**
- **Análisis focado** - solo datos que importan
- **Menos errores** - evita hojas con formato incorrecto
- **Comparaciones justas** - solo cuentas similares

### **🎨 UX Mejorada:**
- **UI intuitiva** - selección visual de hojas
- **Feedback claro** - muestra qué se está analizando
- **Flexibilidad total** - desde auto hasta manual

---

## 🔧 **IMPLEMENTACIÓN TÉCNICA:**

### **Archivos Creados:**
- **`sheet_filter.py`** - Sistema de filtros principal
- **Integración en `app.py`** - UI y funcionalidad

### **Clases Principales:**
- **`SheetFilter`** - Filtro configurable principal
- **`CommonFilters`** - Filtros predefinidos comunes

### **Funcionalidades:**
- ✅ **Filtros por nombre** - exacto o parcial
- ✅ **Patrones regex** - búsquedas complejas
- ✅ **Auto-detección** - inteligencia artificial
- ✅ **Exclusiones** - lista negra de hojas
- ✅ **UI integrada** - selector visual en sidebar

---

## 🎯 **USO EN LA APLICACIÓN:**

### **Paso 1:** Sube tu archivo Excel
### **Paso 2:** Elige modo de filtro en sidebar
### **Paso 3:** Configura según tus necesidades
### **Paso 4:** Presiona "🚀 Analizar Archivo"
### **Paso 5:** Ve resultados solo de hojas seleccionadas

**¡Tu análisis ahora es mucho más preciso y controlable!** 🎯✨