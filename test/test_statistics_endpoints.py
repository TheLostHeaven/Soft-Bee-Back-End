"""
Script para probar los endpoints de estadísticas
Ejecutar: python test_statistics_endpoints.py
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:5000"
APIARY_ID = "tu-apiary-id-aqui"  # Reemplazar con un ID real

def print_response(title, response):
    """Imprime la respuesta de forma legible"""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")

def test_apiary_statistics():
    """Prueba el endpoint de estadísticas generales"""
    url = f"{BASE_URL}/api/v1/statistics/apiary/{APIARY_ID}"
    response = requests.get(url)
    print_response("Estadísticas Generales del Apiario", response)

def test_health_trends():
    """Prueba el endpoint de tendencias de salud"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    url = f"{BASE_URL}/api/v1/statistics/apiary/{APIARY_ID}/health-trends"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
    response = requests.get(url, params=params)
    print_response("Tendencias de Salud de Colmenas", response)

def test_treatment_distribution():
    """Prueba el endpoint de distribución de tratamientos"""
    url = f"{BASE_URL}/api/v1/statistics/apiary/{APIARY_ID}/treatment-distribution"
    response = requests.get(url)
    print_response("Distribución de Tratamientos", response)

def test_inventory_levels():
    """Prueba el endpoint de niveles de inventario"""
    url = f"{BASE_URL}/api/v1/statistics/apiary/{APIARY_ID}/inventory-levels"
    response = requests.get(url)
    print_response("Niveles de Inventario", response)

def test_answer_score_trends():
    """Prueba el endpoint de tendencias de scores"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    url = f"{BASE_URL}/api/v1/statistics/apiary/{APIARY_ID}/answer-score-trends"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
    response = requests.get(url, params=params)
    print_response("Tendencias de Scores por Categoría", response)

def main():
    """Ejecuta todas las pruebas"""
    print("\n🚀 Iniciando pruebas de endpoints de estadísticas...")
    print(f"Base URL: {BASE_URL}")
    print(f"Apiary ID: {APIARY_ID}")
    
    if APIARY_ID == "tu-apiary-id-aqui":
        print("\n⚠️  ADVERTENCIA: Debes reemplazar APIARY_ID con un ID real")
        return
    
    try:
        # Ejecutar todas las pruebas
        test_apiary_statistics()
        test_health_trends()
        test_treatment_distribution()
        test_inventory_levels()
        test_answer_score_trends()
        
        print("\n✅ Pruebas completadas")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor")
        print("Asegúrate de que el servidor Flask esté corriendo en", BASE_URL)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()
