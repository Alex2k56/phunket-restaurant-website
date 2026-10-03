from flask import Flask, render_template, request, session, redirect, url_for, abort

app = Flask(__name__)
app.secret_key = 'phunket_secret_key_2026'

TEXTE = {
    'ro': {
        'toate': 'Toate',
        'cos': '🛒 Coșul meu',
        'de_la': 'De la',
        'adauga': 'Adaugă în coș',
        'finalizeaza': 'Finalizează Comanda',
        'total': 'Total',
        'nume': 'Nume complet',
        'telefon': 'Număr de telefon',
        'adresa': 'Adresa de livrare',
        'plata': 'Metoda de plată',
        'cash': 'Numerar la livrare (Cash)',
        'card': 'Card bancar online',
        'trimite': 'TRIMITE COMANDA'
    },
    'en': {
        'toate': 'All',
        'cos': '🛒 My Cart',
        'de_la': 'From',
        'adauga': 'Add to Cart',
        'finalizeaza': 'Checkout',
        'total': 'Total',
        'nume': 'Full Name',
        'telefon': 'Phone Number',
        'adresa': 'Delivery Address',
        'plata': 'Payment Method',
        'cash': 'Cash on Delivery',
        'card': 'Online Credit Card',
        'trimite': 'PLACE ORDER'
    },
    'th': {
        'toate': 'ทั้งหมด',
        'cos': '🛒 ตะกร้าของฉัน',
        'de_la': 'เริ่มต้น',
        'adauga': 'เพิ่มลงในตะกร้า',
        'finalizeaza': 'ชำระเงิน',
        'total': 'รวมทั้งหมด',
        'nume': 'ชื่อ-นามสกุล',
        'telefon': 'เบอร์โทรศัพท์',
        'adresa': 'ที่อยู่จัดส่ง',
        'plata': 'วิธีการชำระเงิน',
        'cash': 'ชำระเงินปลายทาง',
        'card': 'บัตรเครดิตออนไลน์',
        'trimite': 'ยืนยันการสั่งซื้อ'
    }
}

CATEGORII ={
    "alcohol_drinks": {
        "ro": "Băuturi Alcoolice",
        "en": "Alcohol Drinks",
        "th": "เครื่องดื่มแอลกอฮอล์",
        "icon": "🍸"
    },
    "breakfast": {
        "ro": "Mic Dejun",
        "en": "Breakfast",
        "th": "อาหารเช้า",
        "icon": "🍳"
    },
    "salads": {
        "ro": "Salate",
        "en": "Salads",
        "th": "สลัด",
        "icon": "🥗"
    },
    "first_course": {
        "ro": "Felul Întâi ",
        "en": "First Course",
        "th": "ซุป",
        "icon": "🥣"
    },
    "main_dishes": {
        "ro": "Mâncăruri Principale",
        "en": "Mains",
        "th": "อาหารจานหลัก",
        "icon": "🍲"
    },
    "garnituri": {
        "ro": "Garnituri",
        "en": "Sides",
        "th": "เครื่องเคียง",
        "icon": "🍟"
    },
    "vinuri": {
        "ro": "Vinuri",
        "en": "Wines",
        "th": "ไวน์",
        "icon": "🍷"
    },
    "drinks": {
        "ro": "Băuturi",
        "en": "Drinks",
        "th": "เครื่องดื่ม",
        "icon": "🥤"
    }
}

PRODUSE = {
    # --- DRINKS / BĂUTURI ---

    # HOMEMADE BEVERAGES
    "d_01": {
        "categorie": "drinks",
        "nume": {"ro": "Compot de fructe de casă", "en": "Homemade Fruit compote", "th": "น้ำผลไม้ต้มสไตล์โฮมเมด"},
        "descriere": {"ro": "Compot răcoritor preparat din fructe de casă.", "en": "Refreshing homemade fruit compote.",
                      "th": "น้ำผลไม้ต้มทำเองรสกลมกล่อม"},
        "imagine": "/static/img/fruit_compote.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 80}]
    },
    "d_02": {
        "categorie": "drinks",
        "nume": {"ro": "Cvas", "en": "Kvass", "th": "ควัส"},
        "descriere": {"ro": "Băutură tradițională fermentată din pâine.", "en": "Traditional fermented bread drink.",
                      "th": "เครื่องดื่มหมักสไตล์ยุโรปตะวันออก"},
        "imagine": "/static/img/kvass.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 100}]
    },

    # SOFT BEVERAGES
    "d_03": {
        "categorie": "drinks",
        "nume": {"ro": "Lipton Ice Tea", "en": "Lipton ice tea", "th": "ชาดำเย็น ลิปตัน"},
        "descriere": {"ro": "Ceai rece Lipton răcoritor.", "en": "Refreshing Lipton ice tea.", "th": "ชาดำเย็นลิปตัน"},
        "imagine": "/static/img/lipton.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 50}]
    },
    "d_04": {
        "categorie": "drinks",
        "nume": {"ro": "Coca-Cola", "en": "Coca cola", "th": "โคคา-โคล่า"},
        "descriere": {"ro": "Băutură carbogazoasă Coca-Cola.", "en": "Classic Coca-Cola.", "th": "โคคา-โคล่า"},
        "imagine": "/static/img/coca_cola.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 50}]
    },
    "d_05": {
        "categorie": "drinks",
        "nume": {"ro": "Sprite", "en": "Sprite", "th": "สไปรท์"},
        "descriere": {"ro": "Băutură carbogazoasă cu gust de lămâie și lime.", "en": "Refreshing lemon-lime soda.",
                      "th": "สไปรท์"},
        "imagine": "/static/img/sprite.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 50}]
    },
    "d_06": {
        "categorie": "drinks",
        "nume": {"ro": "Schweppes (original, lămâie)", "en": "Schweppes (original, lemon)",
                 "th": "ชเวปส์ (ออริจินัล, เลมอน)"},
        "descriere": {"ro": "Băutură tonică Schweppes (original sau lămâie).",
                      "en": "Schweppes tonic drink (original or lemon).", "th": "ชเวปส์ (รสออริจินัล หรือ เลมอน)"},
        "imagine": "/static/img/schweppes.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 50}]
    },
    "d_07": {
        "categorie": "drinks",
        "nume": {"ro": "Apă", "en": "Water", "th": "น้ำดื่ม"},
        "descriere": {"ro": "Apă minerală plată sau carbogazoasă.", "en": "Still or sparkling water.", "th": "น้ำดื่ม"},
        "imagine": "/static/img/water.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 30}]
    },

    # SMOOTHIES
    "d_08": {
        "categorie": "drinks",
        "nume": {"ro": "Smoothie de mango", "en": "Mango smoothie", "th": "มะม่วงปั่น"},
        "descriere": {"ro": "Smoothie cremos din mango proaspăt.", "en": "Creamy fresh mango smoothie.",
                      "th": "มะม่วงปั่นเนื้อเนียน"},
        "imagine": "/static/img/smoothie_mango.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 120}]
    },
    "d_09": {
        "categorie": "drinks",
        "nume": {"ro": "Smoothie de banane", "en": "Banana smoothie", "th": "กล้วยปั่น"},
        "descriere": {"ro": "Smoothie delicios de banane.", "en": "Delicious banana smoothie.", "th": "กล้วยหอมปั่น"},
        "imagine": "/static/img/smoothie_banana.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 120}]
    },
    "d_10": {
        "categorie": "drinks",
        "nume": {"ro": "Smoothie de căpșuni", "en": "Strawberry smoothie", "th": "สตรอว์เบอร์รี่ปั่น"},
        "descriere": {"ro": "Smoothie din căpșuni dulci și zemoase.", "en": "Sweet strawberry smoothie.",
                      "th": "สตรอว์เบอร์รี่ปั่น"},
        "imagine": "/static/img/smoothie_strawberry.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 120}]
    },
    "d_11": {
        "categorie": "drinks",
        "nume": {"ro": "Smoothie de fructe de pădure", "en": "Mixed berry smoothie", "th": "มิกซ์เบอร์รี่ปั่น"},
        "descriere": {"ro": "Smoothie din amestec de fructe de pădure.", "en": "Mixed berry smoothie.",
                      "th": "มิกซ์เบอร์รี่ปั่นรสเปรี้ยวหวาน"},
        "imagine": "/static/img/smoothie_berry.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 120}]
    },
    "d_12": {
        "categorie": "drinks",
        "nume": {"ro": "Smoothie de ananas", "en": "Pineapple smoothie", "th": "สับปะรดปั่น"},
        "descriere": {"ro": "Smoothie răcoritor de ananas.", "en": "Refreshing pineapple smoothie.",
                      "th": "สับปะรดปั่น"},
        "imagine": "/static/img/smoothie_pineapple.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 120}]
    },
    "d_13": {
        "categorie": "drinks",
        "nume": {"ro": "Smoothie de pepene roșu", "en": "Watermelon smoothie", "th": "แตงโมปั่น"},
        "descriere": {"ro": "Smoothie hidratant din pepene roșu.", "en": "Hydrating watermelon smoothie.",
                      "th": "แตงโมปั่นสดชื่น"},
        "imagine": "/static/img/smoothie_watermelon.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 120}]
    },
    "d_14": {
        "categorie": "drinks",
        "nume": {"ro": "Smoothie din mix de fructe", "en": "Mixed fruits smoothie", "th": "ผลไม้รวมปั่น"},
        "descriere": {"ro": "Smoothie din amestec de fructe exotice.", "en": "Mixed tropical fruit smoothie.",
                      "th": "ผลไม้รวมปั่น"},
        "imagine": "/static/img/smoothie_mixed.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 120}]
    },

    # JUICES
    "d_15": {
        "categorie": "drinks",
        "nume": {"ro": "Suc de roșii", "en": "Tomato juice", "th": "น้ำมะเขือเทศ"},
        "descriere": {"ro": "Suc proaspăt de roșii.", "en": "Fresh tomato juice.", "th": "น้ำมะเขือเทศ"},
        "imagine": "/static/img/juice_tomato.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 70}]
    },
    "d_16": {
        "categorie": "drinks",
        "nume": {"ro": "Suc de ananas", "en": "Pineapple juice", "th": "น้ำสับปะรด"},
        "descriere": {"ro": "Suc natural de ananas.", "en": "Natural pineapple juice.", "th": "น้ำสับปะรด"},
        "imagine": "/static/img/juice_pineapple.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 70}]
    },
    "d_17": {
        "categorie": "drinks",
        "nume": {"ro": "Suc de măr", "en": "Apple juice", "th": "น้ำแอปเปิ้ล"},
        "descriere": {"ro": "Suc natural de măr.", "en": "Natural apple juice.", "th": "น้ำแอปเปิ้ล"},
        "imagine": "/static/img/juice_apple.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 70}]
    },
    "d_18": {
        "categorie": "drinks",
        "nume": {"ro": "Suc de portocale", "en": "Orange juice", "th": "น้ำส้ม"},
        "descriere": {"ro": "Suc natural de portocale.", "en": "Natural orange juice.", "th": "น้ำส้ม"},
        "imagine": "/static/img/juice_orange.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 70}]
    },
    "d_19": {
        "categorie": "drinks",
        "nume": {"ro": "Nucă de cocos", "en": "Coconut water", "th": "น้ำมะพร้าว"},
        "descriere": {"ro": "Apă proaspătă de nucă de cocos.", "en": "Fresh coconut water.", "th": "น้ำมะพร้าวสด"},
        "imagine": "/static/img/coconut.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 100}]
    },

    # HOT DRINKS
    "d_20": {
        "categorie": "drinks",
        "nume": {"ro": "Americano", "en": "Americano", "th": "อเมริกาโน่"},
        "descriere": {"ro": "Cafea espresso diluată cu apă caldă.", "en": "Classic Americano coffee.",
                      "th": "กาแฟอเมริกาโน่"},
        "imagine": "/static/img/americano.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 80}]
    },
    "d_21": {
        "categorie": "drinks",
        "nume": {"ro": "Caffe Latte", "en": "Latte", "th": "ลาเต้"},
        "descriere": {"ro": "Espresso cu lapte cald și spumă fină.", "en": "Espresso with steamed milk and light foam.",
                      "th": "กาแฟลาเต้"},
        "imagine": "/static/img/latte.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 100}]
    },
    "d_22": {
        "categorie": "drinks",
        "nume": {"ro": "Latte Macchiato", "en": "Latte macchiato", "th": "ลาเต้แมคเคียโต้"},
        "descriere": {"ro": "Lapte spumat pătat cu un shot de espresso.",
                      "en": "Foamed milk marked with a shot of espresso.", "th": "ลาเต้แมคเคียโต้"},
        "imagine": "/static/img/latte_macchiato.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 100}]
    },
    "d_23": {
        "categorie": "drinks",
        "nume": {"ro": "Espresso", "en": "Espresso", "th": "เอสเพรสโซ่"},
        "descriere": {"ro": "Cafea espresso concentrată și aromată.", "en": "Rich and bold espresso shot.",
                      "th": "กาแฟเอสเพรสโซ่"},
        "imagine": "/static/img/espresso.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 80}]
    },
    "d_24": {
        "categorie": "drinks",
        "nume": {"ro": "Cappuccino", "en": "Cappuccino", "th": "คาปูชิโน่"},
        "descriere": {"ro": "Espresso cu lapte și spumă bogată de lapte.",
                      "en": "Espresso with equal parts steamed milk and foam.", "th": "กาแฟคาปูชิโน่"},
        "imagine": "/static/img/cappuccino.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 80}]
    },
    "d_25": {
        "categorie": "drinks",
        "nume": {"ro": "Ceai (verde, negru)", "en": "Tea (green, black)", "th": "ชา (ชาเขียว, ชาดำ)"},
        "descriere": {"ro": "Ceai cald (verde sau negru).", "en": "Hot tea (green or black).",
                      "th": "ชาร้อน (ชาเขียว หรือ ชาดำ)"},
        "imagine": "/static/img/tea_gb.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 60}]
    },
    "d_26": {
        "categorie": "drinks",
        "nume": {"ro": "Ceai (Earl Grey, iasomie)", "en": "Tea (Earl Grey, jasmine)", "th": "ชา (เอิร์ลเกรย์, มะลิ)"},
        "descriere": {"ro": "Ceai aromat (Earl Grey sau iasomie).", "en": "Aromatic tea (Earl Grey or jasmine).",
                      "th": "ชาหอม (เอิร์ลเกรย์ หรือ มะลิ)"},
        "imagine": "/static/img/tea_ej.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 60}]
    },
    "d_27": {
        "categorie": "drinks",
        "nume": {"ro": "Ceainic cu ceai din plante", "en": "Herbal teapot", "th": "ชาสมุนไพร (กา)"},
        "descriere": {"ro": "Ceainic cald cu infuzie din plante naturale.",
                      "en": "Teapot filled with natural herbal infusion.", "th": "ชาสมุนไพรร้อนแบบกา"},
        "imagine": "/static/img/herbal_teapot.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 200}]
    },
    # --- BREAKFAST ---
    "brk_01": {
        "categorie": "breakfast",
        "nume": {"ro": "Papanași cu somon sărat", "en": "Papanași with salted salmon", "th": "ปาปานาชีใส่แซลมอนหมักเกลือ"},
        "descriere": {"ro": "Papanași de casă serviți cu somon sărat.", "en": "Homemade papanași served with salted salmon.", "th": "ปาปานาชีทำเองเสิร์ฟพร้อมแซลมอนหมักเกลือ"},
        "imagine": "/static/img/papanasi_salmon.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 320}]
    },
    "brk_02": {
        "categorie": "breakfast",
        "nume": {"ro": "Papanași dulci", "en": "Sweet papanași", "th": "ปาปานาชีหวาน"},
        "descriere": {"ro": "Papanași tradiționali dulci serviți cu smântână și gem.", "en": "Traditional sweet papanași with sour cream and jam.", "th": "ปาปานาชีหวานสไตล์ดั้งเดิมเสิร์ฟพร้อมครีมและแยม"},
        "imagine": "/static/img/papanasi_sweet.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 270}]
    },
    "brk_03": {
        "categorie": "breakfast",
        "nume": {"ro": "Clătite cu brânză de vaci și stafide", "en": "Pancakes with cottage cheese and raisins", "th": "แพนเค้กไส้คอทเทจชีสและลูกเกด"},
        "descriere": {"ro": "Clătite fine umplute cu brânză dulce de vaci și stafide.", "en": "Fine pancakes stuffed with sweet cottage cheese and raisins.", "th": "แพนเค้กนุ่มๆ ไส้คอทเทจชีสหวานและลูกเกด"},
        "imagine": "/static/img/pancakes_cheese_raisins.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 270}]
    },
    "brk_04": {
        "categorie": "breakfast",
        "nume": {"ro": "Clătite cu ficat de pui", "en": "Pancakes with chicken liver", "th": "แพนเค้กไส้ตับไก่"},
        "descriere": {"ro": "Clătite calde umplute cu ficat de pui fraged.", "en": "Warm pancakes stuffed with tender chicken liver.", "th": "แพนเค้กร้อนๆ ไส้ตับไก่นุ่ม"},
        "imagine": "/static/img/pancakes_liver.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 250}]
    },
    "brk_05": {
        "categorie": "breakfast",
        "nume": {"ro": "Clătite cu pui", "en": "Pancakes with chicken", "th": "แพนเค้กไส้ไก่"},
        "descriere": {"ro": "Clătite umplute cu carne de pui suculentă.", "en": "Pancakes stuffed with juicy chicken meat.", "th": "แพนเค้กไส้เนื้อไก่ฉ่ำๆ"},
        "imagine": "/static/img/pancakes_chicken.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 250}]
    },
    "brk_06": {
        "categorie": "breakfast",
        "nume": {"ro": "Clătite cu somon", "en": "Pancakes with salmon", "th": "แพนเค้กไส้แซลมอน"},
        "descriere": {"ro": "Clătite umplute cu bucăți de somon delicioase.", "en": "Pancakes filled with delicious salmon pieces.", "th": "แพนเค้กไส้แซลมอนอร่อย"},
        "imagine": "/static/img/pancakes_salmon.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 300}]
    },
    "brk_07": {
        "categorie": "breakfast",
        "nume": {"ro": "Clătite Moldova", "en": "Moldova pancakes", "th": "แพนเค้กมอลโดวา"},
        "descriere": {"ro": "Clătite tradiționale specifice casei.", "en": "Traditional house special pancakes.", "th": "แพนเค้กสูตรพิเศษสไตล์มอลโดวา"},
        "imagine": "/static/img/pancakes_moldova.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 200}]
    },
    "brk_08": {
        "categorie": "breakfast",
        "nume": {"ro": "Omletă cu șuncă și brânză feta", "en": "Omelette with ham & feta cheese", "th": "ไข่เจียวแฮมและเฟต้าชีส"},
        "descriere": {"ro": "Omletă puffy cu șuncă și brânză feta.", "en": "Fluffy omelette with ham and feta cheese.", "th": "ไข่เจียวนุ่มฟูใส่แฮมและเฟต้าชีส"},
        "imagine": "/static/img/omelette_ham.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 270}]
    },
    "brk_09": {
        "categorie": "breakfast",
        "nume": {"ro": "Omletă cu legume", "en": "Omelette with vegetables", "th": "ไข่เจียวใส่ผัก"},
        "descriere": {"ro": "Omletă proaspătă cu legume de sezon.", "en": "Fresh omelette cooked with seasonal vegetables.", "th": "ไข่เจียวสดใส่ผักตามฤดูกาล"},
        "imagine": "/static/img/omelette_veg.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 220}]
    },
    "brk_10": {
        "categorie": "breakfast",
        "nume": {"ro": "Mămăligă cu ciuperci și ou ochi", "en": "Polenta with mushrooms & poached egg", "th": "โพลเอนต้ากับเห็ดและไข่ดาวน้ำ"},
        "descriere": {"ro": "Mămăligă caldă servită cu ciuperci sotate și ou ochi.", "en": "Warm polenta served with sautéed mushrooms and poached egg.", "th": "โพลเอนต้าร้อนๆ เสิร์ฟพร้อมเห็ดผัดและไข่ดาวน้ำ"},
        "imagine": "/static/img/polenta_egg.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 300}]
    },
    "brk_11": {
        "categorie": "breakfast",
        "nume": {"ro": "Ouă prăjite cu bacon și roșii", "en": "Fried eggs with bacon & tomatoes", "th": "ไข่ดาวเสิร์ฟพร้อมเบคอนและมะเขือเทศ"},
        "descriere": {"ro": "Ouă prăjite crocante alături de bacon și roșii proaspete.", "en": "Fried eggs with crispy bacon and fresh tomatoes.", "th": "ไข่ดาวเสิร์ฟพร้อมเบคอนกรอบและมะเขือเทศสด"},
        "imagine": "/static/img/fried_eggs_bacon.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 200}]
    },
    # --- SALADS ---
    "sal_01": {
        "categorie": "salads",
        "nume": {"ro": "Vegetable salad", "en": "Vegetable salad", "th": "สลัดผักสด"},
        "descriere": {"ro": "Salată proaspătă din legume de sezon.", "en": "Fresh seasonal vegetable salad.",
                      "th": "สลัดผักสดตามฤดูกาล"},
        "imagine": "/static/img/veg_salad.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 150}]
    },
    "sal_02": {
        "categorie": "salads",
        "nume": {"ro": "Greek salad", "en": "Greek salad", "th": "สลัดกรีก"},
        "descriere": {"ro": "Legume proaspete, măsline și brânză feta.",
                      "en": "Fresh vegetables, olives and feta cheese.", "th": "สลัดกรีกใส่มะกอกและเฟต้าชีส"},
        "imagine": "/static/img/greek_salad.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 280}]
    },
    "sal_03": {
        "categorie": "salads",
        "nume": {"ro": "Sauerkraut salad", "en": "Sauerkraut salad", "th": "สลัดกะหล่ำปลีดอง"},
        "descriere": {"ro": "Varză murată tradițională cu ulei.", "en": "Traditional sauerkraut salad with oil.",
                      "th": "สลัดกะหล่ำปลีดองสไตล์ดั้งเดิม"},
        "imagine": "/static/img/sauerkraut.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 120}]
    },
    "sal_04": {
        "categorie": "salads",
        "nume": {"ro": "Eggplant caviar", "en": "Eggplant caviar", "th": "คาร์เวียร์มะเขือยาว"},
        "descriere": {"ro": "Salată de vinete coapte tocate fin.", "en": "Finely chopped roasted eggplant salad.",
                      "th": "สลัดมะเขือยาวเผาบดละเอียด"},
        "imagine": "/static/img/eggplant_caviar.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 250}]
    },
    "sal_05": {
        "categorie": "salads",
        "nume": {"ro": "Tea leaf salad", "en": "Tea leaf salad", "th": "สลัดใบชา"},
        "descriere": {"ro": "Salată specială cu frunze de ceai.", "en": "Special tea leaf salad.",
                      "th": "สลัดสูตรพิเศษผสมใบชา"},
        "imagine": "/static/img/tea_leaf_salad.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 150}]
    },
    "sal_06": {
        "categorie": "salads",
        "nume": {"ro": "Olivier salad", "en": "Olivier salad", "th": "สลัดโอลิเวียร์"},
        "descriere": {"ro": "Salată tradițională cu legume fierte și maioneză.",
                      "en": "Traditional boiled vegetable salad with mayo.",
                      "th": "สลัดรัสเซียดั้งเดิมใส่มันฝรั่งและมายองเนส"},
        "imagine": "/static/img/olivier.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 250}]
    },
    "sal_07": {
        "categorie": "salads",
        "nume": {"ro": "Dressed mackerel", "en": "Dressed mackerel", "th": "สลัดปลาแมคเคอเรลทรงเครื่อง"},
        "descriere": {"ro": "Macrou stratificat cu legume fierte și maioneză.",
                      "en": "Layered mackerel with boiled vegetables and mayo.",
                      "th": "สลัดปลาแมคเคอเรลชั้นๆ ใส่มายองเนส"},
        "imagine": "/static/img/dressed_mackerel.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 300}]
    },
    "sal_08": {
        "categorie": "salads",
        "nume": {"ro": "Beetroot salad", "en": "Beetroot salad", "th": "สลัดบีทรูท"},
        "descriere": {"ro": "Sfeclă roșie cu maioneză.", "en": "Beetroot salad with mayonnaise.",
                      "th": "สลัดบีทรูทผสมมายองเนส"},
        "imagine": "/static/img/beetroot_salad.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 150}]
    },
        "sal_09": {
        "categorie": "salads",
        "nume": {"ro": "Salată cu carne de vită", "en": "Beef salad", "th": "สลัดเนื้อวัว"},
        "descriere": {"ro": "Mix de salată, roșii cherry, felii de cartofi, castraveți, dovlecei, ulei de trufe, semințe de dovleac și porumb.", "en": "Salad mix, cherry tomatoes, potato wedges, cucumber, zucchini, truffle oil, pumpkin seeds, corn.", "th": "สลัดมิกซ์ เนื้อวัว มะเขือเทศเชอร์รี่ และซอสทรัฟเฟิล"},
        "imagine": "/static/img/porumbs.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 650}]
    },
    "sal_10": {
        "categorie": "salads",
        "nume": {"ro": "Salată Yuzu cu pui", "en": "Yuzu chicken salad", "th": "สลัดไก่ซอสยูสุ"},
        "descriere": {"ro": "Pulpă de pui, mix de salată, castraveți, avocado, ridichi, roșii cherry, edamame, sos Yuzu și arahide.", "en": "Chicken thigh, salad mix, cucumber, avocado, radish, cherry tomatoes, edamame, Yuzu sauce, peanuts.", "th": "สลัดสะโพกไก่ พร้อมอะโวคาโดและซอสยูสุ"},
        "imagine": "/static/img/castravetes.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 570}]
    },
    "sal_11": {
        "categorie": "salads",
        "nume": {"ro": "Salată Mango cu creveți", "en": "Mango & shrimp salad", "th": "สลัดมะม่วงและกุ้ง"},
        "descriere": {"ro": "Creveți, edamame, mix de salată, mango, avocado, castraveți, paie de cartofi, sosuri Mango și Ponzu.", "en": "Shrimp, edamame, salad mix, mango, avocado, cucumber, potato straw, Mango and Ponzu sauces.", "th": "สลัดกุ้งเสิร์ฟพร้อมมะม่วง อะโวคาโด และซอสพอนสึ"},
        "imagine": "/static/img/mangos.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 750}]
    },
    "sal_12": {
        "categorie": "salads",
        "nume": {"ro": "Salată Bowl cu somon", "en": "Salmon bowl salad", "th": "สลัดโบวล์แซลมอน"},
        "descriere": {"ro": "Somon afumat la rece, orez, legume crocante, ou poșat, alge chuka și dressing de susan.", "en": "Cold-smoked salmon, rice, crispy vegetables, poached egg, chuka seaweed and sesame dressing.", "th": "สลัดโบวล์แซลมอนรมควัน ไข่ดาวน้ำ และสาหร่ายวากาเมะ"},
        "imagine": "/static/img/ricesalmon.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 680}]
    },
    "sal_13": {
        "categorie": "salads",
        "nume": {"ro": "Salată Bowl cu hrișcă", "en": "Buckwheat bowl salad", "th": "สลัดโบวล์บัควีท"},
        "descriere": {"ro": "Hrișcă aromată cu ciuperci cremoase, legume proaspete, ou poșat și sos dulce de mango.", "en": "Aromatic buckwheat with creamy mushrooms, fresh vegetables, poached egg and sweet mango sauce.", "th": "สลัดโบวล์บัควีทเสิร์ฟพร้อมเห็ดผัดครีม และไข่ดาวน้ำ"},
        "imagine": "/static/img/poachedeggs.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 575}]
    },
    "sal_14": {
        "categorie": "salads",
        "nume": {"ro": "Salată Bowl Teriyaki cu pui", "en": "Teriyaki chicken bowl salad", "th": "สลัดโบวล์ไก่เทอริยากิ"},
        "descriere": {"ro": "Pui fraged în sos teriyaki, quinoa, legume proaspete, ridichi crocante și ou poșat.", "en": "Tender chicken in teriyaki sauce, quinoa, fresh vegetables, crispy radish and poached egg.", "th": "สลัดโบวล์ไก่เทอริยากิเสิร์ฟพร้อมคีนัวและไข่ดาวน้ำ"},
        "imagine": "/static/img/chickent.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 680}]
    },
    "sal_15": {
        "categorie": "salads",
        "nume": {"ro": "Tataki de ton", "en": "Tuna tataki", "th": "ทูน่าทาทากิ"},
        "descriere": {
            "ro": "Broccoli, mix de salată, castraveți, ridichi, sos Yuzu și petale de arahide.",
            "en": "Broccoli, salad mix, cucumber, radish, Yuzu sauce, peanut flakes.",
            "th": "บรอกโคลี สลัดมิกซ์ แตงกวา หัวไชเท้า ซอสยูสุ และถั่วลิสง"
        },
        "imagine": "/static/img/tons.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 555}]
    },
    "sal_16": {
        "categorie": "salads",
        "nume": {"ro": "Salată cu carne de vită prăjită", "en": "Fried beef salad", "th": "สลัดเนื้อวัวทอด"},
        "descriere": {
            "ro": "Ciuperci champignon, felii de cartofi, ceapă verde, ardei gras, salată iceberg, sos Poke, sos condimentat, coriandru și susan.",
            "en": "Champignons, potato wedges, green onion, bell pepper, iceberg lettuce, Poke sauce, spiced sauce, cilantro, sesame.",
            "th": "เห็ดแชมปินญอง มันฝรั่ง หอมใหญ่ พริกหยวก ผักกาดแก้ว ซอสโพเก้ และผักชี"
        },
        "imagine": "/static/img/champs.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 495}]
    },
    "sal_17": {
        "categorie": "salads",
        "nume": {"ro": "Salată Yasai cu calmar și sos Yuzu", "en": "Yasai salad with squid and Yuzu sauce", "th": "สลัดยาไซปลาหมึกซอสยูสุ"},
        "descriere": {
            "ro": "Mix de salată, avocado, castraveți, roșii cherry, ridichi, boabe edamame și sos Yuzu.",
            "en": "Salad mix, avocado, cucumber, cherry tomatoes, radish, edamame beans, Yuzu sauce.",
            "th": "สลัดมิกซ์ อะโวคาโด แตงกวา มะเขือเทศเชอร์รี่ ถั่วแระญี่ปุ่น และซอสยูสุ"
        },
        "imagine": "/static/img/cals.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 579}]
    },
    "sal_18": {
        "categorie": "salads",
        "nume": {"ro": "Salată Caesar", "en": "Caesar salad", "th": "ซีซาร์สลัด"},
        "descriere": {
            "ro": "Salată iceberg, roșii cherry, ouă de prepeliță, sos Caesar, crutoane și parmezan.",
            "en": "Iceberg lettuce, cherry tomatoes, quail egg, Caesar sauce, croutons, parmesan cheese.",
            "th": "ผักกาดแก้ว มะเขือเทศเชอร์รี่ ไข่นกกระทา ซอสซีซาร์ ขนมปังกรอบ และพาร์เมซานชีส"
        },
        "imagine": "/static/img/caesar_salad.jpg",
        "optiuni": [
            {"id_opt": "Cu pui", "pret": 425},
            {"id_opt": "Cu creveți", "pret": 525}
        ]
    },
    "sal_19": {
        "categorie": "salads",
        "nume": {"ro": "Vinete crocante cu coriandru și chilli dulce", "en": "Crispy eggplant with cilantro & sweet chili", "th": "มะเขือยาวกรอบผัดผักชีและซอสพริกหวาน"},
        "descriere": {
            "ro": "Vinete crocante, roșii cherry, coriandru proaspăt și sos chilli dulce.",
            "en": "Crispy eggplants, cherry tomatoes, fresh cilantro, sweet chili sauce.",
            "th": "มะเขือยาวทอดกรอบ มะเขือเทศเชอร์รี่ ผักชีสด และซอสพริกหวาน"
        },
        "imagine": "/static/img/crispy_eggplants.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 435}]
    },
    "sal_20": {
        "categorie": "salads",
        "nume": {"ro": "Salată asiatică cu carne de porc", "en": "Asian pork salad", "th": "สลัดหมูสไตล์เอเชีย"},
        "descriere": {
            "ro": "Mușchiuleț de porc, mix de salată, morcov, castraveți, roșii cherry, sos Yakiniku și susan.",
            "en": "Pork tenderloin, salad mix, carrot, cucumber, cherry tomatoes, Yakiniku sauce, sesame.",
            "th": "สันในหมู สลัดมิกซ์ แครอท แตงกวา มะเขือเทศเชอร์รี่ ซอสยากินิกุ และงา"
        },
        "imagine": "/static/img/asian_pork_salad.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 579}]
    },

    # --- FIRST COURSE ---
    "fc_01": {
        "categorie": "first_course",
        "nume": {"ro": "Borsch", "en": "Borsch", "th": "ซุปบอร์ช"},
        "descriere": {"ro": "Supă tradițională de sfeclă roșie și legume.",
                      "en": "Traditional beetroot and vegetable soup.", "th": "ซุปบีทรูทสไตล์ดั้งเดิม"},
        "imagine": "/static/img/borsch.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 220}]
    },
    "fc_02": {
        "categorie": "first_course",
        "nume": {"ro": "Zeama", "en": "Zeama", "th": "ซุปไก่ใส่นู้ดเดิ้ล"},
        "descriere": {"ro": "Supă tradițională de pui de casă cu tăiței de casă.",
                      "en": "Free range chicken soup with homemade noodles.", "th": "ซุปไก่บ้านเสิร์ฟพร้อมบะหมี่ทำเอง"},
        "imagine": "/static/img/zeama.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 220}]
    },
    "fc_03": {
        "categorie": "first_course",
        "nume": {"ro": "Pumpkin cream soup", "en": "Pumpkin cream soup", "th": "ซุปครีมฟักทอง"},
        "descriere": {"ro": "Supă fină și cremoasă de dovleac.", "en": "Smooth and creamy pumpkin soup.",
                      "th": "ซุปครีมฟักทองเนื้อเนียน"},
        "imagine": "/static/img/supa.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 200}]
    },
    "fc_04": {
        "categorie": "first_course",
        "nume": {"ro": "Spinach soup", "en": "Spinach soup", "th": "ซุปครีมผักโขม"},
        "descriere": {"ro": "Supă cremă de spanac proaspăt.", "en": "Fresh spinach cream soup.",
                      "th": "ซุปครีมผักโขมสด"},
        "imagine": "/static/img/spinach_soup.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 200}]
    },
    "fc_05": {
        "categorie": "first_course",
        "nume": {"ro": "Borsch - small portion", "en": "Borsch - small portion", "th": "ซุปบอร์ช (จานเล็ก)"},
        "descriere": {"ro": "Borș porție pentru copii.", "en": "Kid-sized portion of borsch.",
                      "th": "ซุปบอร์ชขนาดเล็กสำหรับเด็ก"},
        "imagine": "/static/img/borsch_small.jpg",
        "optiuni": [{"id_opt": "Porție mică", "pret": 120}]
    },
    "fc_06": {
        "categorie": "first_course",
        "nume": {"ro": "Zeama - small portion", "en": "Zeama - small portion", "th": "ซุปไก่ Zeama (จานเล็ก)"},
        "descriere": {"ro": "Zeamă porție pentru copii.", "en": "Kid-sized portion of zeama soup.",
                      "th": "ซุปไก่ Zeama ขนาดเล็กสำหรับเด็ก"},
        "imagine": "/static/img/supa2.jpg",
        "optiuni": [{"id_opt": "Porție mică", "pret": 120}]
    },

    # --- MAIN DISHES ---
    # --- MAIN DISHES (20 PREPARATE CU CHEI UNICE) ---
    "m_01": {
        "categorie": "main_dishes",
        "nume": {"ro": "Pelmeni cu carne", "en": "Dumplings with meat", "th": "เกี๊ยวไส้เนื้อ (Pelmeni)"},
        "descriere": {"ro": "Colțunași tradiționali umpluți cu carne suculentă de porc și vită.", "en": "Traditional dumplings filled with juicy minced meat.", "th": "เกี๊ยวสไตล์มอลโดวายัดไส้เนื้อบดละเอียด"},
        "imagine": "/static/img/dumplings_meat.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 250}]
    },
    "m_02": {
        "categorie": "main_dishes",
        "nume": {"ro": "Vareniki cu brânză de vaci", "en": "Dumplings with cottage cheese", "th": "เกี๊ยวไส้คอทเทจชีส (Vareniki)"},
        "descriere": {"ro": "Colțunași moi umpluți cu brânză proaspătă de vaci.", "en": "Soft dumplings stuffed with fresh cottage cheese.", "th": "เกี๊ยวนุ่มๆ ไส้คอทเทจชีสสด"},
        "imagine": "/static/img/dumplings_cheese.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 250}]
    },
    "m_03": {
        "categorie": "main_dishes",
        "nume": {"ro": "Vareniki cu cartofi și ciuperci", "en": "Dumplings with potatoes & mushroom", "th": "เกี๊ยวไส้มันฝรั่งและเห็ด"},
        "descriere": {"ro": "Colțunași umpluți cu cartofi și ciuperci, serviți cu ceapă prăjită deasupra.", "en": "Dumplings filled with potatoes and mushrooms, topped with fried onion.", "th": "เกี๊ยวไส้มันฝรั่งและเห็ด โรยหน้าด้วยหอมเจียว"},
        "imagine": "/static/img/dumplings_potato.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 220}]
    },
    "m_04": {
        "categorie": "main_dishes",
        "nume": {"ro": "Mămăligă cu pește prăjit și mujdei", "en": "Polenta with fried fish and garlic sauce", "th": "โพลเอนต้ากับปลาทอดและซอสกระเทียม"},
        "descriere": {"ro": "Mămăligă tradițională servită cu pește prăjit și sos mujdei picant.", "en": "Traditional polenta served with crispy fried fish and garlic sauce.", "th": "โพลเอนต้าเสิร์ฟพร้อมปลาทอดกรอบและซอสกระเทียม"},
        "imagine": "/static/img/polenta_fish.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 500}]
    },
    "m_05": {
        "categorie": "main_dishes",
        "nume": {"ro": "Mămăligă cu brânză și smântână", "en": "Polenta with feta cheese & sour cream", "th": "โพลเอนต้ากับชีสและครีมสด"},
        "descriere": {"ro": "Mămăligă caldă cu brânză rasă și smântână proaspătă.", "en": "Warm polenta with grated feta cheese and sour cream.", "th": "โพลเอนต้าร้อนๆ เสิร์ฟพร้อมชีสและครีมสด"},
        "imagine": "/static/img/polenta_cheese.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 200}]
    },
    "m_06": {
        "categorie": "main_dishes",
        "nume": {"ro": "Mămăligă cu pui", "en": "Polenta with chicken", "th": "โพลเอนต้ากับไก่"},
        "descriere": {"ro": "Mămăligă aurie alături de bucăți suculente de pui.", "en": "Golden polenta served with tender juicy chicken.", "th": "โพลเอนต้าทองคำเสิร์ฟพร้อมไก่เนื้อนุ่ม"},
        "imagine": "/static/img/polenta_chicken.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 350}]
    },
    "m_07": {
        "categorie": "main_dishes",
        "nume": {"ro": "Ardei umplut", "en": "Stuffed bell pepper", "th": "พริกหยวกยัดไส้"},
        "descriere": {"ro": "Ardei dulce umplut cu carne tocată și orez, gătit în sos de roșii.", "en": "Sweet bell pepper stuffed with minced meat and rice in tomato sauce.", "th": "พริกหยวกยัดไส้เนื้อบดและข้าวต้มในซอสมะเขือเทศ"},
        "imagine": "/static/img/stuffed_pepper.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 250}]
    },
    "m_08": {
        "categorie": "main_dishes",
        "nume": {"ro": "Ciulama de vită cu piure", "en": "Beef ciulama with mashed potato", "th": "สตูว์เนื้อกับมันบด"},
        "descriere": {"ro": "Bucăți fragede de vită în sos alb cremos, servite cu piure de cartofi.", "en": "Tender beef pieces in creamy white sauce served with mashed potatoes.", "th": "สตูว์เนื้อนุ่มในซอสต้มครีมขาวเสิร์ฟพร้อมมันบด"},
        "imagine": "/static/img/beef_ciulama.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 400}]
    },
    "m_09": {
        "categorie": "main_dishes",
        "nume": {"ro": "Ciuperci magice cu piure de conopidă", "en": "Magic mushrooms with cauliflower puree", "th": "เห็ดผัดพร้อมมันบดดอกกะหล่ำ"},
        "descriere": {"ro": "Ciuperci delicioase sotate, servite pe un pat fin de piure de conopidă.", "en": "Sautéed mushrooms served over fine cauliflower puree.", "th": "เห็ดผัดรสเด็ดเสิร์ฟบนมันบดดอกกะหล่ำเนื้อเนียน"},
        "imagine": "/static/img/magic_mushrooms.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 270}]
    },
    "m_10": {
        "categorie": "main_dishes",
        "nume": {"ro": "Mititei cu cartofi copți și salată", "en": "Mititei with roasted potatoes & salad", "th": "มิติเตยเสิร์ฟพร้อมมันฝรั่งอบและสลัด"},
        "descriere": {"ro": "Mititei tradiționali la grătar serviți cu cartofi copți și salată proaspătă.", "en": "Traditional grilled mititei served with roasted potatoes and fresh salad.", "th": "ไส้กรอกย่างสไตล์มอลโดวาเสิร์ฟพร้อมมันฝรั่งอบและสลัดสด"},
        "imagine": "/static/img/mititei.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 350}]
    },
    "m_11": {
        "categorie": "main_dishes",
        "nume": {"ro": "Pârjoale cu hrișcă", "en": "Cutlets with buckwheat", "th": "คัดเล็ทเสิร์ฟพร้อมบัควีท"},
        "descriere": {"ro": "Pârjoale suculente de casă servite cu hrișcă.", "en": "Juicy homemade cutlets served with buckwheat.", "th": "คัดเล็ทเนื้อบดเสิร์ฟพร้อมบัควีท"},
        "imagine": "/static/img/cutlets_buckwheat.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 300}]
    },
    "m_12": {
        "categorie": "main_dishes",
        "nume": {"ro": "Pulpă de rață cu piure și salată", "en": "Duck leg with mashed potato & salad", "th": "น่องเป็ดเสิร์ฟพร้อมมันบดและสลัด"},
        "descriere": {"ro": "Pulpă fragedă de rață la cuptor cu piure de cartofi și salată.", "en": "Tender roasted duck leg served with mashed potatoes and salad.", "th": "น่องเป็ดอบนุ่มเสิร์ฟพร้อมมันบดและสลัดสด"},
        "imagine": "/static/img/duck_leg.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 350}]
    },
    "m_13": {
        "categorie": "main_dishes",
        "nume": {"ro": "Piept de rață cu cartofi copți și salată", "en": "Duck breast with roasted potatoes & salad", "th": "อกเป็ดเสิร์ฟพร้อมมันฝรั่งอบและสลัด"},
        "descriere": {"ro": "Piept de rață suculent servit cu cartofi copți și salată.", "en": "Juicy duck breast served with roasted potatoes and salad.", "th": "อกเป็ดเนื้อฉ่ำเสิร์ฟพร้อมมันฝรั่งอบและสลัด"},
        "imagine": "/static/img/duck_breast.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 350}]
    },
    "m_14": {
        "categorie": "main_dishes",
        "nume": {"ro": "Pârjoală Kiev cu piure și salată", "en": "Chicken kiev with mashed potatoes & salad", "th": "ไก่ไคฟ์เสิร์ฟพร้อมมันบดและสลัด"},
        "descriere": {"ro": "Pârjoală Kiev crocantă umplută cu unt, servită cu piure și salată.", "en": "Crispy Chicken Kiev stuffed with butter, served with mashed potatoes and salad.", "th": "ไก่ไคฟ์ยัดไส้เนยทอดกรอบเสิร์ฟพร้อมมันบดและสลัด"},
        "imagine": "/static/img/chicken_kiev.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 350}]
    },
    "m_15": {
        "categorie": "main_dishes",
        "nume": {"ro": "File de scrumbie sărată cu cartofi copți și ceapă", "en": "Salted file mackerel with roasted potatoes and onion", "th": "ฟิเลต์ปลาแมคเคอเรลเค็มเสิร์ฟพร้อมมันฝรั่งอบและหอมใหญ่"},
        "descriere": {"ro": "File de macrou sărat servit cu cartofi copți și ceapă.", "en": "Salted mackerel fillet served with roasted potatoes and onion.", "th": "ฟิเลต์ปลาแมคเคอเรลเค็มเสิร์ฟพร้อมมันฝรั่งอบและหอมใหญ่"},
        "imagine": "/static/img/mackerel_roasted_potatoes.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 300}]
    },
    "m_16": {
        "categorie": "main_dishes",
        "nume": {"ro": "Roșii scăzute cu ardei copt la grătar", "en": "Stewed tomatoes with grilled bell pepper", "th": "มะเขือเทศเคี่ยวเสิร์ฟพร้อมพริกหยวกย่าง"},
        "descriere": {"ro": "Roșii scăzute aromate alături de ardei dulce copt pe grătar.", "en": "Aromatic stewed tomatoes served with sweet grilled bell pepper.", "th": "มะเขือเทศเคี่ยวรสเข้มข้นเสิร์ฟพร้อมพริกหยวกย่าง"},
        "imagine": "/static/img/stewed_tomatoes.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 250}]
    },
    "m_17": {
        "categorie": "main_dishes",
        "nume": {"ro": "Sarmale", "en": "Sarmale", "th": "ซาร์มาเล (กะหล่ำปลีห่อไส้เนื้อ)"},
        "descriere": {"ro": "Sarmale tradiționale din foi de varză umplute cu carne și orez.", "en": "Traditional cabbage rolls stuffed with minced meat and rice.", "th": "กะหล่ำปลีห่อไส้เนื้อบดและข้าวสไตล์มอลโดวาดั้งเดิม"},
        "imagine": "/static/img/sarmale.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 350}]
    },
    "m_18": {
        "categorie": "main_dishes",
        "nume": {"ro": "Plăcintă cu brânză de vaci", "en": "Placinta with cottage cheese", "th": "พลาชินตาไส้คอทเทจชีส"},
        "descriere": {"ro": "Plăcintă tradițională caldă umplută cu brânză proaspătă de vaci.", "en": "Traditional warm pie stuffed with fresh cottage cheese.", "th": "พายร้อนๆ สไตล์มอลโดวายัดไส้คอทเทจชีสสด"},
        "imagine": "/static/img/placinta_cheese.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 200}]
    },
    "m_19": {
        "categorie": "main_dishes",
        "nume": {"ro": "Plăcintă cu varză", "en": "Placinta with cabbage", "th": "พลาชินตาไส้กะหล่ำปลี"},
        "descriere": {"ro": "Plăcintă tradițională umplută cu varză.", "en": "Traditional pie stuffed with cabbage.", "th": "พายสไตล์มอลโดวาไส้กะหล่ำปลี"},
        "imagine": "/static/img/placinta_cabbage.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 180}]
    },
    "m_20": {
        "categorie": "main_dishes",
        "nume": {"ro": "Plăcintă cu cartofi", "en": "Placinta with potatoes", "th": "พลาชินตาไส้มันฝรั่ง"},
        "descriere": {"ro": "Plăcintă tradițională umplută cu cartofi.", "en": "Traditional pie stuffed with potatoes.", "th": "พายสไตล์มอลโดวาไส้มันฝรั่ง"},
        "imagine": "/static/img/placinta_potatoes.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 180}]
    },


    # --- GARNITURI ---
    "7": {
        "categorie": "garnituri",
        "nume": {"ro": "Bile de cartofi cu cașcaval", "en": "Potato cheese balls", "th": "มันฝรั่งทอดไส้ชีส"},
        "descriere": {"ro": "Bule crocante de cartofi umplute cu cașcaval topit.",
                      "en": "Crispy potato balls filled with melted cheese.", "th": "มันฝรั่งทอดกรอบไส้ชีสเยิ้ม"},
        "imagine": "/static/img/potato_balls.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 270}]
    },

    # --- BOTTLED BEER ---
    "alc_01": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Bere Leo 330 ml", "en": "Leo 330 ml", "th": "เบียร์ลีโอ 330 มล."},
        "descriere": {"ro": "Bere la sticlă Leo 330 ml.", "en": "Leo bottled beer 330 ml.",
                      "th": "เบียร์ลีโอแบบขวด 330 มล."},
        "imagine": "/static/img/beer_leo.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 100}]
    },
    "alc_02": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Bere Chang 330 ml", "en": "Chang 330 ml", "th": "เบียร์ช้าง 330 มล."},
        "descriere": {"ro": "Bere la sticlă Chang 330 ml.", "en": "Chang bottled beer 330 ml.",
                      "th": "เบียร์ช้างแบบขวด 330 มล."},
        "imagine": "/static/img/beer_chang.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 100}]
    },
    "alc_03": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Bere Singha 330 ml", "en": "Singha 330 ml", "th": "เบียร์สิงห์ 330 มล."},
        "descriere": {"ro": "Bere la sticlă Singha 330 ml.", "en": "Singha bottled beer 330 ml.",
                      "th": "เบียร์สิงห์แบบขวด 330 มล."},
        "imagine": "/static/img/beer_singha.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 100}]
    },
    "alc_04": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Bere Heineken 330 ml", "en": "Heineken 330 ml", "th": "เบียร์ไฮเนเก้น 330 มล."},
        "descriere": {"ro": "Bere la sticlă Heineken 330 ml.", "en": "Heineken bottled beer 330 ml.",
                      "th": "เบียร์ไฮเนเก้นแบบขวด 330 มล."},
        "imagine": "/static/img/beer_heineken.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 100}]
    },

    # --- GIN ---
    "alc_05": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Gin Gordon's", "en": "Gordon's gin", "th": "ยีน กอร์ดอนส์"},
        "descriere": {"ro": "Gin clasic Gordon's.", "en": "Classic Gordon's gin.", "th": "ยีน กอร์ดอนส์ รสดั้งเดิม"},
        "imagine": "/static/img/gin_gordons.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 140}]
    },
    "alc_06": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Gin Tonic", "en": "Gin tonic", "th": "ยีนโทนิค"},
        "descriere": {"ro": "Cocktail clasic Gin Tonic.", "en": "Classic Gin Tonic cocktail.", "th": "ค็อกเทลยีนโทนิค"},
        "imagine": "/static/img/gin_tonic.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 180}]
    },

    # --- VODKA ---
    "alc_07": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Vodcă Absolut", "en": "Absolute vodka", "th": "วอดก้า แอ็บโซลูท"},
        "descriere": {"ro": "Vodcă clasică Absolut.", "en": "Classic Absolut vodka.",
                      "th": "วอดก้า แอ็บโซลูท รสดั้งเดิม"},
        "imagine": "/static/img/vodka_absolut.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 150}]
    },

    # --- WINE ---
    "alc_08": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Vin alb la pahar 150 ml", "en": "White wine by glass 150 ml", "th": "ไวน์ขาวแก้ว 150 มล."},
        "descriere": {"ro": "Pahar de vin alb proaspăt 150 ml.", "en": "A glass of fresh white wine 150 ml.",
                      "th": "ไวน์ขาวเสิร์ฟเป็นแก้ว 150 มล."},
        "imagine": "/static/img/white_wine_glass.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 300}]
    },
    "alc_09": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Vin roșu la pahar 150 ml", "en": "Red wine by glass 150 ml", "th": "ไวน์แดงแก้ว 150 มล."},
        "descriere": {"ro": "Pahar de vin roșu aromate 150 ml.", "en": "A glass of rich red wine 150 ml.",
                      "th": "ไวน์แดงเสิร์ฟเป็นแก้ว 150 มล."},
        "imagine": "/static/img/red_wine_glass.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 300}]
    },

    # --- WHISKEY ---
    "alc_10": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Whisky Ballantine's", "en": "Ballantine's whiskey", "th": "วิสกี้ บัลลันไทน์"},
        "descriere": {"ro": "Whisky scoțian Ballantine's.", "en": "Ballantine's blended scotch whiskey.",
                      "th": "วิสกี้ บัลลันไทน์"},
        "imagine": "/static/img/whiskey_ballantines.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 150}]
    },
    "alc_11": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Whisky Jameson", "en": "Jameson whiskey", "th": "วิสกี้ เจมสัน"},
        "descriere": {"ro": "Whisky irlandez Jameson.", "en": "Jameson Irish whiskey.", "th": "วิสกี้ไอริช เจมสัน"},
        "imagine": "/static/img/whiskey_jameson.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 150}]
    },
    "alc_12": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Whisky Jack Daniel's", "en": "Jack Daniel's whiskey", "th": "วิสกี้ แจ็ค แดเนียลส์"},
        "descriere": {"ro": "Whisky american Jack Daniel's.", "en": "Jack Daniel's Tennessee whiskey.",
                      "th": "วิสกี้ แจ็ค แดเนียลส์"},
        "imagine": "/static/img/whiskey_jack_daniels.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 200}]
    },
    "alc_13": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Whisky Chivas", "en": "Chivas whiskey", "th": "วิสกี้ ชีวาส"},
        "descriere": {"ro": "Whisky scoțian Chivas Regal.", "en": "Chivas Regal blended scotch whiskey.",
                      "th": "วิสกี้ ชีวาส รีกัล"},
        "imagine": "/static/img/whiskey_chivas.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 200}]
    },

    # --- LIQUEURS ---
    "alc_14": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Lichior Jägermeister", "en": "Jagermeister liqueur", "th": "ลิเคียวร์ เยเกอร์ไมสเตอร์"},
        "descriere": {"ro": "Lichior german din plante Jägermeister.", "en": "German herbal liqueur Jägermeister.",
                      "th": "เหล้าสมุนไพร เยเกอร์ไมสเตอร์"},
        "imagine": "/static/img/jagermeister.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 150}]
    },
    "alc_15": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Lichior Baileys", "en": "Baileys liqueur", "th": "ลิเคียวร์ เบลีย์ส"},
        "descriere": {"ro": "Lichior cremos irlandez Baileys.", "en": "Irish cream liqueur Baileys.",
                      "th": "เหล้าครีม เบลีย์ส"},
        "imagine": "/static/img/baileys.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 150}]
    },

    # --- CHAMPAGNE MOLDOVA ---
    "alc_16": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Spumant Cricova Muscat demisec", "en": "Cricova Muscat semidry sparkling wine",
                 "th": "สปาร์กลิงไวน์ คริโควา มัสแคท กึ่งแห้ง"},
        "descriere": {"ro": "Vin spumant moldovenesc Cricova Muscat demisec.",
                      "en": "Moldovan semidry sparkling wine Cricova Muscat.",
                      "th": "สปาร์กลิงไวน์มอลโดวา คริโควา มัสแคท"},
        "imagine": "/static/img/cricova_muscat.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 1500}]
    },
    "alc_17": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Spumant Cricova roșu demisec", "en": "Cricova Red semidry sparkling wine",
                 "th": "สปาร์กลิงไวน์แดง คริโควา กึ่งแห้ง"},
        "descriere": {"ro": "Vin spumant roșu moldovenesc Cricova demisec.",
                      "en": "Moldovan red semidry sparkling wine Cricova.", "th": "สปาร์กลิงไวน์แดงมอลโดวา คริโควา"},
        "imagine": "/static/img/cricova_red.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 1500}]
    },
    "alc_18": {
        "categorie": "alcohol_drinks",
        "nume": {"ro": "Spumant Cricova rosé demisec", "en": "Cricova Rose semidry sparkling wine",
                 "th": "สปาร์กลิงไวน์โรเซ่ คริโควา กึ่งแห้ง"},
        "descriere": {"ro": "Vin spumant rosé moldovenesc Cricova demisec.",
                      "en": "Moldovan rose semidry sparkling wine Cricova.", "th": "สปาร์กลิงไวน์โรเซ่มอลโดวา คริโควา"},
        "imagine": "/static/img/cricova_rose.jpg",
        "optiuni": [{"id_opt": "1 porție", "pret": 1500}]
    }
}

@app.route('/')
def home():
    lang = session.get('limba', 'ro')
    return render_template('index.html', produse=PRODUSE, categorii=CATEGORII, lang=lang, texte=TEXTE.get(lang, TEXTE['ro']))

@app.route('/produs/<id>')
def produs_detail(id):
    produs = PRODUSE.get(id)
    if not produs:
        abort(404)
    lang = session.get('limba', 'ro')
    return render_template('produs.html', id=id, produs=produs, lang=lang, texte=TEXTE.get(lang, TEXTE['ro']))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    produs_id = request.form.get('produs_id')
    optiune_id = request.form.get('optiune')
    cantitate = int(request.form.get('cantitate', 1))

    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']
    cart.append({'id': produs_id, 'optiune': optiune_id, 'cantitate': cantitate})
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cosul_meu = []
    total = 0
    lang = session.get('limba', 'ro')

    if 'cart' in session:
        for item in session['cart']:
            prod_id = item.get('id')
            opt_id = item.get('optiune')
            cantitate = item.get('cantitate', 1)
            produs = PRODUSE.get(prod_id)

            if produs:
                pret_unitar = 0
                for opt in produs['optiuni']:
                    if opt['id_opt'] == opt_id:
                        pret_unitar = opt['pret']
                        break
                if pret_unitar == 0 and produs['optiuni']:
                    pret_unitar = produs['optiuni'][0]['pret']

                subtotal = pret_unitar * cantitate
                cosul_meu.append({
                    'nume': produs['nume'].get(lang, produs['nume']['ro']),
                    'optiune': opt_id if opt_id else "1 porție",
                    'cantitate': cantitate,
                    'pret': subtotal
                })
                total += subtotal

    return render_template('cart.html', cosul_meu=cosul_meu, total=total, lang=lang, texte=TEXTE.get(lang, TEXTE['ro']))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    lang = session.get('limba', 'ro')
    if request.method == 'POST':
        session.pop('cart', None)
        return redirect(url_for('success'))
    return render_template('checkout.html', lang=lang, texte=TEXTE.get(lang, TEXTE['ro']))

@app.route('/success')
def success():
    lang = session.get('limba', 'ro')
    return render_template('success.html', lang=lang, texte=TEXTE.get(lang, TEXTE['ro']))

@app.route('/set_lang/<limba>')
def set_lang(limba):
    if limba in ['ro', 'en', 'th']:
        session['limba'] = limba
    return redirect(request.referrer or url_for('home'))

# Aici se termină celelalte rute ale tale...

@app.route('/sterge_produs/<int:item_index>')
def sterge_produs(item_index):
    if 'cart' in session:
        cart = session['cart']
        if 0 <= item_index < len(cart):
            cart.pop(item_index)
            session['cart'] = cart
            session.modified = True
    return redirect(url_for('cart'))

# Acestea trebuie să rămână ultimele două rânduri din TOT fișierul:
if __name__ == '__main__':
    app.run(debug=True)