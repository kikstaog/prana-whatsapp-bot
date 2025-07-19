# 🤖 Prana Juice Bar Enhanced WhatsApp Bot

## Overview

The Enhanced WhatsApp Bot for Prana Juice Bar combines the reliability of a rule-based system with the natural language capabilities of Ollama LLM. This hybrid approach ensures your bot always works, even if the AI service is unavailable.

## ✨ Features

### 🧠 AI-Powered Responses
- **Ollama Integration**: Uses local LLM for natural, contextual responses
- **Smart Fallback**: Automatically switches to rule-based system if AI fails
- **Context Awareness**: Remembers conversation history for better responses
- **Multi-language Support**: Primarily Spanish with English support

### 🛡️ Reliability & Safety
- **Always Available**: Rule-based fallback ensures 24/7 operation
- **No External Dependencies**: Ollama runs locally on your machine
- **Data Privacy**: All conversations stay on your local system
- **Graceful Degradation**: Seamless transition between AI and rules

### 🍽️ Menu & Business Intelligence
- **Complete Menu Management**: All categories, items, prices, descriptions
- **Smart Search**: Find items by name, category, or ingredients
- **Business Hours**: Real-time availability information
- **Location Services**: Address and directions
- **Recommendations**: AI-powered product suggestions

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_whatsapp_bot.txt
```

### 2. Setup Ollama (Optional but Recommended)

```bash
python setup_ollama.py
```

This will:
- Install Ollama on your system
- Download the llama2 model
- Test the connection
- Configure everything automatically

### 3. Run the Enhanced Bot

```bash
python enhanced_whatsapp_bot.py
```

## 📋 Installation Options

### Option A: Full AI Experience (Recommended)
1. Run the setup script: `python setup_ollama.py`
2. Start the enhanced bot: `python enhanced_whatsapp_bot.py`
3. Enjoy AI-powered responses with fallback safety

### Option B: Rule-Based Only
1. Skip Ollama setup
2. Run the enhanced bot: `python enhanced_whatsapp_bot.py`
3. The bot will automatically use rule-based responses

### Option C: Manual Ollama Setup
1. Visit [ollama.ai](https://ollama.ai) and download for your OS
2. Install and start Ollama: `ollama serve`
3. Download model: `ollama pull llama2`
4. Run the enhanced bot

## 🔧 Configuration

### Bot Configuration

The enhanced bot can be configured when initializing:

```python
from enhanced_whatsapp_bot import EnhancedPranaWhatsAppBot

# Full AI experience
bot = EnhancedPranaWhatsAppBot(use_ollama=True, ollama_model="llama2")

# Rule-based only
bot = EnhancedPranaWhatsAppBot(use_ollama=False)

# Custom model
bot = EnhancedPranaWhatsAppBot(ollama_model="llama2:13b")
```

### Available Models

- `llama2` (default) - Good balance of speed and quality
- `llama2:7b` - Faster, smaller model
- `llama2:13b` - Higher quality, slower responses
- `llama2:70b` - Best quality, requires more resources

## 🧪 Testing

### Interactive Testing
```bash
python enhanced_whatsapp_bot.py
```

This starts an interactive chat where you can test:
- Menu queries
- Business information
- Natural conversations
- AI vs rule-based responses

### Sample Conversations

```
👤 Tú: hola
🤖 Prana: ¡Hola! Soy Prana, tu asistente virtual de Prana Juice Bar! 🌿

👤 Tú: que jugos tienen
🤖 Prana: 🥤 NUESTROS JUGOS COLD PRESSED:
• Citrus Immunity - $10
  Refrescante combinación de cítricos con jengibre y miel
• Berry Blend - $12
  Mezcla de bayas antioxidantes con espinaca

👤 Tú: me recomiendas algo para la mañana
🤖 Prana: 🌅 Para la mañana te recomiendo nuestro Bowl de Chia con frutas frescas y granola casera. Es nutritivo, energizante y perfecto para empezar el día. También puedes probar nuestro Ginger Shot para un boost de energía natural.
```

## 📊 Performance Comparison

| Feature | Rule-Based | AI-Enhanced |
|---------|------------|-------------|
| Response Speed | ⚡⚡⚡⚡⚡ | ⚡⚡⚡ |
| Response Quality | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Reliability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Natural Language | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Setup Complexity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🔍 Troubleshooting

### Ollama Not Starting
```bash
# Check if Ollama is installed
ollama --version

# Start Ollama service
ollama serve

# Check available models
ollama list
```

### Model Download Issues
```bash
# Download specific model
ollama pull llama2

# Check download progress
ollama list
```

### Connection Problems
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Restart Ollama service
pkill ollama
ollama serve
```

### Bot Fallback Issues
- Check logs for error messages
- Verify bot data files exist in `bot_data/`
- Ensure all dependencies are installed

## 📁 File Structure

```
prana_whatsapp_bot/
├── enhanced_whatsapp_bot.py    # Main enhanced bot
├── setup_ollama.py             # Ollama setup script
├── custom_whatsapp_bot.py      # Original rule-based bot
├── requirements_whatsapp_bot.txt
├── bot_data/
│   ├── menu_items.json         # Menu items with prices
│   ├── menu_structure.json     # Category organization
│   ├── response_templates.json # Response templates
│   └── menu_knowledge_base.txt # Business knowledge
└── ENHANCED_BOT_README.md      # This file
```

## 🔄 Integration with WhatsApp

The enhanced bot can be integrated with WhatsApp using:

1. **Twilio Integration**: Use `whatsapp_integration.py`
2. **Webhook Setup**: Configure webhooks for real-time messaging
3. **Flask Server**: Run as a web service

Example integration:
```python
from enhanced_whatsapp_bot import EnhancedPranaWhatsAppBot
from flask import Flask, request

app = Flask(__name__)
bot = EnhancedPranaWhatsAppBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data['message']
    user_id = data['user_id']
    
    response = bot.process_message(user_id, user_message)
    return {'response': response}
```

## 🎯 Best Practices

### For Optimal Performance
1. **Keep Ollama Running**: Start `ollama serve` before running the bot
2. **Monitor Resources**: LLM models use significant RAM and CPU
3. **Regular Updates**: Keep Ollama and models updated
4. **Backup Data**: Regularly backup your bot data files

### For Better Responses
1. **Clear Prompts**: The bot responds better to clear, specific questions
2. **Context Matters**: Reference previous messages for better continuity
3. **Use Categories**: Ask for specific menu categories for detailed info
4. **Be Specific**: Ask about specific items for detailed descriptions

## 🆘 Support

### Common Issues
- **"Ollama not available"**: Run `python setup_ollama.py`
- **"Model not found"**: Run `ollama pull llama2`
- **"Connection failed"**: Check if `ollama serve` is running
- **"No response"**: Check bot data files in `bot_data/`

### Getting Help
1. Check the logs for error messages
2. Verify all dependencies are installed
3. Test Ollama connection manually
4. Try the rule-based fallback mode

## 🚀 Future Enhancements

- [ ] Multi-language support (English, Portuguese)
- [ ] Voice message processing
- [ ] Image recognition for menu items
- [ ] Order processing integration
- [ ] Customer feedback analysis
- [ ] Sales analytics integration

## 📄 License

This project is part of the Prana Juice Bar WhatsApp Bot system. All rights reserved.

---

**Ready to enhance your customer experience? Start with the enhanced bot today! 🚀** 