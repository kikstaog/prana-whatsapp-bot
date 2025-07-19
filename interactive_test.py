#!/usr/bin/env python3
"""
Interactive Test for Prana WhatsApp Bot
Simulates a real WhatsApp conversation
"""

from custom_whatsapp_bot import PranaWhatsAppBot
import time

def interactive_test():
    """Interactive test simulating WhatsApp conversation"""
    print("🥤 PRANA JUICE BAR - WHATSAPP BOT TEST")
    print("=" * 50)
    print("Simulando una conversación de WhatsApp...")
    print("Escribe 'salir' para terminar")
    print("=" * 50)
    
    # Initialize bot
    bot = PranaWhatsAppBot()
    user_id = "test_user_123"
    
    # Simulate WhatsApp interface
    print(f"\n📱 WhatsApp - Prana Juice Bar")
    print(f"🟢 En línea")
    print("-" * 30)
    
    while True:
        try:
            # Get user input
            user_message = input("\n👤 Tú: ").strip()
            
            if user_message.lower() in ['salir', 'exit', 'quit', 'bye']:
                print("\n🤖 Prana: ¡Gracias por visitar Prana Juice Bar! 🌿")
                print("¡Esperamos verte pronto! ¡Que tengas un día saludable! 🥤")
                break
            
            if not user_message:
                continue
            
            # Process with bot
            print("\n🤖 Prana: ", end="")
            
            # Simulate typing delay
            time.sleep(0.5)
            
            # Get bot response
            response = bot.process_message(user_id, user_message)
            
            # Print response with WhatsApp-like formatting
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n🤖 Prana: ¡Hasta luego! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("🤖 Prana: Lo siento, hubo un error. ¿Puedes intentar de nuevo?")

def quick_test():
    """Quick test with predefined messages"""
    print("🚀 QUICK TEST - PRANA BOT")
    print("=" * 40)
    
    bot = PranaWhatsAppBot()
    user_id = "quick_test_user"
    
    test_messages = [
        "hola",
        "que tienen en el menu",
        "jugos cold pressed",
        "cuanto cuesta el citrus",
        "que shots tienen",
        "cuales son los horarios",
        "gracias"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. 👤 Tú: {message}")
        print("🤖 Prana:", end=" ")
        response = bot.process_message(user_id, message)
        print(response)
        print("-" * 40)
        time.sleep(1)

if __name__ == "__main__":
    print("Elige el tipo de test:")
    print("1. Test interactivo (conversación real)")
    print("2. Test rápido (mensajes predefinidos)")
    
    choice = input("\nOpción (1 o 2): ").strip()
    
    if choice == "2":
        quick_test()
    else:
        interactive_test() 