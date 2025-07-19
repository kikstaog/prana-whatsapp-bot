# 🥤 Prana Juice Bar WhatsApp Bot

A comprehensive WhatsApp AI agent bot for Prana Juice Bar, built with Botpress and integrated with existing business intelligence data.

## 📁 Project Structure

```
prana_whatsapp_bot/
├── 📋 whatsapp_bot_setup.py      # Main setup script
├── 📦 requirements_whatsapp_bot.txt  # Python dependencies
├── 📁 menu_images/               # Place menu1.jpg to menu8.jpg here
├── 📁 data/                      # Additional data files
├── 📁 bot_data/                  # Generated bot configuration files
├── 📁 docs/                      # Documentation
│   ├── whatsapp_bot_implementation.md
│   └── QUICK_START_WHATSAPP_BOT.md
└── 📄 README.md                  # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_whatsapp_bot.txt
```

### 2. Add Menu Images
Place your menu images (menu1.jpg to menu8.jpg) in the `menu_images/` folder.

### 3. Run Setup Script
```bash
python whatsapp_bot_setup.py
```

### 4. Check Generated Files
The script will create structured data in the `bot_data/` folder:
- `menu_items.json` - Extracted menu data
- `bot_config.json` - Botpress configuration
- `response_templates.json` - Spanish response templates
- `menu_structure.json` - Organized menu by category
- `inventory_summary.json` - Inventory data summary
- `sales_summary.json` - Sales data summary

## 📊 Data Integration

This bot integrates with your existing Prana ML project:
- **Inventory Data**: `../prana_ml/data/inv_prana_may.xls`
- **Sales Data**: `../prana_ml/data/cleaned_sales.csv`
- **Menu Images**: Your 8 menu JPGs with Spanish content

## 🎯 Features

### Core Functionality
- 📋 **Menu Display** - Show menu items with ingredients (Spanish)
- 🛒 **Order Processing** - Handle customer orders
- 📊 **Inventory Status** - Real-time stock availability
- 💰 **Pricing Information** - Current prices and promotions
- 🕒 **Business Hours** - Operating hours and location
- ❓ **Customer Support** - FAQ and contact information

### Advanced Features
- 🎯 **Personalized Recommendations** - Based on customer preferences
- 📈 **Analytics Integration** - Connect with existing Prana ML data
- 💳 **Loyalty Program** - Points and rewards system
- 📱 **Multi-language Support** - Spanish primary, English secondary

## 🛠️ Implementation

### Recommended Platform: Botpress
- **Why Botpress**: Easiest implementation, visual interface, direct WhatsApp integration
- **Cost**: $200/month (Professional Plan)
- **Setup Time**: 1-2 weeks vs 2-3 months for Rasa

### Alternative Platforms
- **Rasa**: More powerful but requires significant development
- **Landbot**: Good for simple flows but less flexible

## 📈 Expected Results

- **70% reduction** in manual order processing
- **20-30% revenue increase** through 24/7 availability
- **Improved customer satisfaction** with instant responses
- **Better inventory management** through real-time tracking

## 💰 Cost Breakdown

| Item | Cost | Frequency |
|------|------|-----------|
| Botpress Professional | $200 | Monthly |
| WhatsApp Business API | $50-100 | Monthly |
| **Total** | **$250-300** | **Monthly** |

## 📚 Documentation

- **Implementation Guide**: `docs/whatsapp_bot_implementation.md`
- **Quick Start Guide**: `docs/QUICK_START_WHATSAPP_BOT.md`
- **Setup Report**: `bot_data/setup_report.md` (generated after running setup)

## 🔧 Technical Details

### Dependencies
- **OCR Processing**: pytesseract for menu image text extraction
- **Data Processing**: pandas for inventory and sales data
- **Image Handling**: Pillow for menu image processing
- **Language Support**: Spanish (es) with OCR language pack

### Data Sources
- **Menu Images**: OCR extraction from JPG files
- **Inventory**: Excel file from Prana ML project
- **Sales**: CSV file from Prana ML project
- **Analytics**: Integration with existing ML models

## 🎯 Success Metrics

### Customer Engagement
- Response rate
- Conversation length
- Return customers

### Business Impact
- Orders through bot
- Revenue increase
- Customer satisfaction scores

### Operational Efficiency
- Reduced manual work
- Faster order processing
- Better inventory management

## 🚀 Next Steps

1. **Run the setup script** to process your data
2. **Sign up for Botpress** and create your bot
3. **Import the generated data** from `bot_data/` folder
4. **Set up WhatsApp Business API** integration
5. **Configure conversation flows** using the templates
6. **Test with your team** and launch to customers

## 📞 Support

For questions or issues:
1. Check the documentation in the `docs/` folder
2. Review the setup report in `bot_data/setup_report.md`
3. Refer to Botpress documentation: https://botpress.com/docs

---

**Ready to create your WhatsApp bot? Start with the setup script! 🚀** 