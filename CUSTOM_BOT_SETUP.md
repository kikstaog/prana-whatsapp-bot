# 🚀 Custom WhatsApp Bot Setup Guide

## Overview

This custom WhatsApp bot replaces Botpress with a **faster, cheaper, and more flexible** solution. It uses your existing knowledge base and menu data to provide intelligent responses in Spanish.

## ✅ What You Get

- **Full control** over responses and behavior
- **100% Spanish** responses (no more English!)
- **All your menu data** already integrated
- **Multiple integration options** (Twilio, pywhatkit, webhooks)
- **Much cheaper** than Botpress ($5-20/month vs $50-200/month)
- **No platform limitations** or messy UI

## 🛠️ Quick Setup

### 1. Install Dependencies

```bash
cd prana_whatsapp_bot
pip install -r requirements_whatsapp_bot.txt
```

### 2. Test the Bot Locally

```bash
python custom_whatsapp_bot.py
```

This will run a test showing the bot's responses to common questions.

### 3. Test Interactive Mode

```bash
python whatsapp_integration.py test
```

This starts an interactive chat where you can test the bot responses.

## 🔗 WhatsApp Integration Options

### Option 1: Twilio (Recommended - Professional)

**Cost:** ~$0.005 per message
**Setup Time:** 30 minutes
**Reliability:** High

1. **Sign up for Twilio:**
   - Go to [twilio.com](https://twilio.com)
   - Create account and get WhatsApp Business API access

2. **Get credentials:**
   ```bash
   export TWILIO_ACCOUNT_SID='your_account_sid'
   export TWILIO_AUTH_TOKEN='your_auth_token'
   export TWILIO_WHATSAPP_NUMBER='whatsapp:+1234567890'
   ```

3. **Run with Twilio:**
   ```python
   from whatsapp_integration import WhatsAppIntegration
   
   integration = WhatsAppIntegration("twilio")
   integration.send_message("+1234567890", "¡Hola desde Prana!")
   ```

### Option 2: pywhatkit (Free - Development)

**Cost:** Free
**Setup Time:** 10 minutes
**Reliability:** Medium (requires browser)

```bash
pip install pywhatkit
```

```python
from whatsapp_integration import WhatsAppIntegration

integration = WhatsAppIntegration("pywhatkit")
integration.send_message("1234567890", "¡Hola desde Prana!")
```

### Option 3: Webhook (Custom - Advanced)

**Cost:** Server hosting only
**Setup Time:** 1-2 hours
**Reliability:** High

1. **Deploy to server:**
   ```bash
   # Deploy to Heroku, Railway, or your own server
   git push heroku main
   ```

2. **Set webhook URL:**
   - URL: `https://yourdomain.com/webhook`
   - Configure in WhatsApp Business API

3. **Start server:**
   ```bash
   python whatsapp_integration.py
   ```

## 🧪 Testing Your Bot

### Test Common Questions

The bot handles these questions perfectly:

- ✅ "que shots tienen?"
- ✅ "que es bueno para el frío?"
- ✅ "menu"
- ✅ "jugos"
- ✅ "citrus"
- ✅ "horarios"
- ✅ "precios"
- ✅ "recomendaciones"

### Test via API

```bash
curl -X POST http://localhost:5000/test \
  -H "Content-Type: application/json" \
  -d '{"message": "que shots tienen?", "user_id": "test_user"}'
```

## 📊 Bot Features

### ✅ What Works (Better than Botpress)

1. **Perfect Spanish responses** - No more English!
2. **All menu categories** - 12 categories with emojis
3. **Smart search** - Finds items by name or ingredients
4. **Category filtering** - "jugos", "shots", "desayunos", etc.
5. **Price information** - Complete price ranges
6. **Business hours** - Updated schedule (7am-10pm Sun/Mon, 7am-11pm Tue-Sat)
7. **Recommendations** - Curated suggestions
8. **Item details** - Full ingredient and description info

### 🎯 Response Examples

**User:** "que shots tienen?"
**Bot:** 
```
💉 NUESTROS SHOTS:

✅ flu shot - $1.50
   🥗 jengibre, limon, cayena

✅ ginger shot - $1.50
   🥗 jengibre

✅ power maca - $1.50
   🥗 pina, limon, maca, jengibre

✅ orange baby - $1.50
   🥗 naranja, jengibre, limon, miel
```

**User:** "que es bueno para el frío?"
**Bot:**
```
🥤 BEBIDAS REFRESCANTES:

✅ CITRUS - $6.50
✅ Cool Melon - $6.50
✅ PINA BLIZZ - $6.50
✅ N4 - $6.50
✅ GREEN DAY - $6.50
✅ ez-green - $6.50
✅ red roots - $6.50
✅ dalai lama - $6.50
✅ jugo de zanahoria - $8.00
✅ jugo celery - $8.00
```

## 💰 Cost Comparison

| Platform | Monthly Cost | Setup Time | Control | Spanish Support |
|----------|-------------|------------|---------|-----------------|
| **Custom Bot** | $5-20 | 1-2 hours | Full | ✅ Perfect |
| Botpress | $50-200 | 4-8 hours | Limited | ❌ Generic English |
| Rasa | $20-100 | 10+ hours | Full | ⚠️ Complex |

## 🚀 Deployment Options

### 1. Heroku (Easiest)

```bash
# Create Heroku app
heroku create prana-whatsapp-bot

# Add buildpack
heroku buildpacks:add heroku/python

# Deploy
git add .
git commit -m "Deploy custom WhatsApp bot"
git push heroku main

# Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
```

### 2. Railway (Recommended)

```bash
# Connect GitHub repo to Railway
# Railway will auto-deploy on push
```

### 3. Your Own Server

```bash
# Install dependencies
pip install -r requirements_whatsapp_bot.txt

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 whatsapp_integration:app
```

## 🔧 Customization

### Add New Responses

Edit `custom_whatsapp_bot.py`:

```python
def get_new_feature(self) -> str:
    """Add new response handler"""
    return "Tu nueva respuesta aquí"
```

### Update Menu Data

Edit `bot_data/menu_items.json` or use the existing scripts:

```bash
python add_menu_items.py
```

### Modify Templates

Edit `bot_data/response_templates.json`:

```json
{
  "welcome": [
    "¡Hola! Bienvenido a Prana Juice Bar 🥤",
    "Tu mensaje personalizado aquí"
  ]
}
```

## 🎯 Next Steps

1. **Choose integration method** (Twilio recommended)
2. **Test locally** with `python whatsapp_integration.py test`
3. **Deploy to server** (Heroku/Railway)
4. **Connect WhatsApp Business API**
5. **Go live!** 🚀

## 🆘 Troubleshooting

### Common Issues

**Bot not responding:**
- Check if data files are loaded correctly
- Verify menu_items.json exists
- Check logs for errors

**WhatsApp integration not working:**
- Verify Twilio credentials
- Check phone number format
- Ensure webhook URL is accessible

**Responses in English:**
- Check response_templates.json
- Verify Spanish text in menu data

### Get Help

- Check logs: `tail -f bot.log`
- Test individual functions in Python console
- Verify data files are UTF-8 encoded

## 🎉 Success!

Your custom WhatsApp bot is now ready to replace Botpress with:

- ✅ **Better Spanish responses**
- ✅ **Full control over behavior**
- ✅ **Much lower cost**
- ✅ **All your menu data integrated**
- ✅ **Professional reliability**

**Ready to deploy?** Choose your integration method and get started! 🚀 