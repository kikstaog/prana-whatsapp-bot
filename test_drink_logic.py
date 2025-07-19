#!/usr/bin/env python3
"""
Test drink logic improvements
"""

from custom_whatsapp_bot import PranaWhatsAppBot

def test_drink_logic():
    """Test the improved drink logic"""
    print("🧪 TESTING DRINK LOGIC IMPROVEMENTS")
    print("=" * 50)
    
    bot = PranaWhatsAppBot()
    
    # Test scenarios from WhatsApp
    test_cases = [
        ("para tomar que me recomiendas", "Should show drink categories"),
        ("que tiene de beber", "Should show drink categories"),
        ("que tienen de beber", "Should show drink categories"),
        ("que tienen de comer", "Should show full menu"),
        ("bebidas", "Should show drink categories"),
        ("que bebidas", "Should show drink categories"),
    ]
    
    for message, expected in test_cases:
        print(f"\n📱 Testing: '{message}'")
        print(f"   Expected: {expected}")
        response = bot.process_message("test_user", message)
        print(f"   Response: {response[:100]}...")
        print("-" * 50)

if __name__ == "__main__":
    test_drink_logic() 