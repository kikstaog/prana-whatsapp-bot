# 📱 Twilio WhatsApp Setup Guide

## Quick Setup (15 minutes)

### Step 1: Create Twilio Account
1. Go to [twilio.com](https://twilio.com)
2. Sign up for a free account (no credit card required for trial)
3. Verify your email and phone number

### Step 2: Get WhatsApp Sandbox
1. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. You'll see a WhatsApp number (like +14155238886)
3. Save this number - this is your bot's WhatsApp number

### Step 3: Join the Sandbox
1. Send the provided code to the WhatsApp number
2. Example: Send `join <code>` to +14155238886
3. You'll receive a confirmation message

### Step 4: Configure Webhook
1. In Twilio Console, go to **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
2. Set **When a message comes in** to your webhook URL:
   ```
   https://your-railway-app.railway.app/webhook
   ```
3. Set **HTTP Method** to **POST**
4. Save the configuration

### Step 5: Test Your Bot
1. Send a message to your Twilio WhatsApp number
2. Your bot should respond automatically!

## Environment Variables

Add these to your Railway project:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_whatsapp_number
```

## Production WhatsApp Business API

To move from sandbox to production:

1. **Apply for WhatsApp Business API**:
   - Go to Twilio Console → **Messaging** → **Settings** → **WhatsApp Business API**
   - Fill out the application form
   - Wait for approval (1-3 business days)

2. **Get Production Number**:
   - Once approved, you'll get a real WhatsApp Business number
   - Update your webhook URL
   - Test with real customers

## Cost Breakdown

| Service | Trial | Production |
|---------|-------|------------|
| **Twilio WhatsApp** | Free (100 messages) | $0.0049 per message |
| **Railway Hosting** | Free tier | $5/month |
| **Total** | **$0** | **~$5-10/month** |

## Troubleshooting

### Bot Not Responding
1. Check Railway logs: `railway logs`
2. Verify webhook URL is correct
3. Ensure Twilio is sending POST requests
4. Check if bot data files are loaded

### Message Not Received
1. Verify you joined the sandbox correctly
2. Check if you're sending to the right number
3. Ensure your phone has WhatsApp installed

### Spanish Characters
1. Verify UTF-8 encoding in all files
2. Check Twilio webhook encoding settings
3. Test with simple messages first

## Sample Messages to Test

```
👤 You: hola
🤖 Bot: ¡Hola! Soy Prana, tu asistente de Prana Juice Bar 🥤

👤 You: que tienen en el menu
🤖 Bot: 🥤 NUESTRAS CATEGORÍAS: 1. 🥤 Jugos Cold Pressed...

👤 You: cuanto cuesta el citrus
🤖 Bot: 💰 RANGOS DE PRECIOS: 🥤 Jugos Cold Pressed: $6.50 - $8.00...

👤 You: cuales son los horarios
🤖 Bot: Nuestros horarios de atención: Domingos y Lunes: 7:00 AM - 10:00 PM...
```

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Set up Twilio WhatsApp
3. ✅ Test basic functionality
4. 🔄 Apply for production WhatsApp Business API
5. 🔄 Add order processing features
6. 🔄 Integrate with your POS system

Your bot is ready to serve customers! 🎉 