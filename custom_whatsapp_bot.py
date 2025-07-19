#!/usr/bin/env python3
"""
Prana Juice Bar WhatsApp Bot
A custom WhatsApp bot using existing knowledge base and menu data
"""

import json
import re
import random
from typing import Dict, List, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PranaWhatsAppBot:
    def __init__(self):
        """Initialize the bot with all data and knowledge base"""
        self.load_data()
        self.setup_responses()
        self.conversation_history = {}
        
    def load_data(self):
        """Load all bot data from files"""
        try:
            # Load menu items
            with open('bot_data/menu_items.json', 'r', encoding='utf-8') as f:
                self.menu_items = json.load(f)
            
            # Load knowledge base
            with open('bot_data/menu_knowledge_base.txt', 'r', encoding='utf-8') as f:
                self.knowledge_base = f.read()
            
            # Load response templates
            with open('bot_data/response_templates.json', 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
                
            # Load menu structure
            with open('bot_data/menu_structure.json', 'r', encoding='utf-8') as f:
                self.menu_structure = json.load(f)
                
            logger.info("✅ All bot data loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            raise
    
    def setup_responses(self):
        """Setup response patterns and categories"""
        self.categories = {
            'jugos cold pressed': ['jugos', 'zumo', 'zumo fresco', 'cold pressed', 'citrus', 'immunity', 'jugo'],
            'shots': ['shot', 'flu shot', 'ginger shot', 'power maca', 'orange baby'],
            'desayunos': ['desayuno', 'breakfast', 'bowl de chia', 'pancakes', 'tostada', 'berry blend'],
            'almuerzos': ['almuerzo', 'lunch', 'bowl', 'wrap', 'panini', 'ensalada'],
            'bake goods': ['bake', 'muffin', 'bolitas', 'energy balls'],
            'postres': ['postre', 'dessert', 'trufa', 'cheesecake', 'cookies'],
            'prana cakes': ['prana cakes', 'brownie', 'banana bread', 'cookie pie'],
            'milks': ['milky way', 'go nuts', 'batido', 'milk', 'milks', 'leche'],
            'extras': ['extra', 'adicional', 'complemento', 'topping', 'toppings']
        }
        
        # Common questions and their responses
        self.qa_patterns = {
            r'que.*shots.*tienen': self.get_shots,
            r'que.*jugos.*tienen': self.get_juices,
            r'que.*batidos.*tienen': self.get_smoothies,
            r'que.*desayunos.*tienen': self.get_breakfast,
            r'que.*almuerzos.*tienen': self.get_lunch,
            r'que.*postres.*tienen': self.get_desserts,
            r'bueno.*frio|frio.*bueno|refrescante': self.get_cold_drinks,
            r'energizante|energia|energetico': self.get_energy_drinks,
            r'detox|limpiar|desintoxicar': self.get_detox_drinks,
            r'precio|cuanto.*cuesta|costo': self.get_prices,
            r'(hora|horario|horarios|cierran|abren|cierre|apertura)': self.get_hours,
            # Location patterns - specific locations first
            r'(prana.*castellana|castellana|ubicacion.*castellana|donde.*castellana)': lambda: self.get_specific_location('castellana'),
            r'(prana.*palos.*grandes|palos.*grandes|ubicacion.*palos.*grandes|donde.*palos.*grandes)': lambda: self.get_specific_location('palos_grandes'),
            r'(castellana|palos.*grandes)': lambda: self.get_specific_location('castellana'),
            # General location patterns
            r'direccion|ubicacion|donde.*estan': self.get_location,
            r'menu.*completo|todo.*menu': self.get_full_menu,
            r'ingredientes.*(\w+)': self.get_ingredients,
            r'recomendacion|recomienda|sugerencia': self.get_recommendations,
            r'(ml|mililitros|tamaño|size|volumen|cuanto.*ml|cuantos.*ml)': self.get_volume_info,
            r'(cuanto.*pesa|peso.*gramos|peso.*g\b)': self.get_weight_info,
            r'(azucar|azúcar|añaden azucar|añaden azúcar|tienen azucar|tienen azúcar|agregan azucar|agregan azúcar|azucar añadida|azúcar añadida|azucar refinada|azúcar refinada|agua añadida|agregan agua|tienen agua)': self.get_sugar_water_info,
            r'(gluten|gluten free|sin gluten|celiaco|celíaco|trigo|wheat|pan|bread)': self.get_gluten_info,
            # Website patterns
            r'(sitio web|website|pagina web|página web|web|online|ordenar online|pedir online|comprar online|menu online|menú online)': self.get_website_link,
            # More specific drink patterns - these should come BEFORE the general drink pattern
            r'(para.*tomar|que.*tiene.*de.*beber|que.*tienen.*de.*beber|bebidas|que.*bebidas|que.*puedo.*tomar)': self.get_drink_categories,
            r'(sed|tomar|bebida|bebidas|algo.*tomar|quiero.*tomar)': self.get_drink_suggestions,
            r'(gripe|resfriado|enfermo|enferma|malestar|dolor|dolor de cabeza|dolor de estomago|dolor de estómago|nausea|vomito|vómito)': self.get_health_recommendations
        }
    
    def process_message(self, user_id: str, message: str) -> str:
        """Process incoming message and return appropriate response"""
        message = message.lower().strip()
        
        # Store in conversation history
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        self.conversation_history[user_id].append({
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Check for QA patterns (FAQ: hours, location, etc.) FIRST - even for first messages
        for pattern, handler in self.qa_patterns.items():
            if re.search(pattern, message, re.IGNORECASE):
                response = handler()
                return self.add_follow_up_question(response)
        
        # Always start with greeting for new conversations (if not a QA pattern)
        if len(self.conversation_history[user_id]) <= 1:
            return self.get_welcome_message()
        
        # Check for positive responses (yes, si, claro, etc.)
        if self.is_positive_response(message):
            return "¡Perfecto! ¿En qué puedo ayudarte? Puedes preguntarme por nuestro menú, horarios, precios, o cualquier cosa que necesites."
        
        # Check for goodbye/farewell messages
        if self.is_goodbye(message):
            return self.get_goodbye_message()
        
        # Check for greetings (for returning users)
        if self.is_greeting(message):
            return self.get_welcome_message()
        
        # Check for menu requests
        if self.is_menu_request(message):
            response = self.get_menu_categories()
            return self.add_follow_up_question(response)
        
        # Check for specific category requests
        category_response = self.get_category_items(message)
        if category_response:
            return self.add_follow_up_question(category_response)
        
        # Check for specific item searches
        item_response = self.search_menu_items(message)
        if item_response:
            return self.add_follow_up_question(item_response)
        
        # Check for specific item details
        item_detail = self.get_item_details(message)
        if item_detail:
            return self.add_follow_up_question(item_detail)
        
        # Default response
        response = self.get_help_message()
        return self.add_follow_up_question(response)
    
    def is_goodbye(self, message: str) -> bool:
        """Check if message is a goodbye/farewell"""
        goodbye_words = [
            'no', 'eso es todo', 'eso es', 'nada más', 'nada mas', 'gracias', 'hasta luego',
            'hasta la vista', 'adiós', 'adios', 'chao', 'bye', 'goodbye', 'that\'s all',
            'no más', 'no mas', 'ya está', 'ya esta', 'listo', 'terminado', 'mas nada'
        ]
        # Use word boundaries to avoid partial matches
        message_words = message.split()
        return any(word in message_words for word in goodbye_words)
    
    def add_follow_up_question(self, response: str) -> str:
        """Add follow-up question to any response"""
        follow_up = "\n\n¿Hay algo más en lo que pueda ayudarte?"
        return response + follow_up
    
    def get_goodbye_message(self) -> str:
        """Get goodbye message"""
        return "¡Gracias por visitar Prana Juice Bar! 🌿\n\n¡Esperamos verte pronto! ¡Que tengas un día saludable! 🥤"
    
    def is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        greetings = ['hola', 'buenos dias', 'buenas', 'buenas tardes', 'buenas noches', 'hey', 'hi', 'hello', 'que tal', 'bueno dias']
        return any(greeting in message for greeting in greetings)
    
    def is_menu_request(self, message: str) -> bool:
        """Check if user is asking for menu"""
        menu_words = ['menu', 'carta', 'que tienen', 'que ofrecen', 'que venden']
        return any(word in message for word in menu_words)
    
    def get_welcome_message(self) -> str:
        """Get personalized welcome message with website link"""
        # Use both welcome messages for a complete greeting
        welcome_messages = self.templates['welcome']
        website_info = self.templates['website']
        
        # Combine welcome message with website information
        welcome_text = f"{welcome_messages[0]}\n{welcome_messages[1]}"
        website_text = '\n'.join(website_info)
        
        return f"{welcome_text}\n\n{website_text}"
    
    def get_menu_categories(self) -> str:
        """Get menu categories"""
        categories = list(self.menu_structure.keys())
        response = "🥤 *NUESTRAS CATEGORÍAS:*\n\n"
        
        for i, category in enumerate(categories, 1):
            emoji = self.get_category_emoji(category)
            response += f"{i}. {emoji} {category.title()}\n"
        
        response += "\n¿Qué categoría te interesa? Puedes escribir el nombre o número."
        return response
    
    def get_category_emoji(self, category: str) -> str:
        """Get emoji for category"""
        emojis = {
            'jugos cold pressed': '🥤',
            'shots': '💉',
            'desayunos': '🌅',
            'almuerzos': '🍽️',
            'bake goods': '🥐',
            'postres': '🍰',
            'prana cakes': '🧁',
            'milks': '🥛',
            'extras': '➕'
        }
        return emojis.get(category.lower(), '🍽️')
    
    def get_category_items(self, message: str) -> Optional[str]:
        """Get items from a specific category"""
        message_lower = message.lower().strip()
        
        # Check for number inputs (1-9)
        number_mapping = {
            '1': 'jugos cold pressed',
            '2': 'shots', 
            '3': 'desayunos',
            '4': 'almuerzos',
            '5': 'bake goods',
            '6': 'postres',
            '7': 'prana cakes',
            '8': 'milks',
            '9': 'extras'
        }
        
        # Check if user typed a number
        for number, category in number_mapping.items():
            if number in message_lower:
                return self.get_items_by_category(category)
        
        # Check for exact category matches first (case insensitive)
        for category, keywords in self.categories.items():
            # Check if the message contains the category name
            if category.lower() in message_lower:
                return self.get_items_by_category(category)
            
            # Check for keyword matches
            if any(keyword.lower() in message_lower for keyword in keywords):
                return self.get_items_by_category(category)
        
        # Special handling for common variations
        if 'milk' in message_lower or 'milks' in message_lower or 'leche' in message_lower:
            return self.get_items_by_category('milks')
        
        if 'extra' in message_lower or 'extras' in message_lower or 'topping' in message_lower:
            return self.get_items_by_category('extras')
            
        return None
    
    def get_items_by_category(self, category: str) -> str:
        """Get all items from a category"""
        # Normalize category name for comparison
        category_lower = category.lower()
        
        items = []
        for item in self.menu_items:
            item_category = item.get('category', '').lower()
            if item_category == category_lower:
                items.append(item)
        
        if not items:
            return f"No encontré items en la categoría '{category}'. ¿Podrías ser más específico?"
        
        response = f"🍽️ *{category.upper()}*\n\n"
        
        for item in items[:10]:  # Limit to 10 items
            price = item.get('price', 'N/A')
            name = item.get('name', 'Sin nombre')
            response += f"✅ {name} - ${price}\n"
        
        if len(items) > 10:
            response += f"\n... y {len(items) - 10} más. ¿Te interesa algún item específico?"
        
        return response
    
    def search_menu_items(self, message: str) -> Optional[str]:
        """Search for specific menu items"""
        found_items = []
        
        for item in self.menu_items:
            name = item.get('name', '').lower()
            ingredients = item.get('ingredients', [])
            
            # Handle ingredients as list or string
            if isinstance(ingredients, list):
                ingredients_text = ', '.join(ingredients).lower()
            else:
                ingredients_text = str(ingredients).lower()
            
            if any(word in name or word in ingredients_text for word in message.split()):
                found_items.append(item)
        
        if found_items:
            response = "🔍 *ITEMS ENCONTRADOS:*\n\n"
            for item in found_items[:5]:  # Limit to 5 results
                name = item.get('name', 'Sin nombre')
                price = item.get('price', 'N/A')
                category = item.get('category', 'Sin categoría')
                response += f"✅ {name} - ${price} ({category})\n"
            
            if len(found_items) > 5:
                response += f"\n... y {len(found_items) - 5} más. ¿Cuál te interesa?"
            
            return response
        
        return None
    
    def get_item_details(self, message: str) -> Optional[str]:
        """Get detailed information about a specific item"""
        for item in self.menu_items:
            name = item.get('name', '').lower()
            if name in message.lower():
                return self.format_item_details(item)
        return None
    
    def format_item_details(self, item: Dict) -> str:
        """Format item details nicely"""
        name = item.get('name', 'Sin nombre')
        price = item.get('price', 'N/A')
        ingredients = item.get('ingredients', [])
        description = item.get('description', 'Sin descripción')
        category = item.get('category', 'Sin categoría')
        
        # Handle ingredients as list or string
        if isinstance(ingredients, list):
            ingredients_text = ', '.join(ingredients)
        else:
            ingredients_text = str(ingredients)
        
        response = f"🍽️ *{name.upper()}*\n\n"
        response += f"💰 *Precio:* ${price}\n"
        response += f"📂 *Categoría:* {category}\n"
        response += f"🥗 *Ingredientes:* {ingredients_text}\n"
        
        if description and description != 'Sin descripción':
            response += f"📝 *Descripción:* {description}\n"
        
        return response
    
    # Specific response handlers
    def get_shots(self) -> str:
        """Get all shots"""
        shots = [item for item in self.menu_items if 'shot' in item.get('category', '').lower()]
        response = "💉 *NUESTROS SHOTS:*\n\n"
        
        for shot in shots:
            name = shot.get('name', 'Sin nombre')
            price = shot.get('price', 'N/A')
            ingredients = shot.get('ingredients', [])
            
            # Handle ingredients as list or string
            if isinstance(ingredients, list):
                ingredients_text = ', '.join(ingredients)
            else:
                ingredients_text = str(ingredients)
            
            response += f"✅ {name} - ${price}\n"
            if ingredients_text:
                response += f"   🥗 {ingredients_text}\n"
            response += "\n"
        
        return response
    
    def get_juices(self) -> str:
        """Get all juices"""
        juices = [item for item in self.menu_items if 'jugos cold pressed' in item.get('category', '').lower()]
        response = "🥤 *NUESTROS JUGOS:*\n\n"
        
        for juice in juices:
            name = juice.get('name', 'Sin nombre')
            price = juice.get('price', 'N/A')
            response += f"✅ {name} - ${price}\n"
        
        return response
    
    def get_smoothies(self) -> str:
        """Get all smoothies"""
        smoothies = [item for item in self.menu_items if 'milks' in item.get('category', '').lower()]
        response = "🥛 *NUESTROS BATIDOS:*\n\n"
        
        for smoothie in smoothies:
            name = smoothie.get('name', 'Sin nombre')
            price = smoothie.get('price', 'N/A')
            response += f"✅ {name} - ${price}\n"
        
        return response
    
    def get_breakfast(self) -> str:
        """Get breakfast items"""
        breakfast = [item for item in self.menu_items if 'desayuno' in item.get('category', '').lower()]
        response = "🌅 *NUESTROS DESAYUNOS:*\n\n"
        
        for item in breakfast:
            name = item.get('name', 'Sin nombre')
            price = item.get('price', 'N/A')
            response += f"✅ {name} - ${price}\n"
        
        return response
    
    def get_lunch(self) -> str:
        """Get lunch items"""
        lunch = [item for item in self.menu_items if 'almuerzo' in item.get('category', '').lower()]
        response = "🍽️ *NUESTROS ALMUERZOS:*\n\n"
        
        for item in lunch:
            name = item.get('name', 'Sin nombre')
            price = item.get('price', 'N/A')
            response += f"✅ {name} - ${price}\n"
        
        return response
    
    def get_desserts(self) -> str:
        """Get dessert items"""
        desserts = [item for item in self.menu_items if 'postre' in item.get('category', '').lower()]
        response = "🍰 *NUESTROS POSTRES:*\n\n"
        
        for dessert in desserts:
            name = dessert.get('name', 'Sin nombre')
            price = dessert.get('price', 'N/A')
            response += f"✅ {name} - ${price}\n"
        
        return response
    
    def get_cold_drinks(self) -> str:
        """Get cold/refreshing drinks"""
        cold_drinks = [
            'citrus', 'cool melon', 'pina blizz', 'n4', 'green day', 'ez-green',
            'red roots', 'dalai lama', 'jugo de zanahoria', 'jugo celery'
        ]
        
        response = "🥤 *BEBIDAS REFRESCANTES:*\n\n"
        for drink_name in cold_drinks:
            for item in self.menu_items:
                if drink_name.lower() in item.get('name', '').lower():
                    name = item.get('name', 'Sin nombre')
                    price = item.get('price', 'N/A')
                    response += f"✅ {name} - ${price}\n"
                    break
        
        return response
    
    def get_energy_drinks(self) -> str:
        """Get energy drinks"""
        energy_drinks = [
            'flu shot', 'ginger shot', 'power maca', 'orange baby',
            'pina blizz', 'green day', 'red roots', 'dalai lama'
        ]
        
        response = "⚡ *BEBIDAS ENERGIZANTES:*\n\n"
        for drink_name in energy_drinks:
            for item in self.menu_items:
                if drink_name.lower() in item.get('name', '').lower():
                    name = item.get('name', 'Sin nombre')
                    price = item.get('price', 'N/A')
                    response += f"✅ {name} - ${price}\n"
                    break
        
        return response
    
    def get_detox_drinks(self) -> str:
        """Get detox drinks"""
        detox_drinks = [
            'n4', 'green day', 'ez-green', 'red roots', 'jugo de zanahoria', 'jugo celery'
        ]
        
        response = "🌿 *BEBIDAS DETOX:*\n\n"
        for drink_name in detox_drinks:
            for item in self.menu_items:
                if drink_name.lower() in item.get('name', '').lower():
                    name = item.get('name', 'Sin nombre')
                    price = item.get('price', 'N/A')
                    response += f"✅ {name} - ${price}\n"
                    break
        
        return response
    
    def get_prices(self) -> str:
        """Get price information"""
        return "💰 *RANGOS DE PRECIOS:*\n\n" \
               "🥤 Jugos Cold Pressed: $6.50 - $8.00\n" \
               "💉 Shots: $1.50\n" \
               "🥛 Batidos: $8.00\n" \
               "🌅 Desayunos: $3.00 - $13.00\n" \
               "🍽️ Almuerzos: $7.00 - $10.00\n" \
               "🍰 Postres: $2.00 - $5.50\n\n" \
               "¿Te interesa algún item específico?"
    
    def get_hours(self) -> str:
        """Get business hours"""
        return "\n".join(self.templates['hours'])
    
    def get_location(self) -> str:
        """Get location information with GPS links"""
        return "\n".join(self.templates['location'])
    
    def get_specific_location(self, location_name: str = None) -> str:
        """Get specific location information"""
        locations = {
            'castellana': {
                'name': 'PRANA LA CASTELLANA',
                'address': 'Avenida Mohedano, Caracas 1060, Chacao, Distrito Capital',
                'gps': 'https://maps.google.com/?q=10.4870,-66.8512',
                'hours': '7:00 AM - 11:00 PM'
            },
            'palos_grandes': {
                'name': 'PRANA LOS PALOS GRANDES',
                'address': 'Transversal 3 entre 3ra y 4ta, Los Palos Grandes, Caracas, Distrito Capital',
                'gps': 'https://maps.google.com/?q=10.4806,-66.9036',
                'hours': '7:00 AM - 11:00 PM'
            }
        }
        
        if location_name and location_name.lower() in locations:
            loc = locations[location_name.lower()]
            return f"📍 *{loc['name']}*\n\n" \
                   f"🏪 {loc['address']}\n" \
                   f"🕐 Horarios: {loc['hours']}\n" \
                   f"📱 {loc['gps']}\n\n" \
                   f"💡 Haz clic en el enlace para obtener direcciones GPS"
        
        # Return all locations if no specific location requested
        return self.get_location()
    
    def get_full_menu(self) -> str:
        """Get complete menu"""
        return "📋 *MENÚ COMPLETO PRANA JUICE BAR*\n\n" + self.knowledge_base
    
    def get_ingredients(self) -> str:
        """Get ingredients for specific item"""
        return "🥗 Para ver los ingredientes de un item específico, escribe el nombre del producto."
    
    def get_recommendations(self) -> str:
        """Get recommendations"""
        recommendations = [
            "🥤 *CITRUS* - Perfecto para refrescarse",
            "💉 *GINGER SHOT* - Energía natural",
            "🌿 *GREEN DAY* - Detox completo",
            "🍰 *CHEESECAKE DE MORA* - Postre favorito",
            "🌅 *BOWL DE CHIA* - Desayuno saludable"
        ]
        
        response = "⭐ *NUESTRAS RECOMENDACIONES:*\n\n"
        for rec in recommendations:
            response += f"✅ {rec}\n"
        
        return response
    
    def get_help_message(self) -> str:
        """Get help message"""
        return "🤔 *¿EN QUÉ PUEDO AYUDARTE?*\n\n" \
               "• Escribe 'menu' para ver categorías\n" \
               "• Pregunta por items específicos\n" \
               "• 'Que shots tienen?' - Ver shots\n" \
               "• 'Bueno para frío' - Bebidas refrescantes\n" \
               "• 'Horarios' - Horarios de atención\n" \
               "• 'Precios' - Información de precios\n\n" \
               "¿Qué te gustaría saber?"
    
    def is_positive_response(self, message: str) -> bool:
        """Check if message is a positive response"""
        positive_words = [
            'si', 'sí', 'yes', 'claro', 'por supuesto', 'ok', 'okay', 'vale', 'bueno',
            'perfecto', 'excelente', 'genial', 'me gustaría', 'me gustaria'
        ]
        return any(word in message for word in positive_words)
    
    def get_volume_info(self) -> str:
        """Get volume/size information for drinks"""
        return "🥤 *INFORMACIÓN DE TAMAÑOS:*\n\n" \
               "✅ **Jugos Cold Pressed**: Todos son de 500ml\n" \
               "✅ **Milks (Batidos)**: Todos son de 500ml\n" \
               "✅ **Shots**: 30ml cada uno\n" \
               "✅ **Berry Blend**: 500ml\n\n" \
               "Todos nuestros jugos cold pressed son de 500ml para máxima frescura y nutrientes! 🌿"
    
    def get_weight_info(self) -> str:
        """Get weight information for food items"""
        return "⚖️ *INFORMACIÓN DE PESOS:*\n\n" \
               "🍰 **Postres**: Porciones individuales\n" \
               "🥐 **Bake Goods**: Tamaños individuales\n" \
               "🌅 **Desayunos**: Porciones completas\n" \
               "🍽️ **Almuerzos**: Porciones generosas\n\n" \
               "Para información específica de algún item, escribe su nombre."
    
    def get_sugar_water_info(self) -> str:
        """Answer for added sugar or water questions"""
        return (
            "🚫 No usamos azúcar refinada añadida en ninguno de nuestros jugos ni recetas. "
            "Todos nuestros jugos son 100% naturales, sin azúcares añadidos ni agua extra.\n"
            "🍯 En nuestros postres y productos horneados, solo endulzamos con miel, dátiles o monkfruit."
        )
    
    def get_gluten_info(self) -> str:
        """Get gluten-related information"""
        return (
            "🌾 *INFORMACIÓN SOBRE GLUTEN:*\n\n"
            "No somos completamente gluten-free, pero la mayoría de nuestros productos son bajos en gluten. "
            "Nuestro único producto con trigo es nuestro pan de masa madre con fermentación de 38 horas. "
            "Si tienes alguna alergia o intolerancia al gluten, por favor, háznoslo saber para ayudarte mejor."
        )
    
    def get_drink_categories(self) -> str:
        """Get drink categories only"""
        drink_categories = [
            'jugos cold pressed', 'shots', 'milks'
        ]
        response = "🥤 *BEBIDAS DISPONIBLES:*\n\n"
        
        for i, category in enumerate(drink_categories, 1):
            emoji = self.get_category_emoji(category)
            response += f"{i}. {emoji} {category.title()}\n"
        
        response += "\n¿Qué tipo de bebida te interesa? Puedes escribir el nombre o número."
        return response
    
    def get_drink_suggestions(self) -> str:
        """Get drink suggestions for thirst-related messages"""
        return "🥤 *BEBIDAS REFRESCANTES:*\n\n" \
               "✅ **CITRUS** - Zumo de piña, naranja, toronja y hierbabuena\n" \
               "✅ **COOL MELON** - Patilla, pepino y hierbabuena\n" \
               "✅ **GREEN DAY** - Celery, pepino, lechuga, cilantro, limón y jengibre\n" \
               "✅ **N4** - Celery, pepino, manzana verde y limón\n" \
               "✅ **GINGER SHOT** - Energía natural de jengibre\n\n" \
               "Todos nuestros jugos son de 500ml y 100% naturales! 🌿"

    def get_health_recommendations(self) -> str:
        """Get health recommendations for illness/symptoms"""
        return "🏥 *RECOMENDACIONES PARA TU SALUD:*\n\n" \
               "💉 **GINGER SHOT** - Antiinflamatorio natural, perfecto para gripe y resfriados\n" \
               "🥤 **IMMUNITY** - Con naranja, parchita, limón, jengibre y cayena para fortalecer el sistema inmune\n" \
               "🌿 **GREEN DAY** - Detox completo con celery, pepino, lechuga, cilantro, limón y jengibre\n" \
               "🥤 **CITRUS** - Vitamina C natural para combatir infecciones\n" \
               "💉 **FLU SHOT** - Específicamente diseñado para síntomas de gripe\n\n" \
               "Todos nuestros shots y jugos son 100% naturales y sin azúcares añadidos. ¡Te ayudarán a sentirte mejor! 🌿"
    
    def get_website_link(self) -> str:
        """Get website link and information"""
        website_info = self.templates['website']
        return '\n'.join(website_info)

# Example usage and testing
if __name__ == "__main__":
    # Initialize bot
    bot = PranaWhatsAppBot()
    
    # Test the bot
    test_messages = [
        "hola",
        "que shots tienen?",
        "que es bueno para el frío?",
        "menu",
        "jugos",
        "citrus",
        "horarios"
    ]
    
    print("🤖 *PRANA WHATSAPP BOT - TESTING*\n")
    print("=" * 50)
    
    for message in test_messages:
        print(f"👤 Usuario: {message}")
        response = bot.process_message("test_user", message)
        print(f"🤖 Bot: {response}")
        print("-" * 50) 