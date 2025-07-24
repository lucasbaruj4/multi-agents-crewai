# CURSOR MEMORY: Google Colab Model Connection Setup

## **PROBLEMA RESUELTO:**
Conectar un modelo LLM desplegado en Google Colab con un proyecto local usando Cursor.

## **SOLUCIÓN IMPLEMENTADA:**

### **1. SETUP EN COLAB:**
- **Servidor Flask** en Colab exponiendo el modelo en puerto 8081
- **Localtunnel** para crear túnel público sin limitaciones de cuenta
- **URL pública:** `https://mistral-server.loca.lt`

### **2. HERRAMIENTAS UTILIZADAS:**
- **Localtunnel** (alternativa a ngrok sin limitaciones)
- **Flask API** con endpoints: `/health`, `/generate`, `/model_info`, `/resources`
- **Headers especiales** para bypasear advertencias: `bypass-tunnel-reminder: true`

### **3. CÓDIGO CLAVE PARA COLAB (Celda 6):**
```python
# Instalar localtunnel
subprocess.run(["npm", "install", "-g", "localtunnel"], check=True)

# Crear túnel
process = subprocess.Popen(
    ["lt", "--port", "8081", "--subdomain", "mistral-server"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# URL resultante: https://mistral-server.loca.lt
```

### **4. CÓDIGO CLAVE PARA CLIENTE LOCAL:**
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'bypass-tunnel-reminder': 'true',
    'Content-Type': 'application/json'
}

response = requests.post(
    "https://mistral-server.loca.lt/generate",
    headers=headers,
    json={"prompt": "Hello", "max_tokens": 50, "temperature": 0.7}
)
```

### **5. VENTAJAS DE ESTA SOLUCIÓN:**
- ✅ Sin limitaciones de cuenta (vs ngrok gratuito)
- ✅ Funciona desde cualquier lugar del mundo
- ✅ Modelo sigue en Colab usando GPU
- ✅ Código local puede usar modelo como si fuera local
- ✅ Latencia razonable

### **6. ARCHIVOS CREADOS:**
- `local_mistral_client.py` - Cliente para conectar con Colab
- `test_mistral_connection.py` - Test de conexión
- `crewai_mistral_integration.py` - Integración con CrewAI

### **7. FLUJO DE CONEXIÓN:**
```
PROYECTO LOCAL → INTERNET → LOCALTUNNEL → COLAB (Puerto 8081) → MODELO LLM
```

### **8. PARA FUTUROS PROYECTOS:**
1. Desplegar modelo en Colab con Flask API
2. Usar localtunnel para exponer puerto
3. Usar headers especiales en requests locales
4. URL será: `https://[subdomain].loca.lt`

## **COMANDOS ÚTILES:**
```bash
# En Colab
npm install -g localtunnel
lt --port 8081 --subdomain [nombre]

# En local
python test_connection.py
```

## **FECHA:** 24/Jul/2025
## **PROYECTO:** Multi AI-Agent Systems with CrewAI
## **MODELO:** Mistral-7B-Instruct-v0.3 