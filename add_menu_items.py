#!/usr/bin/env python3
"""
Simple Menu Item Entry Script for Prana Juice Bar
This script helps you quickly add your menu items manually.
"""

import json
import os

def add_menu_item():
    """Add a single menu item"""
    print("\n" + "="*50)
    print("🥤 AÑADIR NUEVO ITEM DEL MENÚ")
    print("="*50)
    
    # Get item details
    name = input("Nombre del producto: ").strip()
    if not name:
        return None
    
    try:
        price = float(input("Precio (ej: 8.50): ").strip())
    except ValueError:
        print("❌ Precio inválido. Usando 0.00")
        price = 0.00
    
    print("\nCategorías disponibles:")
    categories = [
        "Jugos Cold Pressed",
        "Desayunos", 
        "Almuerzos",
        "Bake Goods",
        "Milks",
        "Shots",
        "Postres",
        "Prana Cakes"
    ]
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    try:
        cat_choice = int(input("Selecciona categoría (1-8): ").strip())
        category = categories[cat_choice - 1]
    except (ValueError, IndexError):
        print("❌ Selección inválida. Usando 'Jugos Cold Pressed'")
        category = "Jugos Cold Pressed"
    
    ingredients_input = input("Ingredientes (separados por comas): ").strip()
    ingredients = [ing.strip() for ing in ingredients_input.split(",") if ing.strip()]
    
    description = input("Descripción (opcional): ").strip()
    
    available = input("¿Disponible? (s/n): ").strip().lower() == 's'
    
    return {
        "name": name,
        "price": price,
        "category": category,
        "ingredients": ingredients,
        "description": description,
        "available": available
    }

def load_existing_menu():
    """Load existing menu items"""
    menu_file = "menu_template.json"
    if os.path.exists(menu_file):
        with open(menu_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("menu_items", [])
    return []

def save_menu(menu_items):
    """Save menu items to file"""
    menu_file = "menu_template.json"
    data = {
        "menu_items": menu_items,
        "categories": [
            "Jugos Cold Pressed",
            "Desayunos", 
            "Almuerzos",
            "Bake Goods",
            "Milks",
            "Shots",
            "Postres",
            "Prana Cakes"
        ]
    }
    
    with open(menu_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Menú guardado en {menu_file}")

def display_menu(menu_items):
    """Display current menu items"""
    if not menu_items:
        print("\n📋 No hay items en el menú aún.")
        return
    
    print(f"\n📋 MENÚ ACTUAL ({len(menu_items)} items):")
    print("="*50)
    
    current_category = ""
    for item in menu_items:
        if item["category"] != current_category:
            current_category = item["category"]
            print(f"\n🍹 {current_category}:")
        
        status = "✅" if item["available"] else "❌"
        print(f"  {status} {item['name']} - ${item['price']:.2f}")
        if item["ingredients"]:
            print(f"     Ingredientes: {', '.join(item['ingredients'])}")

def main():
    """Main function"""
    print("🥤 PRANA JUICE BAR - EDITOR DE MENÚ")
    print("="*50)
    
    # Load existing menu
    menu_items = load_existing_menu()
    
    while True:
        print("\n" + "="*50)
        print("OPCIONES:")
        print("1. Ver menú actual")
        print("2. Añadir nuevo item")
        print("3. Guardar y continuar con bot setup")
        print("4. Salir")
        
        choice = input("\nSelecciona opción (1-4): ").strip()
        
        if choice == "1":
            display_menu(menu_items)
        
        elif choice == "2":
            new_item = add_menu_item()
            if new_item:
                menu_items.append(new_item)
                print(f"\n✅ '{new_item['name']}' añadido al menú!")
        
        elif choice == "3":
            if menu_items:
                save_menu(menu_items)
                print("\n🎯 Ahora puedes continuar con el setup del bot!")
                print("Ejecuta: python whatsapp_bot_setup.py")
                break
            else:
                print("\n❌ No hay items en el menú. Añade al menos uno.")
        
        elif choice == "4":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("\n❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main() 