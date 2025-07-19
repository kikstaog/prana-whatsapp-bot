#!/usr/bin/env python3
"""
Test script for Prana WhatsApp Bot
"""

from custom_whatsapp_bot import PranaWhatsAppBot

def test_bot():
    """Test the bot with various messages"""
    print("🤖 Testing Prana WhatsApp Bot...")
    print("=" * 50)
    
    bot = PranaWhatsAppBot()
    
    # Test cases
    test_cases = [
        ("hola", "Greeting test"),
        ("que tienen en el menu", "Menu request test"),
        ("que shots tienen", "Shots category test"),
        ("cuanto cuesta el citrus", "Price inquiry test"),
        ("cuales son los horarios", "Hours inquiry test"),
        ("gracias", "Goodbye test")
    ]
    
    for message, description in test_cases:
        print(f"\n📝 {description}: '{message}'")
        print("-" * 30)
        response = bot.process_message("test_user", message)
        print(response)
        print("-" * 30)

if __name__ == "__main__":
    test_bot() 