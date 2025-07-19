#!/usr/bin/env python3
"""
Test real Prana locations
"""

from custom_whatsapp_bot import PranaWhatsAppBot

def test_real_locations():
    """Test the real Prana locations"""
    print("📍 TESTING REAL PRANA LOCATIONS")
    print("=" * 50)
    
    bot = PranaWhatsAppBot()
    
    # Test scenarios for real locations
    test_cases = [
        ("direccion", "All locations with GPS links"),
        ("castellana", "Prana La Castellana location"),
        ("palos grandes", "Prana Los Palos Grandes location"),
        ("prana castellana", "Prana La Castellana location"),
        ("prana los palos grandes", "Prana Los Palos Grandes location"),
    ]
    
    for message, expected in test_cases:
        print(f"\n📱 Testing: '{message}'")
        print(f"   Expected: {expected}")
        response = bot.process_message("test_user", message)
        
        # Check if GPS links are present
        if "maps.google.com" in response:
            print(f"   ✅ GPS LINKS FOUND!")
        else:
            print(f"   ❌ No GPS links found")
        
        print(f"   Response preview: {response[:150]}...")
        print("-" * 50)

if __name__ == "__main__":
    test_real_locations() 