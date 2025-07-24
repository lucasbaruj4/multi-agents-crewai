# 🚀 QUICK REFERENCE: Colab Model Connection

## **PROBLEMA:** Conectar modelo LLM en Colab con proyecto local

## **SOLUCIÓN RÁPIDA:**

### **1. EN COLAB:**
```python
# Celda 1-5: Setup modelo + Flask server en puerto 8081

# Celda 6: Localtunnel
import subprocess
subprocess.run(["npm", "install", "-g", "localtunnel"])
process = subprocess.Popen(["lt", "--port", "8081", "--subdomain", "mi-modelo"])
# URL: https://mi-modelo.loca.lt
```

### **2. EN LOCAL:**
```python
import requests

headers = {
    'bypass-tunnel-reminder': 'true',
    'Content-Type': 'application/json'
}

response = requests.post(
    "https://mi-modelo.loca.lt/generate",
    headers=headers,
    json={"prompt": "Hello", "max_tokens": 50}
)
```

## **ARCHIVOS LISTOS:**
- `local_mistral_client.py` - Cliente reutilizable
- `test_mistral_connection.py` - Test de conexión
- `cursor_memory_colab_model_connection.md` - Memoria completa

## **VENTAJAS:**
✅ Sin límites de cuenta  
✅ Modelo en GPU de Colab  
✅ Código local simple  
✅ Funciona desde cualquier lugar  

---
**Fecha:** 24/Jul/2025 | **Proyecto:** CrewAI Multi-Agent 