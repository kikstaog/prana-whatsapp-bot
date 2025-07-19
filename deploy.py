#!/usr/bin/env python3
"""
Prana WhatsApp Bot - Deployment Script
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking deployment requirements...")
    
    # Check if files exist
    required_files = [
        'app.py',
        'custom_whatsapp_bot.py',
        'requirements_whatsapp_bot.txt',
        'Procfile',
        'runtime.txt'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing required file: {file}")
            return False
        else:
            print(f"✅ Found {file}")
    
    return True

def deploy_to_railway():
    """Deploy to Railway"""
    print("🚀 Starting Railway deployment...")
    
    # Check if Railway CLI is installed
    if run_command("railway --version", "Checking Railway CLI") is None:
        print("📦 Installing Railway CLI...")
        run_command("npm install -g @railway/cli", "Installing Railway CLI")
    
    # Login to Railway
    if run_command("railway login", "Logging into Railway") is None:
        print("❌ Railway login failed. Please run 'railway login' manually.")
        return False
    
    # Initialize project
    if run_command("railway init", "Initializing Railway project") is None:
        print("❌ Railway init failed.")
        return False
    
    # Deploy
    if run_command("railway up", "Deploying to Railway") is None:
        print("❌ Railway deployment failed.")
        return False
    
    # Get the URL
    url_result = run_command("railway domain", "Getting deployment URL")
    if url_result:
        print(f"🌐 Your bot is deployed at: {url_result.strip()}")
        print(f"📱 Webhook URL: {url_result.strip()}/webhook")
    
    return True

def main():
    """Main deployment function"""
    print("🥤 Prana WhatsApp Bot - Deployment")
    print("=" * 40)
    
    if not check_requirements():
        print("❌ Deployment requirements not met. Please fix the issues above.")
        return
    
    print("\n🚀 Ready to deploy!")
    print("This will deploy your bot to Railway (free tier available)")
    
    response = input("Continue with deployment? (y/n): ").lower()
    if response != 'y':
        print("Deployment cancelled.")
        return
    
    if deploy_to_railway():
        print("\n🎉 Deployment completed successfully!")
        print("\n📋 Next steps:")
        print("1. Copy the webhook URL above")
        print("2. Set up Twilio WhatsApp (see DEPLOYMENT_GUIDE.md)")
        print("3. Test your bot!")
    else:
        print("\n❌ Deployment failed. Check the errors above.")

if __name__ == "__main__":
    main() 