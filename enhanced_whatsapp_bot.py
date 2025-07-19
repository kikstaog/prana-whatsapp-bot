#!/usr/bin/env python3
"""
Prana Juice Bar Enhanced WhatsApp Bot
Enhanced version with Ollama LLM integration and fallback to rule-based system
"""

import json
import re
import random
import time
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedPranaWhatsAppBot:
    def __init__(self, use_ollama: bool = True, ollama_model: str = "llama2", ollama_url: str = "http://localhost:11434"):
        """
        Initialize the enhanced bot with Ollama integration
        
        Args:
            use_ollama: Whether to use Ollama LLM (default: True)
            ollama_model: Ollama model to use (default: "llama2")
            ollama_url: Ollama server URL (default: "http://localhost:11434")
        """
        self.use_ollama = use_ollama
        self.ollama_model = ollama_model
        self.ollama_url = ollama_url
        self.ollama_available = False
        
        # Load original bot data
        self.load_data()
        self.setup_responses()
        self.conversation_history = {}
        
        # Test Ollama availability
        if self.use_ollama:
            self.test_ollama_connection()
    
    def test_ollama_connection(self):
        """Test if Ollama is available and working"""
        try:
            # Test basic connection
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                # Test if model is available
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                if self.ollama_model in model_names:
                    self.ollama_available = True
                    logger.info(f"✅ Ollama connection successful with model: {self.ollama_model}")
                else:
                    logger.warning(f"⚠️ Ollama available but model '{self.ollama_model}' not found. Available models: {model_names}")
                    logger.info("🔄 Falling back to rule-based system")
            else:
                logger.warning(f"⚠️ Ollama connection failed with status: {response.status_code}")
                logger.info("🔄 Falling back to rule-based system")
                
        except Exception as e:
            logger.warning(f"⚠️ Ollama connection failed: {e}")
            logger.info("🔄 Falling back to rule-based system")
    
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
            'Jugos Cold Pressed': ['jugos', 'zumo', 'zumo fresco', 'cold pressed', 'citrus', 'immunity'],
            'Shots': ['shot', 'flu shot', 'ginger shot', 'power maca', 'orange baby'],
            'Desayunos': ['desayuno', 'breakfast', 'bowl de chia', 'pancakes', 'tostada', 'berry blend'],
            'Almuerzos': ['almuerzo', 'lunch', 'bowl', 'wrap', 'panini', 'ensalada'],
            'Bake Goods': ['bake', 'muffin', 'bolitas', 'energy balls'],
            'Postres': ['postre', 'dessert', 'trufa', 'cheesecake', 'cookies'],
            'Prana Cakes': ['prana cakes', 'brownie', 'banana bread', 'cookie pie'],
            'Milks': ['milky way', 'go nuts', 'batido'],
            'Extras': ['extra', 'adicional', 'complemento']
        }
        
        # Common questions and their responses
        self.qa_patterns = {
            r'(que.*shots.*tienen|tienen.*shots)': self.get_shots,
            r'(que.*jugos.*tienen|tienen.*jugos)': self.get_juices,
            r'(que.*batidos.*tienen|tienen.*batidos)': self.get_smoothies,
            r'(que.*desayunos.*tienen|tienen.*desayunos)': self.get_breakfast,
            r'(que.*almuerzos.*tienen|tienen.*almuerzos)': self.get_lunch,
            r'(que.*postres.*tienen|tienen.*postres)': self.get_desserts,
            r'bueno.*frio|frio.*bueno|refrescante': self.get_cold_drinks,
            r'energizante|energia|energetico': self.get_energy_drinks,
            r'detox|limpiar|desintoxicar': self.get_detox_drinks,
            r'precio|cuanto.*cuesta|costo': self.get_prices,
            r'(hora|horario|cierran|abren|cierre|apertura)': self.get_hours,
            r'direccion|ubicacion|donde.*estan': self.get_location,
            r'menu.*completo|todo.*menu': self.get_full_menu,
            r'ingredientes.*(\w+)': self.get_ingredients,
            r'recomendacion|recomienda|sugerencia': self.get_recommendations
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
        
        # Always start with greeting for new conversations
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
        
        # Try Ollama first if available
        if self.ollama_available and self.use_ollama:
            try:
                llm_response = self.get_ollama_response(user_id, message)
                if llm_response:
                    return self.add_follow_up_question(llm_response)
            except Exception as e:
                logger.warning(f"⚠️ Ollama response failed: {e}")
                logger.info("🔄 Falling back to rule-based system")
        
        # Fallback to rule-based system
        return self.process_with_rules(user_id, message)
    
    def get_ollama_response(self, user_id: str, message: str) -> Optional[str]:
        """Get response from Ollama LLM"""
        try:
            # Build context from conversation history and knowledge base
            context = self.build_llm_context(user_id, message)
            
            # Create prompt for Ollama
            prompt = self.create_ollama_prompt(context, message)
            
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 500
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                llm_response = result.get('response', '').strip()
                
                # Validate and clean the response
                cleaned_response = self.validate_llm_response(llm_response)
                if cleaned_response:
                    logger.info("✅ Ollama response successful")
                    return cleaned_response
                else:
                    logger.warning("⚠️ Ollama response validation failed")
                    return None
            else:
                logger.warning(f"⚠️ Ollama API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Ollama error: {e}")
            return None
    
    def build_llm_context(self, user_id: str, current_message: str) -> str:
        """Build context for LLM from conversation history and knowledge base"""
        context_parts = []
        
        # Add knowledge base
        context_parts.append("CONOCIMIENTO DEL NEGOCIO:")
        context_parts.append(self.knowledge_base)
        
        # Add menu structure
        context_parts.append("\nESTRUCTURA DEL MENÚ:")
        for category, items in self.menu_structure.items():
            context_parts.append(f"- {category}: {', '.join(items)}")
        
        # Add recent conversation history (last 3 messages)
        if user_id in self.conversation_history:
            recent_messages = self.conversation_history[user_id][-3:]
            context_parts.append("\nHISTORIAL RECIENTE:")
            for msg in recent_messages:
                context_parts.append(f"Usuario: {msg['message']}")
        
        return "\n".join(context_parts)
    
    def create_ollama_prompt(self, context: str, current_message: str) -> str:
        """Create prompt for Ollama"""
        prompt = f"""Eres Prana, el asistente virtual de Prana Juice Bar. Eres amigable, profesional y conoces todo sobre nuestro menú y servicios.

CONTEXTO:
{context}

INSTRUCCIONES:
- Responde en español de manera natural y amigable
- Usa el nombre "Prana" para referirte a ti mismo
- Proporciona información precisa sobre el menú, precios, horarios y ubicación
- Si no tienes información específica, sugiere que el cliente pregunte por el menú completo
- Mantén un tono cálido y profesional
- No inventes información que no esté en el contexto

MENSAJE ACTUAL DEL CLIENTE: {current_message}

RESPUESTA:"""
        
        return prompt
    
    def validate_llm_response(self, response: str) -> Optional[str]:
        """Validate and clean LLM response"""
        if not response or len(response.strip()) < 10:
            return None
        
        # Remove any system-like prefixes
        response = re.sub(r'^(Asistente|Bot|AI|Sistema):\s*', '', response, flags=re.IGNORECASE)
        
        # Ensure it's a reasonable length
        if len(response) > 1000:
            response = response[:1000] + "..."
        
        return response.strip()
    
    def process_with_rules(self, user_id: str, message: str) -> str:
        """Process message using the original rule-based system"""
        # Check for QA patterns (FAQ: hours, location, etc.) FIRST
        for pattern, handler in self.qa_patterns.items():
            if re.search(pattern, message, re.IGNORECASE):
                response = handler()
                return self.add_follow_up_question(response)
        
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
    
    # All the original methods from the base bot
    def is_goodbye(self, message: str) -> bool:
        """Check if message is a goodbye/farewell"""
        goodbye_words = [
            'no', 'eso es todo', 'eso es', 'nada más', 'nada mas', 'gracias', 'hasta luego',
            'hasta la vista', 'adiós', 'adios', 'chao', 'bye', 'goodbye', 'that\'s all',
            'no más', 'no mas', 'ya está', 'ya esta', 'listo', 'terminado'
        ]
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
        """Get personalized welcome message"""
        welcome_messages = self.templates['welcome']
        return f"{welcome_messages[0]}\n{welcome_messages[1]}"
    
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
            'Jugos Cold Pressed': '🥤',
            'Shots': '💉',
            'Desayunos': '🌅',
            'Almuerzos': '🍽️',
            'Bake Goods': '🥐',
            'Postres': '🍰',
            'Prana Cakes': '🧁',
            'Milks': '🥛',
            'Extras': '➕'
        }
        return emojis.get(category, '🍽️')
    
    def get_category_items(self, message: str) -> Optional[str]:
        """Get items for a specific category"""
        for category, keywords in self.categories.items():
            if any(keyword in message for keyword in keywords):
                return self.get_items_by_category(category)
        
        # Check for numeric category selection
        if re.search(r'\b[1-9]\b', message):
            categories = list(self.menu_structure.keys())
            try:
                num = int(re.search(r'\b([1-9])\b', message).group(1))
                if 1 <= num <= len(categories):
                    category = categories[num - 1]
                    return self.get_items_by_category(category)
            except:
                pass
        
        return None
    
    def get_items_by_category(self, category: str) -> str:
        """Get formatted items for a category"""
        if category not in self.menu_structure:
            return "Lo siento, no encontré esa categoría. ¿Podrías ser más específico?"
        
        items = self.menu_structure[category]
        response = f"🍽️ *{category.upper()}:*\n\n"
        
        for item in items:
            # Handle both string items and object items
            if isinstance(item, str):
                # Simple string item
                response += f"• *{item}*\n\n"
            elif isinstance(item, dict):
                # Full item object
                name = item.get('name', 'Sin nombre')
                price = item.get('price', 'Precio no disponible')
                description = item.get('description', '')
                ingredients = item.get('ingredients', [])
                
                response += f"• *{name}* - ${price}\n"
                if description:
                    response += f"  {description}\n"
                if ingredients:
                    response += f"  🥗 Ingredientes: {', '.join(ingredients)}\n"
                response += "\n"
        
        return response
    
    def search_menu_items(self, message: str) -> Optional[str]:
        """Search for specific menu items"""
        found_items = []
        
        for item in self.menu_items:
            item_name = item['name'].lower()
            if item_name in message or any(word in item_name for word in message.split()):
                found_items.append(item)
        
        if found_items:
            response = "🔍 *ITEMS ENCONTRADOS:*\n\n"
            for item in found_items[:5]:  # Limit to 5 results
                response += f"• *{item['name']}* - ${item.get('price', 'N/A')}\n"
                response += f"  {item.get('description', 'Sin descripción')}\n\n"
            
            if len(found_items) > 5:
                response += f"... y {len(found_items) - 5} más. ¿Puedes ser más específico?"
            
            return response
        
        return None
    
    def get_item_details(self, message: str) -> Optional[str]:
        """Get detailed information about a specific item"""
        for item in self.menu_items:
            if item['name'].lower() in message:
                return self.format_item_details(item)
        return None
    
    def format_item_details(self, item: Dict) -> str:
        """Format item details"""
        response = f"🍽️ *{item['name']}*\n\n"
        
        if 'price' in item:
            response += f"💰 *Precio:* ${item['price']}\n\n"
        
        if 'description' in item:
            response += f"📝 *Descripción:* {item['description']}\n\n"
        
        if 'ingredients' in item and item['ingredients']:
            response += f"🥗 *Ingredientes:* {item['ingredients']}\n"
        
        if 'category' in item:
            response += f"📂 *Categoría:* {item['category']}\n\n"
        
        return response
    
    def get_shots(self) -> str:
        """Get shots information"""
        shots = [item for item in self.menu_items if 'shot' in item['name'].lower()]
        response = "💉 *NUESTROS SHOTS:*\n\n"
        
        for shot in shots:
            response += f"• *{shot['name']}* - ${shot.get('price', 'N/A')}\n"
            response += f"  {shot.get('description', 'Sin descripción')}\n\n"
        
        return response
    
    def get_juices(self) -> str:
        """Get juices information"""
        juices = [item for item in self.menu_items if any(word in item['name'].lower() for word in ['jugo', 'zumo', 'citrus', 'immunity'])]
        response = "🥤 *NUESTROS JUGOS COLD PRESSED:*\n\n"
        
        for juice in juices:
            response += f"• *{juice['name']}* - ${juice.get('price', 'N/A')}\n"
            response += f"  {juice.get('description', 'Sin descripción')}\n\n"
        
        return response
    
    def get_smoothies(self) -> str:
        """Get smoothies information"""
        smoothies = [item for item in self.menu_items if any(word in item['name'].lower() for word in ['batido', 'milky way', 'go nuts'])]
        response = "🥛 *NUESTROS BATIDOS:*\n\n"
        
        for smoothie in smoothies:
            response += f"• *{smoothie['name']}* - ${smoothie.get('price', 'N/A')}\n"
            response += f"  {smoothie.get('description', 'Sin descripción')}\n\n"
        
        return response
    
    def get_breakfast(self) -> str:
        """Get breakfast information"""
        breakfast = [item for item in self.menu_items if any(word in item['name'].lower() for word in ['desayuno', 'breakfast', 'bowl de chia', 'pancakes', 'tostada'])]
        response = "🌅 *NUESTROS DESAYUNOS:*\n\n"
        
        for item in breakfast:
            response += f"• *{item['name']}* - ${item.get('price', 'N/A')}\n"
            response += f"  {item.get('description', 'Sin descripción')}\n\n"
        
        return response
    
    def get_lunch(self) -> str:
        """Get lunch information"""
        lunch = [item for item in self.menu_items if any(word in item['name'].lower() for word in ['almuerzo', 'lunch', 'bowl', 'wrap', 'panini', 'ensalada'])]
        response = "🍽️ *NUESTROS ALMUERZOS:*\n\n"
        
        for item in lunch:
            response += f"• *{item['name']}* - ${item.get('price', 'N/A')}\n"
            response += f"  {item.get('description', 'Sin descripción')}\n\n"
        
        return response
    
    def get_desserts(self) -> str:
        """Get desserts information"""
        desserts = [item for item in self.menu_items if any(word in item['name'].lower() for word in ['postre', 'dessert', 'trufa', 'cheesecake', 'cookies'])]
        response = "🍰 *NUESTROS POSTRES:*\n\n"
        
        for dessert in desserts:
            response += f"• *{dessert['name']}* - ${dessert.get('price', 'N/A')}\n"
            response += f"  {dessert.get('description', 'Sin descripción')}\n\n"
        
        return response
    
    def get_cold_drinks(self) -> str:
        """Get cold drinks recommendations"""
        cold_drinks = []
        for item in self.menu_items:
            if any(word in item['name'].lower() for word in ['jugo', 'zumo', 'batido', 'milky way', 'go nuts']):
                cold_drinks.append(item)
        
        response = "🥤 *BEBIDAS REFRESCANTES:*\n\n"
        for drink in cold_drinks[:5]:
            response += f"• *{drink['name']}* - ${drink.get('price', 'N/A')}\n"
            response += f"  {drink.get('description', 'Sin descripción')}\n\n"
        
        return response
    
    def get_energy_drinks(self) -> str:
        """Get energy drinks recommendations"""
        energy_drinks = []
        for item in self.menu_items:
            if any(word in item['name'].lower() for word in ['shot', 'power', 'energizante', 'maca']):
                energy_drinks.append(item)
        
        response = "⚡ *BEBIDAS ENERGIZANTES:*\n\n"
        for drink in energy_drinks:
            response += f"• *{drink['name']}* - ${drink.get('price', 'N/A')}\n"
            response += f"  {drink.get('description', 'Sin descripción')}\n\n"
        
        return response
    
    def get_detox_drinks(self) -> str:
        """Get detox drinks recommendations"""
        detox_drinks = []
        for item in self.menu_items:
            if any(word in item['name'].lower() for word in ['detox', 'limpiar', 'immunity', 'ginger']):
                detox_drinks.append(item)
        
        response = "🌿 *BEBIDAS DETOX:*\n\n"
        for drink in detox_drinks:
            response += f"• *{drink['name']}* - ${drink.get('price', 'N/A')}\n"
            response += f"  {drink.get('description', 'Sin descripción')}\n\n"
        
        return response
    
    def get_prices(self) -> str:
        """Get general pricing information"""
        return "💰 *PRECIOS:*\n\nNuestros precios varían según el producto. Los jugos cold pressed cuestan entre $8-12, los shots entre $3-5, y los alimentos entre $6-15. ¿Te gustaría ver el menú completo con precios específicos?"
    
    def get_hours(self) -> str:
        """Get business hours"""
        return "🕒 *HORARIOS:*\n\nLunes a Viernes: 7:00 AM - 7:00 PM\nSábados: 8:00 AM - 6:00 PM\nDomingos: 9:00 AM - 5:00 PM"
    
    def get_location(self) -> str:
        """Get location information"""
        return "📍 *UBICACIÓN:*\n\nEstamos ubicados en el centro de la ciudad. ¿Te gustaría que te envíe la dirección exacta?"
    
    def get_full_menu(self) -> str:
        """Get full menu"""
        return "📋 *MENÚ COMPLETO:*\n\nTe envío nuestro menú completo por categorías. ¿Qué te gustaría ver primero?"
    
    def get_ingredients(self) -> str:
        """Get ingredients information"""
        return "🥗 *INGREDIENTES:*\n\nTodos nuestros productos están hechos con ingredientes frescos y naturales. ¿Hay algún ingrediente específico que te interese conocer?"
    
    def get_recommendations(self) -> str:
        """Get recommendations"""
        recommendations = [
            "🥤 *Citrus Immunity* - Perfecto para fortalecer tu sistema inmune",
            "💉 *Ginger Shot* - Ideal para la digestión y energía",
            "🌅 *Bowl de Chia* - Desayuno nutritivo y delicioso",
            "🍽️ *Berry Blend* - Desayuno saludable y refrescante"
        ]
        
        response = "🌟 *RECOMENDACIONES DE PRANA:*\n\n"
        for rec in recommendations:
            response += f"• {rec}\n\n"
        
        return response
    
    def get_help_message(self) -> str:
        """Get help message"""
        return """🤖 *¡Hola! Soy Prana, tu asistente virtual de Prana Juice Bar!*

Puedo ayudarte con:
• 📋 Información del menú
• 💰 Precios
• 🕒 Horarios
• 📍 Ubicación
• 🌟 Recomendaciones
• 🥗 Ingredientes

Solo pregúntame lo que necesites. ¿Qué te gustaría saber?"""
    
    def is_positive_response(self, message: str) -> bool:
        """Check if message is a positive response"""
        positive_words = ['si', 'sí', 'claro', 'ok', 'okay', 'perfecto', 'excelente', 'bueno', 'vale', 'yes', 'yeah', 'yep']
        message_words = message.split()
        return any(word in message_words for word in positive_words)

def main():
    """Test the enhanced bot"""
    print("🤖 Prana Juice Bar Enhanced WhatsApp Bot")
    print("=" * 50)
    
    # Initialize bot with Ollama
    bot = EnhancedPranaWhatsAppBot(use_ollama=True)
    
    print(f"Ollama available: {bot.ollama_available}")
    print("\n💬 Chat with Prana (type 'quit' to exit):")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("👤 Tú: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'salir']:
                print("👋 ¡Hasta luego!")
                break
            
            if user_input:
                response = bot.process_message("test_user", user_input)
                print(f"🤖 Prana: {response}")
                print("-" * 50)
        
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 