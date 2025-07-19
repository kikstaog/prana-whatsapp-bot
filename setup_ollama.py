#!/usr/bin/env python3
"""
Ollama Setup Script for Prana Juice Bar WhatsApp Bot
Helps install and configure Ollama for enhanced bot functionality
"""

import os
import sys
import subprocess
import requests
import json
import time
from typing import Optional

def check_ollama_installed() -> bool:
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ollama_windows():
    """Install Ollama on Windows"""
    print("🔄 Installing Ollama on Windows...")
    
    # Download and install Ollama
    install_url = "https://ollama.ai/download/ollama-windows-amd64.exe"
    
    try:
        # Download installer
        print("📥 Downloading Ollama installer...")
        response = requests.get(install_url, stream=True)
        installer_path = "ollama-installer.exe"
        
        with open(installer_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Run installer
        print("🔧 Running Ollama installer...")
        subprocess.run([installer_path, '/S'], check=True)
        
        # Clean up
        os.remove(installer_path)
        
        print("✅ Ollama installed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error installing Ollama: {e}")
        print("\n📋 Manual installation instructions:")
        print("1. Visit https://ollama.ai/download")
        print("2. Download the Windows installer")
        print("3. Run the installer and follow the prompts")
        print("4. Restart your terminal/command prompt")
        return False

def install_ollama_mac():
    """Install Ollama on macOS"""
    print("🔄 Installing Ollama on macOS...")
    
    try:
        # Use curl to install Ollama
        install_command = "curl -fsSL https://ollama.ai/install.sh | sh"
        subprocess.run(install_command, shell=True, check=True)
        
        print("✅ Ollama installed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error installing Ollama: {e}")
        print("\n📋 Manual installation instructions:")
        print("1. Visit https://ollama.ai/download")
        print("2. Download the macOS installer")
        print("3. Run the installer and follow the prompts")
        return False

def install_ollama_linux():
    """Install Ollama on Linux"""
    print("🔄 Installing Ollama on Linux...")
    
    try:
        # Use curl to install Ollama
        install_command = "curl -fsSL https://ollama.ai/install.sh | sh"
        subprocess.run(install_command, shell=True, check=True)
        
        print("✅ Ollama installed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error installing Ollama: {e}")
        print("\n📋 Manual installation instructions:")
        print("1. Visit https://ollama.ai/download")
        print("2. Follow the Linux installation instructions")
        print("3. Or run: curl -fsSL https://ollama.ai/install.sh | sh")
        return False

def start_ollama_service():
    """Start Ollama service"""
    print("🚀 Starting Ollama service...")
    
    try:
        # Start Ollama
        subprocess.run(['ollama', 'serve'], start_new_session=True)
        
        # Wait a moment for service to start
        time.sleep(3)
        
        # Test connection
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service started successfully!")
            return True
        else:
            print("⚠️ Ollama service may not be running properly")
            return False
            
    except Exception as e:
        print(f"❌ Error starting Ollama service: {e}")
        return False

def download_model(model_name: str = "llama2") -> bool:
    """Download Ollama model"""
    print(f"📥 Downloading {model_name} model...")
    
    try:
        # Download the model
        subprocess.run(['ollama', 'pull', model_name], check=True)
        print(f"✅ {model_name} model downloaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading {model_name} model: {e}")
        return False

def test_ollama_connection() -> bool:
    """Test Ollama connection and model availability"""
    print("🔍 Testing Ollama connection...")
    
    try:
        # Test basic connection
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Cannot connect to Ollama service")
            return False
        
        # Check available models
        models = response.json().get('models', [])
        model_names = [model['name'] for model in models]
        
        print(f"📋 Available models: {model_names}")
        
        # Test with llama2 model
        if 'llama2' in model_names:
            print("✅ llama2 model is available")
            return True
        else:
            print("⚠️ llama2 model not found, downloading...")
            return download_model("llama2")
            
    except Exception as e:
        print(f"❌ Error testing Ollama connection: {e}")
        return False

def test_model_response() -> bool:
    """Test model response generation"""
    print("🧪 Testing model response...")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": "Hola, ¿cómo estás?",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('response'):
                print("✅ Model response test successful!")
                return True
            else:
                print("❌ No response from model")
                return False
        else:
            print(f"❌ Model test failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing model response: {e}")
        return False

def main():
    """Main setup function"""
    print("🤖 Ollama Setup for Prana Juice Bar WhatsApp Bot")
    print("=" * 60)
    
    # Check if Ollama is already installed
    if check_ollama_installed():
        print("✅ Ollama is already installed")
    else:
        print("📦 Ollama not found, installing...")
        
        # Detect OS and install
        if sys.platform.startswith('win'):
            if not install_ollama_windows():
                print("❌ Failed to install Ollama")
                return
        elif sys.platform.startswith('darwin'):
            if not install_ollama_mac():
                print("❌ Failed to install Ollama")
                return
        else:
            if not install_ollama_linux():
                print("❌ Failed to install Ollama")
                return
    
    # Start Ollama service
    if not start_ollama_service():
        print("❌ Failed to start Ollama service")
        return
    
    # Test connection
    if not test_ollama_connection():
        print("❌ Failed to connect to Ollama")
        return
    
    # Test model response
    if not test_model_response():
        print("❌ Failed to test model response")
        return
    
    print("\n🎉 Ollama setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the enhanced bot: python enhanced_whatsapp_bot.py")
    print("2. The bot will automatically use Ollama for natural responses")
    print("3. If Ollama fails, it will fallback to the rule-based system")
    print("\n💡 Tips:")
    print("- Keep Ollama running in the background")
    print("- You can use different models: llama2, llama2:7b, llama2:13b")
    print("- The bot will automatically detect if Ollama is available")

if __name__ == "__main__":
    main() 