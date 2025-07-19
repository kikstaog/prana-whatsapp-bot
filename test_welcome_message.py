#!/usr/bin/env python3
"""
Test Updated Welcome Message with Website Link
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from custom_whatsapp_bot import PranaWhatsAppBot

def test_welcome_message():
    """Test the updated welcome message"""
    print("🤖 Testing Updated Welcome Message")
    print("=" * 60)
    
    # Initialize bot
    bot = PranaWhatsAppBot()
    
    # Test the welcome message
    print("👤 Usuario: 'hola'")
    response = bot.process_message("new_user", "hola")
    print("🤖 Bot:")
    print(response)
    print("=" * 60)
    
    # Test with a different greeting
    print("\n👤 Usuario: 'buenos dias'")
    response = bot.process_message("new_user", "buenos dias")
    print("🤖 Bot:")
    print(response)
    print("=" * 60)

if __name__ == "__main__":
    test_welcome_message() 