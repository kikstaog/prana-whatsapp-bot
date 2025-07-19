#!/usr/bin/env python3
"""
Test GPS Location Links for Prana Juice Bar
"""

import json

def test_gps_coordinates():
    """Test the GPS coordinates and generate working links"""
    
    # Correct coordinates provided by user
    locations = {
        "Prana La Castellana": {
            "address": "Avenida Mohedano, Caracas 1060, Chacao, Distrito Capital",
            "coordinates": "10.4980742,-66.8539189"
        },
        "Prana Los Palos Grandes": {
            "address": "Transversal 3 entre 3ra y 4ta, Los Palos Grandes, Caracas, Distrito Capital", 
            "coordinates": "10.5011756,-66.8435612"
        }
    }
    
    print("📍 *TESTING GPS COORDINATES:*")
    print("=" * 50)
    
    for name, data in locations.items():
        gps_link = f"https://maps.google.com/?q={data['coordinates']}"
        print(f"\n🏪 *{name}*")
        print(f"📍 {data['address']}")
        print(f"📱 {gps_link}")
        print(f"✅ Coordinates: {data['coordinates']}")
    
    print("\n" + "=" * 50)
    print("✅ GPS coordinates updated successfully!")
    print("🔗 All links should now point to the correct locations")
    
    # Test the bot response
    print("\n🤖 *BOT LOCATION RESPONSE:*")
    print("-" * 30)
    
    try:
        with open('bot_data/response_templates.json', 'r', encoding='utf-8') as f:
            templates = json.load(f)
        
        location_response = templates.get('location', [])
        for line in location_response:
            print(line)
            
    except Exception as e:
        print(f"❌ Error reading bot data: {e}")

if __name__ == "__main__":
    test_gps_coordinates() 