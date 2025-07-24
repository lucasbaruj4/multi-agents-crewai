"""
Test Mistral Connection - Simple Local Test
Prueba la conexión desde tu proyecto local al modelo Mistral en Colab
"""

import requests
import json
import time

def test_mistral_simple():
    """Test simple y directo del modelo Mistral"""
    
    # URL del túnel localtunnel
    base_url = "https://mistral-server.loca.lt"
    
    print("🚀 Probando conexión local → Colab Mistral")
    print(f"🔗 URL: {base_url}")
    print("=" * 50)
    
    # Headers para bypasear advertencias
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'bypass-tunnel-reminder': 'true',
        'Content-Type': 'application/json'
    }
    
    try:
        # Test 1: Health Check
        print("1️⃣ Health Check...")
        response = requests.get(f"{base_url}/health", headers=headers, timeout=10)
        
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Servidor saludable!")
            print(f"   Modelo cargado: {health.get('model_loaded', False)}")
            print(f"   Timestamp: {health.get('timestamp', 'N/A')}")
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
        
        # Test 2: Generación simple en español
        print("\n2️⃣ Generación en español...")
        prompt = "Explica qué es un sistema multi-agente en 2 oraciones."
        
        gen_response = requests.post(
            f"{base_url}/generate",
            headers=headers,
            json={
                "prompt": prompt,
                "max_tokens": 50,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if gen_response.status_code == 200:
            result = gen_response.json()
            print("✅ Generación exitosa!")
            print(f"📝 Prompt: {prompt}")
            print(f"🤖 Respuesta: {result.get('response', 'Sin respuesta')}")
            print(f"🔢 Tokens: {result.get('tokens_used', 'N/A')}")
        else:
            print(f"❌ Generación falló: {gen_response.status_code}")
            return False
        
        # Test 3: Generación técnica
        print("\n3️⃣ Generación técnica...")
        tech_prompt = "¿Cuáles son las ventajas de usar CrewAI para sistemas multi-agente?"
        
        tech_response = requests.post(
            f"{base_url}/generate",
            headers=headers,
            json={
                "prompt": tech_prompt,
                "max_tokens": 80,
                "temperature": 0.5
            },
            timeout=30
        )
        
        if tech_response.status_code == 200:
            result = tech_response.json()
            print("✅ Generación técnica exitosa!")
            print(f"📝 Prompt: {tech_prompt}")
            print(f"🤖 Respuesta: {result.get('response', 'Sin respuesta')}")
        else:
            print(f"⚠️ Generación técnica falló: {tech_response.status_code}")
        
        # Test 4: Info del modelo
        print("\n4️⃣ Información del modelo...")
        info_response = requests.get(f"{base_url}/model_info", headers=headers, timeout=10)
        
        if info_response.status_code == 200:
            info = info_response.json()
            print("✅ Info del modelo:")
            print(f"   Modelo: {info.get('model_name', 'unknown')}")
            print(f"   Tipo: {info.get('model_type', 'unknown')}")
            print(f"   Device: {info.get('device', 'unknown')}")
        
        print("\n" + "=" * 50)
        print("🎉 ¡CONEXIÓN EXITOSA!")
        print("✅ Tu proyecto local puede usar el modelo Mistral en Colab")
        print(f"🔗 URL lista para CrewAI: {base_url}")
        print("💡 Ahora puedes integrar esto en tu sistema multi-agente")
        
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Timeout - La conexión tardó mucho")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - Verifica que Colab esté corriendo")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_crewai_integration():
    """Test específico para integración con CrewAI"""
    
    print("\n🔧 Test de integración CrewAI...")
    
    # Importar el cliente local
    try:
        from local_mistral_client import ColabMistralClient
        
        # Crear cliente
        client = ColabMistralClient("dummy_url")  # La URL ya está hardcodeada
        
        # Test del cliente
        print("📡 Probando cliente local...")
        health = client.health_check()
        print(f"✅ Cliente funciona: {health}")
        
        # Test de generación con el cliente
        print("🤖 Probando generación con cliente...")
        response = client.generate_text(
            prompt="¿Qué es CrewAI?",
            max_tokens=40,
            temperature=0.6
        )
        print(f"✅ Respuesta del cliente: {response}")
        
        print("🎉 Cliente local listo para CrewAI!")
        return True
        
    except ImportError:
        print("⚠️ No se pudo importar local_mistral_client.py")
        return False
    except Exception as e:
        print(f"❌ Error en cliente: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TEST DE CONEXIÓN MISTRAL LOCAL → COLAB")
    print("=" * 60)
    
    # Test básico
    success = test_mistral_simple()
    
    if success:
        print("\n" + "="*60)
        # Test de integración
        test_crewai_integration()
    
    print("\n" + "="*60)
    print("🏁 Tests completados!")
    
    if success:
        print("✅ ¡Todo listo para trabajar con CrewAI!")
    else:
        print("❌ Hay problemas de conexión que resolver") 