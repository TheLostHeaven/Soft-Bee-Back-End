"""
Script de ejemplo para probar la feature de Reports
"""
import requests
import json
from uuid import UUID

# Configuración
BASE_URL = "http://localhost:5000/api/v1"
TOKEN = "tu-token-aqui"  # Reemplazar con un token válido

def test_get_apiary_report(apiary_id: str):
    """
    Prueba el endpoint de reporte de apiario
    """
    url = f"{BASE_URL}/reports/apiary/{apiary_id}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    print(f"\n{'='*60}")
    print(f"Obteniendo reporte del apiario: {apiary_id}")
    print(f"{'='*60}\n")
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            report = response.json()
            print_report(report)
        elif response.status_code == 404:
            print(f"❌ Error: Apiario no encontrado")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    
    except Exception as e:
        print(f"❌ Error al hacer la petición: {str(e)}")


def print_report(report: dict):
    """
    Imprime el reporte de forma legible
    """
    print("✅ Reporte generado exitosamente\n")
    
    # Información del apiario
    apiary = report['apiary']
    print(f"📍 APIARIO: {apiary['name']}")
    print(f"   Ubicación: {apiary['location']}")
    print(f"   Colmenas: {apiary['beehives_count']}")
    print(f"   Creado: {apiary['created_at']}")
    
    # Inventario
    print(f"\n📦 INVENTARIO ({len(report['inventory'])} items):")
    for item in report['inventory']:
        print(f"   • {item['name']}: {item['quantity']} {item['unit']}")
        if item['quantity'] <= item['minimum_stock']:
            print(f"     ⚠️  Stock bajo (mínimo: {item['minimum_stock']})")
    
    # Colmenas
    print(f"\n🐝 COLMENAS ({len(report['beehives'])} colmenas):")
    for beehive_detail in report['beehives']:
        beehive = beehive_detail['beehive']
        print(f"\n   Colmena #{beehive['hive_number']}:")
        print(f"   • Estado: {beehive['hive_status']}")
        print(f"   • Salud: {beehive['health_status']}")
        print(f"   • Población: {beehive['bee_population']}")
        print(f"   • Cuadros de alimento: {beehive['food_frames']}")
        print(f"   • Cuadros de cría: {beehive['brood_frames']}")
        print(f"   • Tratamientos: {'Sí' if beehive['treatments'] else 'No'}")
        
        # Preguntas y respuestas
        qa_list = beehive_detail['questions_answers']
        answered = sum(1 for qa in qa_list if qa['answer'])
        print(f"   • Preguntas respondidas: {answered}/{len(qa_list)}")
        
        if qa_list:
            print(f"   • Respuestas:")
            for qa in qa_list[:3]:  # Mostrar solo las primeras 3
                answer = qa['answer'] if qa['answer'] else "Sin responder"
                print(f"     - {qa['question']}: {answer}")
    
    # Estadísticas
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   • Total de preguntas: {report['total_questions']}")
    print(f"   • Total de respuestas: {report['total_answers']}")
    completion = (report['total_answers'] / report['total_questions'] * 100) if report['total_questions'] > 0 else 0
    print(f"   • Completitud: {completion:.1f}%")
    print(f"   • Generado: {report['generated_at']}")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    # Ejemplo de uso
    # Reemplazar con un UUID válido de tu base de datos
    apiary_id = "uuid-del-apiario-aqui"
    
    print("\n🚀 Iniciando prueba de la feature de Reports")
    test_get_apiary_report(apiary_id)
