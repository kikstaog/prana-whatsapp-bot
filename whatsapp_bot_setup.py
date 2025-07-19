#!/usr/bin/env python3
"""
Prana Juice Bar WhatsApp Bot Setup Script
This script helps set up the WhatsApp bot by processing menu data and integrating with existing Prana ML data.
"""

import os
import json
import pandas as pd
from PIL import Image
import pytesseract
import re
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PranaWhatsAppBotSetup:
    def __init__(self, data_dir: str = "data", output_dir: str = "bot_data"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.menu_items = []
        self.inventory_data = None
        self.sales_data = None
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_manual_menu_data(self) -> List[Dict[str, Any]]:
        """
        Load menu data from manually created menu_template.json
        """
        logger.info("Loading manual menu data...")
        
        menu_file = "menu_template.json"
        
        if os.path.exists(menu_file):
            try:
                with open(menu_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    menu_items = data.get("menu_items", [])
                    logger.info(f"Loaded {len(menu_items)} menu items from manual entry")
                    self.menu_items = menu_items
                    return menu_items
            except Exception as e:
                logger.error(f"Error loading menu data: {str(e)}")
        else:
            logger.warning(f"Menu file {menu_file} not found. Please run add_menu_items.py first.")
        
        return []
    
    def process_menu_images(self, menu_images_dir: str = None) -> List[Dict[str, Any]]:
        """
        Process menu images (menu1.jpg to menu8.jpg) and extract menu items
        This is kept for compatibility but manual entry is preferred
        """
        logger.info("Processing menu images...")
        
        if menu_images_dir is None:
            menu_images_dir = "menu_images"
        
        menu_items = []
        
        # Process each menu image
        for i in range(1, 9):
            image_path = os.path.join(menu_images_dir, f"menu{i}.jpg")
            
            if not os.path.exists(image_path):
                logger.warning(f"Menu image {image_path} not found, skipping...")
                continue
            
            try:
                # Extract text from image using OCR
                image = Image.open(image_path)
                text = pytesseract.image_to_string(image, lang='spa')
                
                # Parse menu items from text
                items = self._parse_menu_text(text, f"menu{i}")
                menu_items.extend(items)
                
                logger.info(f"Processed menu{i}.jpg - found {len(items)} items")
                
            except Exception as e:
                logger.error(f"Error processing menu{i}.jpg: {str(e)}")
        
        self.menu_items = menu_items
        return menu_items
    
    def _parse_menu_text(self, text: str, source: str) -> List[Dict[str, Any]]:
        """
        Parse menu text and extract structured menu items
        """
        items = []
        lines = text.split('\n')
        
        current_category = "General"
        current_item = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect categories (common juice bar categories)
            if any(keyword in line.lower() for keyword in ['zumo', 'jugo', 'batido', 'smoothie', 'bowl', 'acai', 'extra']):
                current_category = line
                continue
            
            # Parse menu item (assuming format: Name - Price or Name Price)
            price_match = re.search(r'(\d+\.?\d*)', line)
            if price_match:
                # Extract item name (everything before the price)
                price = float(price_match.group(1))
                name = line[:price_match.start()].strip().rstrip('-').strip()
                
                if name:
                    item = {
                        'name': name,
                        'price': price,
                        'category': current_category,
                        'source': source,
                        'ingredients': [],  # Will be filled manually or through additional processing
                        'description': '',
                        'available': True
                    }
                    items.append(item)
        
        return items
    
    def load_inventory_data(self) -> pd.DataFrame:
        """
        Load and process inventory data from existing Prana ML files
        """
        logger.info("Loading inventory data...")
        
        # Point to the prana_ml data folder
        prana_ml_data_dir = os.path.join("..", "prana_ml", "data")
        inventory_path = os.path.join(prana_ml_data_dir, "inv_prana_may.xls")
        
        if os.path.exists(inventory_path):
            try:
                inventory = pd.read_excel(inventory_path)
                self.inventory_data = inventory
                logger.info(f"Loaded inventory data with {len(inventory)} items")
                return inventory
            except Exception as e:
                logger.error(f"Error loading inventory data: {str(e)}")
        else:
            logger.warning(f"Inventory file not found at {inventory_path}")
        
        return pd.DataFrame()
    
    def load_sales_data(self) -> pd.DataFrame:
        """
        Load and process sales data from existing Prana ML files
        """
        logger.info("Loading sales data...")
        
        # Point to the prana_ml data folder
        prana_ml_data_dir = os.path.join("..", "prana_ml", "data")
        sales_path = os.path.join(prana_ml_data_dir, "cleaned_sales.csv")
        
        if os.path.exists(sales_path):
            try:
                sales = pd.read_csv(sales_path)
                self.sales_data = sales
                logger.info(f"Loaded sales data with {len(sales)} records")
                return sales
            except Exception as e:
                logger.error(f"Error loading sales data: {str(e)}")
        else:
            logger.warning(f"Sales file not found at {sales_path}")
        
        return pd.DataFrame()
    
    def generate_bot_config(self) -> Dict[str, Any]:
        """
        Generate Botpress configuration
        """
        config = {
            "bot_name": "Prana Juice Bot",
            "language": "es",
            "timezone": "America/Mexico_City",
            "features": {
                "nlu": True,
                "qna": True,
                "analytics": True,
                "whatsapp": True
            },
            "menu_categories": self._get_menu_categories(),
            "total_menu_items": len(self.menu_items),
            "inventory_items": len(self.inventory_data) if self.inventory_data is not None else 0,
            "sales_records": len(self.sales_data) if self.sales_data is not None else 0
        }
        
        return config
    
    def _get_menu_categories(self) -> List[str]:
        """
        Extract unique menu categories
        """
        if not self.menu_items:
            return []
        
        categories = list(set(item['category'] for item in self.menu_items))
        return sorted(categories)
    
    def generate_response_templates(self) -> Dict[str, Any]:
        """
        Generate Spanish response templates for the bot
        """
        templates = {
            "welcome": [
                "¡Hola! Bienvenido a Prana Juice Bar 🥤",
                "¿En qué puedo ayudarte hoy?",
                "Puedo mostrarte nuestro menú, ayudarte con tu pedido, o responder cualquier pregunta."
            ],
            "menu_intro": [
                "Aquí tienes nuestro menú delicioso:",
                "¿Qué te gustaría probar hoy?"
            ],
            "order_confirmation": [
                "¡Perfecto! Tu pedido ha sido confirmado.",
                "Te enviaremos una confirmación por WhatsApp.",
                "¿Necesitas algo más?"
            ],
            "hours": [
                "Nuestros horarios de atención:",
                "Lunes a Viernes: 8:00 AM - 8:00 PM",
                "Sábados y Domingos: 9:00 AM - 7:00 PM"
            ],
            "location": [
                "Nos encuentras en:",
                "[Dirección de Prana Juice Bar]",
                "¡Te esperamos!"
            ],
            "support": [
                "¿Necesitas ayuda?",
                "Puedes contactarnos directamente o hablar con nuestro equipo.",
                "¿En qué puedo ayudarte?"
            ]
        }
        
        return templates
    
    def generate_menu_structure(self) -> Dict[str, Any]:
        """
        Generate structured menu data for the bot
        """
        if not self.menu_items:
            return {}
        
        menu_structure = {}
        
        for item in self.menu_items:
            category = item['category']
            if category not in menu_structure:
                menu_structure[category] = []
            
            menu_structure[category].append({
                'name': item['name'],
                'price': item['price'],
                'available': item['available'],
                'description': item.get('description', ''),
                'ingredients': item.get('ingredients', [])
            })
        
        return menu_structure
    
    def save_bot_data(self):
        """
        Save all processed data for bot implementation
        """
        logger.info("Saving bot data...")
        
        # Save menu items
        menu_file = os.path.join(self.output_dir, "menu_items.json")
        with open(menu_file, 'w', encoding='utf-8') as f:
            json.dump(self.menu_items, f, ensure_ascii=False, indent=2)
        
        # Save bot configuration
        config_file = os.path.join(self.output_dir, "bot_config.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.generate_bot_config(), f, ensure_ascii=False, indent=2)
        
        # Save response templates
        templates_file = os.path.join(self.output_dir, "response_templates.json")
        with open(templates_file, 'w', encoding='utf-8') as f:
            json.dump(self.generate_response_templates(), f, ensure_ascii=False, indent=2)
        
        # Save menu structure
        menu_structure_file = os.path.join(self.output_dir, "menu_structure.json")
        with open(menu_structure_file, 'w', encoding='utf-8') as f:
            json.dump(self.generate_menu_structure(), f, ensure_ascii=False, indent=2)
        
        # Save inventory data summary
        if self.inventory_data is not None:
            inventory_summary = {
                'total_items': len(self.inventory_data),
                'columns': list(self.inventory_data.columns),
                'sample_data': self.inventory_data.head(5).to_dict('records')
            }
            inventory_file = os.path.join(self.output_dir, "inventory_summary.json")
            with open(inventory_file, 'w', encoding='utf-8') as f:
                json.dump(inventory_summary, f, ensure_ascii=False, indent=2)
        
        # Save sales data summary
        if self.sales_data is not None:
            sales_summary = {
                'total_records': len(self.sales_data),
                'columns': list(self.sales_data.columns),
                'sample_data': self.sales_data.head(5).to_dict('records')
            }
            sales_file = os.path.join(self.output_dir, "sales_summary.json")
            with open(sales_file, 'w', encoding='utf-8') as f:
                json.dump(sales_summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Bot data saved to {self.output_dir}/")
    
    def generate_setup_report(self) -> str:
        """
        Generate a setup report with summary information
        """
        report = f"""
# Prana Juice Bar WhatsApp Bot Setup Report

## Data Processing Summary

### Menu Items
- Total menu items processed: {len(self.menu_items)}
- Categories found: {len(self._get_menu_categories())}
- Categories: {', '.join(self._get_menu_categories())}

### Inventory Data
- Inventory items available: {len(self.inventory_data) if self.inventory_data is not None else 0}
- Data source: ../prana_ml/data/inv_prana_may.xls

### Sales Data
- Sales records available: {len(self.sales_data) if self.sales_data is not None else 0}
- Data source: ../prana_ml/data/cleaned_sales.csv

## Next Steps for Botpress Implementation

1. **Sign up for Botpress** (https://botpress.com)
2. **Create new bot project** with Spanish language
3. **Import generated data** from bot_data/ directory
4. **Set up WhatsApp Business API** integration
5. **Configure conversation flows** using the provided templates
6. **Test with sample conversations**
7. **Launch and monitor performance**

## Files Generated

- `bot_data/menu_items.json` - Structured menu data
- `bot_data/bot_config.json` - Bot configuration
- `bot_data/response_templates.json` - Spanish response templates
- `bot_data/menu_structure.json` - Organized menu by category
- `bot_data/inventory_summary.json` - Inventory data summary
- `bot_data/sales_summary.json` - Sales data summary

## Estimated Implementation Time

- **Week 1**: Botpress setup and basic flows
- **Week 2**: Menu integration and testing
- **Week 3**: Advanced features and data integration
- **Week 4**: Launch and optimization

## Cost Estimation

- Botpress Professional Plan: $200/month
- WhatsApp Business API: ~$50-100/month (depending on usage)
- Total estimated cost: $250-300/month

## Success Metrics

- Customer engagement rate
- Order conversion through bot
- Customer satisfaction scores
- Reduced manual order processing
- Revenue increase from bot channel
        """
        
        return report

def main():
    """
    Main function to run the WhatsApp bot setup
    """
    print("🚀 Prana Juice Bar WhatsApp Bot Setup")
    print("=" * 50)
    
    # Initialize setup
    setup = PranaWhatsAppBotSetup()
    
    # Load manual menu data (preferred over OCR)
    print("\n📋 Loading manual menu data...")
    menu_items = setup.load_manual_menu_data()
    
    # Load existing data
    print("\n📊 Loading existing Prana ML data...")
    setup.load_inventory_data()
    setup.load_sales_data()
    
    # Save bot data
    print("\n💾 Saving bot data...")
    setup.save_bot_data()
    
    # Generate report
    print("\n📈 Generating setup report...")
    report = setup.generate_setup_report()
    
    report_file = os.path.join(setup.output_dir, "setup_report.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Setup complete! Check the '{setup.output_dir}' folder for generated files.")
    print(f"📄 Setup report saved to: {report_file}")
    print("\n🎯 Next steps:")
    print("1. Sign up for Botpress")
    print("2. Import the generated data")
    print("3. Set up WhatsApp Business API")
    print("4. Configure conversation flows")
    print("5. Test and launch!")

if __name__ == "__main__":
    main() 