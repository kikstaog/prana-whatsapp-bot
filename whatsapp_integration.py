#!/usr/bin/env python3
"""
WhatsApp Integration for Prana Juice Bar Bot
Multiple integration options: Twilio, pywhatkit, webhooks
"""

import json
import logging
from flask import Flask, request, jsonify
from custom_whatsapp_bot import PranaWhatsAppBot
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = PranaWhatsAppBot()

class WhatsAppIntegration:
    def __init__(self, integration_type="webhook"):
        """
        Initialize WhatsApp integration
        integration_type: "twilio", "pywhatkit", "webhook"
        """
        self.integration_type = integration_type
        self.bot = PranaWhatsAppBot()
        
    def send_message(self, phone_number: str, message: str) -> bool:
        """Send message via selected integration method"""
        try:
            if self.integration_type == "twilio":
                return self._send_via_twilio(phone_number, message)
            elif self.integration_type == "pywhatkit":
                return self._send_via_pywhatkit(phone_number, message)
            elif self.integration_type == "webhook":
                return self._send_via_webhook(phone_number, message)
            else:
                logger.error(f"Unknown integration type: {self.integration_type}")
                return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def _send_via_twilio(self, phone_number: str, message: str) -> bool:
        """Send message via Twilio WhatsApp API"""
        try:
            from twilio.rest import Client
            
            # Get credentials from environment variables
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            from_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
            
            if not all([account_sid, auth_token, from_number]):
                logger.error("Missing Twilio credentials")
                return False
            
            client = Client(account_sid, auth_token)
            
            # Format phone number for WhatsApp
            if not phone_number.startswith('whatsapp:'):
                phone_number = f"whatsapp:{phone_number}"
            if not from_number.startswith('whatsapp:'):
                from_number = f"whatsapp:{from_number}"
            
            message = client.messages.create(
                from_=from_number,
                body=message,
                to=phone_number
            )
            
            logger.info(f"Message sent via Twilio: {message.sid}")
            return True
            
        except ImportError:
            logger.error("Twilio not installed. Run: pip install twilio")
            return False
        except Exception as e:
            logger.error(f"Twilio error: {e}")
            return False
    
    def _send_via_pywhatkit(self, phone_number: str, message: str) -> bool:
        """Send message via pywhatkit (requires browser automation)"""
        try:
            import pywhatkit as pwk
            
            # pywhatkit requires phone number without country code for some regions
            # You might need to adjust this based on your location
            pwk.sendwhatmsg_instantly(
                phone_no=phone_number,
                message=message,
                wait_time=10,
                tab_close=True
            )
            
            logger.info(f"Message sent via pywhatkit to {phone_number}")
            return True
            
        except ImportError:
            logger.error("pywhatkit not installed. Run: pip install pywhatkit")
            return False
        except Exception as e:
            logger.error(f"pywhatkit error: {e}")
            return False
    
    def _send_via_webhook(self, phone_number: str, message: str) -> bool:
        """Send message via webhook (for custom integrations)"""
        # This is a placeholder for custom webhook implementations
        # You would implement your own webhook logic here
        logger.info(f"Webhook message to {phone_number}: {message}")
        return True

# Flask routes for webhook integration
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp webhook messages"""
    try:
        data = request.get_json()
        logger.info(f"Received webhook: {data}")
        
        # Extract message data (adjust based on your webhook format)
        if 'entry' in data and data['entry']:
            entry = data['entry'][0]
            if 'changes' in entry and entry['changes']:
                change = entry['changes'][0]
                if 'value' in change and 'messages' in change['value']:
                    message_data = change['value']['messages'][0]
                    
                    # Extract phone number and message
                    phone_number = message_data.get('from', '')
                    message_text = message_data.get('text', {}).get('body', '')
                    
                    # Process message with bot
                    response = bot.process_message(phone_number, message_text)
                    
                    # Send response back
                    integration = WhatsAppIntegration("webhook")
                    integration.send_message(phone_number, response)
                    
                    return jsonify({"status": "success"})
        
        return jsonify({"status": "no message found"})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "bot": "Prana Juice Bar Bot"})

@app.route('/test', methods=['POST'])
def test_bot():
    """Test endpoint for bot responses"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_id = data.get('user_id', 'test_user')
        
        response = bot.process_message(user_id, message)
        
        return jsonify({
            "status": "success",
            "message": message,
            "response": response
        })
        
    except Exception as e:
        logger.error(f"Test error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def run_local_test():
    """Run a local test of the bot"""
    print("🤖 *PRANA WHATSAPP BOT - LOCAL TEST*\n")
    print("=" * 50)
    
    integration = WhatsAppIntegration("webhook")
    
    while True:
        try:
            user_input = input("\n👤 Tú: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            # Process message
            response = bot.process_message("test_user", user_input)
            print(f"\n🤖 Bot: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def setup_environment():
    """Setup environment variables and dependencies"""
    print("🔧 *SETUP INSTRUCTIONS*\n")
    print("=" * 50)
    
    print("1. 📦 Install dependencies:")
    print("   pip install flask twilio pywhatkit")
    print()
    
    print("2. 🔑 For Twilio integration, set environment variables:")
    print("   export TWILIO_ACCOUNT_SID='your_account_sid'")
    print("   export TWILIO_AUTH_TOKEN='your_auth_token'")
    print("   export TWILIO_WHATSAPP_NUMBER='whatsapp:+1234567890'")
    print()
    
    print("3. 🌐 For webhook integration:")
    print("   - Deploy this script to a server with HTTPS")
    print("   - Set webhook URL in your WhatsApp Business API")
    print("   - URL: https://yourdomain.com/webhook")
    print()
    
    print("4. 🚀 Run the bot:")
    print("   python whatsapp_integration.py")
    print()
    
    print("5. 🧪 Test locally:")
    print("   python -c \"from whatsapp_integration import run_local_test; run_local_test()\"")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_local_test()
    elif len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_environment()
    else:
        print("🤖 Prana Juice Bar WhatsApp Bot")
        print("=" * 30)
        print("Commands:")
        print("  python whatsapp_integration.py test    - Run local test")
        print("  python whatsapp_integration.py setup   - Show setup instructions")
        print("  python whatsapp_integration.py         - Start webhook server")
        print()
        
        # Start Flask server for webhook
        print("🚀 Starting webhook server on http://localhost:5000")
        print("📝 Test endpoint: POST http://localhost:5000/test")
        print("💚 Health check: GET http://localhost:5000/health")
        print()
        
        app.run(host='0.0.0.0', port=5000, debug=True) 