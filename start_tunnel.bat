@echo off
echo 🚀 Starting Prana WhatsApp Bot Tunnel...
echo.
echo This will create a public URL for your local bot
echo Press Ctrl+C to stop the tunnel
echo.
lt --port 5000 --subdomain prana-whatsapp-bot
pause 