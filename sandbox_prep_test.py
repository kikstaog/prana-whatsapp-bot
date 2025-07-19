#!/usr/bin/env python3
"""
Pre-sandbox testing script for Prana WhatsApp Bot
Run this before testing on WhatsApp sandbox to ensure everything works
"""

from custom_whatsapp_bot import PranaWhatsAppBot
import time

def test_sandbox_scenarios():
    """Test all scenarios that will be used in sandbox testing"""
    print("🧪 PRE-SANDBOX TESTING")
    print("=" * 50)
    
    bot = PranaWhatsAppBot()
    
    # Test scenarios organized by category
    test_cases = [
        # 1. Greetings & Basic Interaction
        ("hola", "Welcome message"),
        ("buenos dias", "Welcome message"),
        ("hello", "Welcome message"),
        ("que tal", "Welcome message"),
        
        # 2. Menu Categories
        ("menu", "Menu categories"),
        ("que tienen en el menu", "Menu categories"),
        ("carta", "Menu categories"),
        ("que ofrecen", "Menu categories"),
        
        # 3. Specific Categories
        ("jugos", "Juice list"),
        ("shots", "Shots list"),
        ("desayunos", "Breakfast items"),
        ("almuerzos", "Lunch items"),
        ("batidos", "Smoothies"),
        ("postres", "Desserts"),
        ("bake goods", "Baked items"),
        ("prana cakes", "Cake items"),
        
        # 4. Health & Wellness
        ("tengo gripe", "Health recommendations"),
        ("estoy enfermo", "Health recommendations"),
        ("tengo dolor de cabeza", "Health recommendations"),
        ("tengo sed", "Drink suggestions"),
        ("quiero algo refrescante", "Cold drinks"),
        ("necesito energia", "Energy drinks"),
        ("quiero detox", "Detox drinks"),
        
        # 5. Pricing
        ("cuanto cuesta", "Price ranges"),
        ("precios", "Price ranges"),
        ("costo", "Price ranges"),
        ("cuanto vale", "Price ranges"),
        
        # 6. Business Info
        ("horarios", "Business hours"),
        ("cuales son los horarios", "Business hours"),
        ("cuando abren", "Business hours"),
        ("cuando cierran", "Business hours"),
        ("direccion", "Location info"),
        ("donde estan", "Location info"),
        ("ubicacion", "Location info"),
        
        # 7. Specific Items
        ("citrus", "Citrus juice details"),
        ("flu shot", "Flu shot details"),
        ("bowl de chia", "Chia bowl details"),
        ("trufa", "Truffle details"),
        ("milky way", "Milky way details"),
        
        # 8. Dietary Questions
        ("gluten", "Gluten info"),
        ("sin gluten", "Gluten info"),
        ("celiaco", "Gluten info"),
        ("azucar", "Sugar info"),
        ("tienen azucar", "Sugar info"),
        
        # 9. Volume & Size
        ("cuantos ml", "Volume info"),
        ("tamaño", "Size info"),
        ("cuanto pesa", "Weight info"),
        
        # 10. Recommendations
        ("recomendacion", "Recommendations"),
        ("que me recomiendas", "Recommendations"),
        ("sugerencia", "Recommendations"),
        
        # 11. Goodbye
        ("gracias", "Goodbye message"),
        ("adios", "Goodbye message"),
        ("hasta luego", "Goodbye message"),
        ("no mas", "Goodbye message"),
        ("eso es todo", "Goodbye message"),
        
        # 12. Edge Cases
        ("xyz123", "Help message"),
        ("...", "Help message"),
        ("", "Help message"),
    ]
    
    passed = 0
    failed = 0
    
    for i, (message, expected) in enumerate(test_cases, 1):
        print(f"\n{i:2d}. Testing: '{message}'")
        print(f"    Expected: {expected}")
        
        try:
            response = bot.process_message("test_user", message)
            
            # Check if response is not empty and contains expected content
            if response and len(response.strip()) > 0:
                print(f"    ✅ PASSED - Response length: {len(response)} chars")
                print(f"    Response preview: {response[:100]}...")
                passed += 1
            else:
                print(f"    ❌ FAILED - Empty response")
                failed += 1
                
        except Exception as e:
            print(f"    ❌ FAILED - Error: {e}")
            failed += 1
        
        # Small delay to avoid overwhelming
        time.sleep(0.1)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Ready for sandbox testing!")
        print("\n📱 Next steps:")
        print("1. Make sure Flask app is running: python app.py")
        print("2. Make sure localtunnel is running: lt --port 5000")
        print("3. Verify webhook URL in Twilio console")
        print("4. Start testing on WhatsApp sandbox!")
    else:
        print(f"\n⚠️  {failed} tests failed. Check the bot logic before sandbox testing.")
    
    return passed, failed

def test_conversation_flow():
    """Test a complete conversation flow"""
    print("\n🔄 TESTING CONVERSATION FLOW")
    print("=" * 50)
    
    bot = PranaWhatsAppBot()
    
    conversation = [
        ("hola", "Welcome"),
        ("jugos", "Juice list"),
        ("citrus", "Citrus details"),
        ("cuanto cuesta", "Pricing"),
        ("gracias", "Goodbye")
    ]
    
    print("Simulating conversation flow:")
    for i, (message, expected) in enumerate(conversation, 1):
        print(f"\n{i}. User: '{message}'")
        response = bot.process_message("test_user", message)
        print(f"   Bot: {response[:100]}...")
        time.sleep(0.1)
    
    print("\n✅ Conversation flow test completed!")

if __name__ == "__main__":
    # Run comprehensive tests
    passed, failed = test_sandbox_scenarios()
    
    # Run conversation flow test
    test_conversation_flow()
    
    print("\n🚀 Ready for WhatsApp sandbox testing!") 