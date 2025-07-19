# 📍 GPS Location Setup Guide

## ✅ **Feature Status: WORKING**

Your WhatsApp bot now includes GPS location links! Customers can click on the links to get directions directly from WhatsApp.

## 🏪 **Current Locations (Template)**

### **Sede Principal**
- **Address**: Centro Comercial [Nombre], Av. Principal #123, Caracas
- **GPS**: https://maps.google.com/?q=10.4806,-66.9036
- **Hours**: 7:00 AM - 11:00 PM

### **Sede Miranda**
- **Address**: Centro Comercial [Nombre], Av. Miranda #456, Miranda
- **GPS**: https://maps.google.com/?q=10.4870,-66.8512
- **Hours**: 7:00 AM - 11:00 PM

### **Sede Valencia**
- **Address**: Centro Comercial [Nombre], Av. Bolívar #789, Valencia
- **GPS**: https://maps.google.com/?q=10.1579,-67.9972
- **Hours**: 7:00 AM - 11:00 PM

---

## 🔧 **How to Customize Locations**

### **Step 1: Get Real Addresses**
Replace the template addresses with your actual store locations.

### **Step 2: Get GPS Coordinates**
1. Go to [Google Maps](https://maps.google.com)
2. Search for your store address
3. Right-click on the exact location
4. Copy the coordinates (latitude, longitude)

### **Step 3: Update the Files**

#### **File 1: `bot_data/response_templates.json`**
Update the location section with real addresses:

```json
"location": [
  "📍 *NUESTRAS UBICACIONES:*",
  "",
  "🏪 *SEDE PRINCIPAL*",
  "Centro Comercial [REAL NAME]",
  "[REAL ADDRESS]",
  "📱 https://maps.google.com/?q=[LAT],[LONG]",
  "",
  "🏪 *SEDE MIRANDA*", 
  "Centro Comercial [REAL NAME]",
  "[REAL ADDRESS]",
  "📱 https://maps.google.com/?q=[LAT],[LONG]",
  "",
  "🏪 *SEDE VALENCIA*",
  "Centro Comercial [REAL NAME]", 
  "[REAL ADDRESS]",
  "📱 https://maps.google.com/?q=[LAT],[LONG]",
  "",
  "💡 *Haz clic en los enlaces para obtener direcciones GPS*",
  "¡Te esperamos en cualquiera de nuestras sedes!"
]
```

#### **File 2: `custom_whatsapp_bot.py`**
Update the `get_specific_location` method with real data:

```python
locations = {
    'principal': {
        'name': 'SEDE PRINCIPAL',
        'address': '[REAL ADDRESS]',
        'gps': 'https://maps.google.com/?q=[LAT],[LONG]',
        'hours': '7:00 AM - 11:00 PM'
    },
    'miranda': {
        'name': 'SEDE MIRANDA',
        'address': '[REAL ADDRESS]',
        'gps': 'https://maps.google.com/?q=[LAT],[LONG]',
        'hours': '7:00 AM - 11:00 PM'
    },
    'valencia': {
        'name': 'SEDE VALENCIA',
        'address': '[REAL ADDRESS]',
        'gps': 'https://maps.google.com/?q=[LAT],[LONG]',
        'hours': '7:00 AM - 11:00 PM'
    }
}
```

---

## 🧪 **Test Commands**

Try these messages on WhatsApp:

### **General Location**
- "direccion" - Shows all locations with GPS links
- "ubicacion" - Shows all locations with GPS links
- "donde estan" - Shows all locations with GPS links

### **Specific Locations**
- "sede principal" - Shows principal location only
- "sede miranda" - Shows Miranda location only
- "sede valencia" - Shows Valencia location only
- "principal" - Shows principal location only
- "miranda" - Shows Miranda location only
- "valencia" - Shows Valencia location only

---

## 📱 **How It Works**

1. **Customer asks**: "direccion"
2. **Bot responds**: All locations with clickable GPS links
3. **Customer clicks**: Any GPS link
4. **Opens**: Google Maps with directions to that location

---

## 🎯 **Benefits**

✅ **Easy navigation** - One-click directions  
✅ **Multiple locations** - Support for all your stores  
✅ **Professional** - Looks great in WhatsApp  
✅ **Convenient** - No need to copy/paste addresses  

---

**Your GPS location feature is ready to use!** 🚀 