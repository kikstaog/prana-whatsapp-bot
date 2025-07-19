#!/usr/bin/env python3
"""
Simple tunnel script to expose local server without ngrok
Uses localtunnel or similar free services
"""

import subprocess
import sys
import time
import requests

def check_localtunnel():
    """Check if localtunnel is installed"""
    try:
        subprocess.run(['lt', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_localtunnel():
    """Install localtunnel"""
    print("Installing localtunnel...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'localtunnel'], check=True)
        print("✅ localtunnel installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install localtunnel")
        return False

def start_tunnel(port=5000):
    """Start localtunnel on specified port"""
    if not check_localtunnel():
        if not install_localtunnel():
            return None
    
    print(f"🚀 Starting tunnel on port {port}...")
    try:
        # Start localtunnel
        process = subprocess.Popen(
            ['lt', '--port', str(port), '--subdomain', 'prana-whatsapp-bot'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for tunnel to start
        time.sleep(3)
        
        # Get the tunnel URL
        tunnel_url = f"https://prana-whatsapp-bot.loca.lt"
        webhook_url = f"{tunnel_url}/webhook"
        
        print(f"✅ Tunnel started!")
        print(f"🌐 Tunnel URL: {tunnel_url}")
        print(f"🔗 Webhook URL: {webhook_url}")
        print(f"\n📋 Copy this webhook URL to Twilio:")
        print(f"   {webhook_url}")
        print(f"\n⏹️  Press Ctrl+C to stop the tunnel")
        
        return process, webhook_url
        
    except Exception as e:
        print(f"❌ Error starting tunnel: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Prana WhatsApp Bot - Tunnel Setup")
    print("=" * 50)
    
    result = start_tunnel(5000)
    if result:
        process, webhook_url = result
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n⏹️  Stopping tunnel...")
            process.terminate()
            print("✅ Tunnel stopped")
    else:
        print("❌ Failed to start tunnel")
        print("\n💡 Alternative: Deploy to Railway or Render (see DEPLOYMENT_GUIDE.md)") 