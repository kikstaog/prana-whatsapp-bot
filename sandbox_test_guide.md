# 🧪 WhatsApp Sandbox Testing Guide

## Current Setup ✅
- **Bot URL**: `https://twenty-dancers-push.loca.lt/webhook`
- **Status**: Running and responding
- **Language**: Spanish

## 📱 How to Test
1. Open WhatsApp on your phone
2. Send the test message to your Twilio sandbox number
3. Wait for response
4. Check if response matches expected

---

## 🧪 Test Scenarios

### 1. **Greetings & Basic Interaction**
```
Test Message → Expected Response
"hola" → Welcome message + menu categories
"buenos dias" → Welcome message + menu categories  
"hello" → Welcome message + menu categories
"que tal" → Welcome message + menu categories
```

### 2. **Menu Categories**
```
"menu" → All 9 categories listed
"que tienen en el menu" → All 9 categories listed
"carta" → All 9 categories listed
"que ofrecen" → All 9 categories listed
```

### 3. **Specific Categories**
```
"jugos" → Cold pressed juices list
"shots" → Shots list (flu shot, ginger shot, etc.)
"desayunos" → Breakfast items
"almuerzos" → Lunch items
"batidos" → Smoothies/milks
"postres" → Desserts
"bake goods" → Baked items
"prana cakes" → Cake items
```

### 4. **Health & Wellness Questions**
```
"tengo gripe" → Health recommendations
"estoy enfermo" → Health recommendations
"tengo dolor de cabeza" → Health recommendations
"tengo sed" → Drink suggestions
"quiero algo refrescante" → Cold drink options
"necesito energia" → Energy drink options
"quiero detox" → Detox drink options
```

### 5. **Pricing Questions**
```
"cuanto cuesta" → Price ranges
"precios" → Price ranges
"costo" → Price ranges
"cuanto vale" → Price ranges
```

### 6. **Business Information**
```
"horarios" → Business hours
"cuales son los horarios" → Business hours
"cuando abren" → Business hours
"cuando cierran" → Business hours
"direccion" → Location info
"donde estan" → Location info
"ubicacion" → Location info
```

### 7. **Specific Items**
```
"citrus" → Citrus juice details
"flu shot" → Flu shot details
"bowl de chia" → Chia bowl details
"trufa" → Truffle details
"milky way" → Milky way details
```

### 8. **Dietary Questions**
```
"gluten" → Gluten-free information
"sin gluten" → Gluten-free information
"celiaco" → Gluten-free information
"azucar" → Sugar information
"tienen azucar" → Sugar information
```

### 9. **Volume & Size Questions**
```
"cuantos ml" → Volume information
"tamaño" → Size information
"cuanto pesa" → Weight information
```

### 10. **Recommendations**
```
"recomendacion" → Personalized recommendations
"que me recomiendas" → Personalized recommendations
"sugerencia" → Personalized recommendations
```

### 11. **Goodbye & Exit**
```
"gracias" → Goodbye message
"adios" → Goodbye message
"hasta luego" → Goodbye message
"no mas" → Goodbye message
"eso es todo" → Goodbye message
```

---

## 🔍 **Advanced Testing Scenarios**

### **Conversation Flow Test**
1. Send: "hola"
2. Send: "jugos"
3. Send: "citrus"
4. Send: "cuanto cuesta"
5. Send: "gracias"

### **Error Handling Test**
1. Send: "xyz123" (random text)
2. Send: "..." (just dots)
3. Send: "" (empty message)

### **Multi-language Test**
1. Send: "hello" (English)
2. Send: "hola" (Spanish)
3. Send: "hi" (English)

### **Complex Questions Test**
1. Send: "tengo gripe y quiero algo bueno"
2. Send: "que jugos tienen y cuanto cuestan"
3. Send: "estoy sediento y necesito energia"

---

## 📊 **Testing Checklist**

### ✅ **Core Functionality**
- [ ] Greetings work
- [ ] Menu categories display
- [ ] Specific items found
- [ ] Health recommendations work
- [ ] Business info accessible
- [ ] Goodbye messages work

### ✅ **Response Quality**
- [ ] Responses are in Spanish
- [ ] Responses are helpful
- [ ] Follow-up questions included
- [ ] No errors or crashes
- [ ] Quick response time

### ✅ **Edge Cases**
- [ ] Random text handled gracefully
- [ ] Empty messages handled
- [ ] Long messages handled
- [ ] Special characters handled

---

## 🚨 **If Something Doesn't Work**

### **Bot Not Responding**
1. Check if Flask app is running: `python app.py`
2. Check if localtunnel is running: `lt --port 5000`
3. Verify webhook URL in Twilio console
4. Check Flask logs for errors

### **Wrong Responses**
1. Check `bot_data/` files are loaded
2. Verify message patterns in code
3. Test locally with `python quick_test.py`

### **Slow Responses**
1. Check internet connection
2. Verify localtunnel status
3. Check Flask app performance

---

## 📝 **Test Results Log**

| Test | Message | Expected | Actual | Status |
|------|---------|----------|--------|--------|
| 1 | "hola" | Welcome | | |
| 2 | "menu" | Categories | | |
| 3 | "jugos" | Juice list | | |
| 4 | "tengo gripe" | Health recs | | |
| 5 | "horarios" | Hours | | |

---

**Happy Testing! 🎉** 