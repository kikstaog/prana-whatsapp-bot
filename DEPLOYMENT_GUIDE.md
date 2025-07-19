# WhatsApp Bot Deployment Guide

## Option 1: Railway (Recommended - Free & Easy)

1. **Go to [Railway.app](https://railway.app)** and sign up with GitHub
2. **Create a new project** → "Deploy from GitHub repo"
3. **Select your repository** (prana_whatsapp_bot)
4. **Railway will automatically detect** it's a Python app
5. **Deploy** - Railway will use the `requirements.txt` and `Procfile`
6. **Get your URL** - Railway will give you a public URL like: `https://your-app-name.railway.app`

## Option 2: Render (Alternative - Free)

1. **Go to [Render.com](https://render.com)** and sign up
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure:**
   - **Name:** prana-whatsapp-bot
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. **Deploy** and get your URL

## Option 3: Heroku (If you have an account)

1. **Install Heroku CLI**
2. **Login:** `heroku login`
3. **Create app:** `heroku create your-app-name`
4. **Deploy:** `git push heroku main`
5. **Get URL:** `heroku info`

## Configure Twilio Webhook

Once deployed, use your public URL:

```
https://your-app-name.railway.app/webhook
```

**In Twilio Console:**
1. Go to WhatsApp → Senders
2. Select your WhatsApp number
3. Set webhook URL to: `https://your-app-name.railway.app/webhook`
4. Set HTTP method to: `POST`
5. Save

## Environment Variables

If you need to set environment variables (like API keys), add them in your deployment platform's settings.

## Testing

After deployment, test by sending a message to your Twilio WhatsApp number. You should see logs in your deployment platform's dashboard. 