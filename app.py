#!/usr/bin/env python3
"""
Prana Juice Bar WhatsApp Bot - Flask Web App
"""

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from custom_whatsapp_bot import PranaWhatsAppBot
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = PranaWhatsAppBot()

@app.route('/')
def home():
    """Home page"""
    return """
    <h1>🥤 Prana Juice Bar WhatsApp Bot</h1>
    <p>Bot is running! Send messages to your WhatsApp number.</p>
    <p>Webhook URL: /webhook</p>
    """

@app.route('/webhook', methods=['POST'])
def webhook():
    """WhatsApp webhook endpoint"""
    try:
        # Get message data from Twilio
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        logger.info(f"📱 Message from {from_number}: {incoming_msg}")
        
        # Process message with our bot
        response_text = bot.process_message(from_number, incoming_msg)
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(response_text)
        
        logger.info(f"🤖 Bot response: {response_text[:100]}...")
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"❌ Error processing message: {e}")
        resp = MessagingResponse()
        resp.message("Lo siento, hubo un error. Por favor intenta de nuevo.")
        return str(resp)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "bot": "running"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 