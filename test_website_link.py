#!/usr/bin/env python3
"""
Test Website Link Functionality for Prana WhatsApp Bot
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from custom_whatsapp_bot import PranaWhatsAppBot

def test_website_link():
    """Test the website link functionality"""
    print("🌐 Testing Website Link Functionality")
    print("=" * 50)
    
    # Initialize bot
    bot = PranaWhatsAppBot()
    
    # Test messages that should trigger website link
    test_messages = [
        "sitio web",
        "website",
        "pagina web",
        "página web",
        "web",
        "online",
        "ordenar online",
        "pedir online",
        "comprar online",
        "menu online",
        "menú online"
    ]
    
    print("📱 Testing website link triggers:")
    print()
    
    for message in test_messages:
        print(f"👤 Usuario: '{message}'")
        response = bot.process_message("test_user", message)
        print(f"🤖 Bot: {response}")
        print("-" * 50)
        print()
    
    # Test other functionality to make sure it still works
    print("🔍 Testing other functionality still works:")
    print()
    
    other_tests = [
        "hola",
        "menu",
        "horarios",
        "precios"
    ]
    
    for message in other_tests:
        print(f"👤 Usuario: '{message}'")
        response = bot.process_message("test_user", message)
        print(f"🤖 Bot: {response}")
        print("-" * 50)
        print()

if __name__ == "__main__":
    test_website_link() 