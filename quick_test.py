#!/usr/bin/env python3
"""
Quick test for the fixes
"""

from custom_whatsapp_bot import PranaWhatsAppBot

def test_fixes():
    """Test the recent fixes"""
    print("🔧 Testing recent fixes...")
    print("=" * 40)
    
    bot = PranaWhatsAppBot()
    
    # Test 1: Gluten question
    print("\n1. Testing 'y glutten':")
    print("-" * 20)
    response = bot.process_message("test_user", "y glutten")
    print(response)
    
    # Test 2: Batido search
    print("\n2. Testing 'batido de fresa':")
    print("-" * 20)
    response = bot.process_message("test_user", "batido de fresa")
    print(response)
    
    # Test 3: Thirst question
    print("\n3. Testing 'tengo sed':")
    print("-" * 20)
    response = bot.process_message("test_user", "tengo sed")
    print(response)

if __name__ == "__main__":
    test_fixes() 