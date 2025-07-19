#!/usr/bin/env python3
"""
Convert JSON menu data to text format for Botpress Knowledge Base
"""

import json
import os

def create_menu_text_file():
    """Create a text file with all menu items for Botpress Knowledge Base"""
    
    # Load menu data
    menu_file = "menu_template.json"
    if not os.path.exists(menu_file):
        print("❌ menu_template.json not found. Please run add_menu_items.py first.")
        return
    
    with open(menu_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        menu_items = data.get("menu_items", [])
    
    # Group items by category
    categories = {}
    for item in menu_items:
        category = item.get("category", "Otros")
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    # Create text content
    text_content = "PRANA JUICE BAR - MENÚ COMPLETO\n\n"
    
    # Add each category
    for category, items in categories.items():
        text_content += f"CATEGORÍA: {category.upper()}\n\n"
        
        for item in items:
            name = item.get("name", "")
            price = item.get("price", 0)
            ingredients = item.get("ingredients", [])
            description = item.get("description", "")
            available = item.get("available", True)
            
            status = "✅" if available else "❌"
            text_content += f"{status} {name} - ${price:.2f}\n"
            
            if ingredients:
                text_content += f"Ingredientes: {', '.join(ingredients)}\n"
            
            if description:
                text_content += f"Descripción: {description}\n"
            
            text_content += "\n"
    
    # Add general information
    text_content += """
INFORMACIÓN GENERAL:

- Todos los jugos cold pressed son de 500ml
- Los precios están en dólares americanos
- Todos los ingredientes son frescos y naturales
- Horarios de atención: Lunes a Viernes 8:00 AM - 8:00 PM, Sábados y Domingos 9:00 AM - 7:00 PM
- Ubicación: [Dirección de Prana Juice Bar]
- Para pedidos especiales o consultas, contactar directamente

RESPUESTAS FRECUENTES:

¿Cuánto tiempo duran los jugos?
Los jugos cold pressed se recomiendan consumir el mismo día para máxima frescura y nutrientes.

¿Puedo personalizar mi jugo?
Sí, puedes solicitar modificaciones en los ingredientes según tus preferencias o restricciones alimentarias.

¿Tienen opciones sin azúcar?
Todos nuestros jugos son naturales sin azúcares añadidos. La dulzura proviene de las frutas naturales.

¿Puedo hacer pedidos para eventos?
Sí, ofrecemos servicios de catering para eventos. Contactar con anticipación para pedidos grandes.

¿Tienen opciones veganas?
Sí, todos nuestros jugos y la mayoría de nuestros productos son veganos. Consultar ingredientes específicos si tienes dudas.

¿Cuáles son los beneficios de los jugos cold pressed?
Los jugos cold pressed preservan más nutrientes, enzimas y vitaminas que los jugos tradicionales.

¿Tienen opciones sin gluten?
Sí, todos nuestros jugos son naturalmente sin gluten.

¿Puedo hacer pedidos por adelantado?
Sí, puedes hacer pedidos con anticipación para recoger en el momento que prefieras.

¿Tienen opciones para deportistas?
Sí, tenemos jugos específicos para recuperación muscular y energía pre-entrenamiento.

¿Cuál es la diferencia entre cold pressed y jugos normales?
Los jugos cold pressed se extraen sin generar calor, preservando más nutrientes y enzimas.
"""
    
    # Save to file
    output_file = "bot_data/menu_knowledge_base.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text_content)
    
    print(f"✅ Menu text file created: {output_file}")
    print(f"📋 Total items: {len(menu_items)}")
    print(f"📂 Categories: {len(categories)}")
    print("\n🎯 Now you can upload this file to Botpress Knowledge Base!")

if __name__ == "__main__":
    create_menu_text_file() 