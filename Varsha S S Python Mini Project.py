import os
import datetime as d
from PIL import Image
import pygame as pg
import time as t
import speech_recognition as sr
import webbrowser as wb

ACCOUNT_FILE = "account.txt"
SESSION_FILE = "session.txt"

def registration():
    username = input("Create Username: ")
    password = input("Create Password: ")
    with open(ACCOUNT_FILE, "w") as f:
        f.write(username + "\n" + password)
    print("\n✅Account Created Successfully.")

def login():
    with open(ACCOUNT_FILE, "r") as f:
        Username = f.readline().strip()
        Password = f.readline().strip()
    attempt = 0
    while attempt < 3:
        u = input("Username: ")
        p = input("Password: ")
        if u == Username and p == Password:
            with open(SESSION_FILE,"w") as f:
                f.write("True")
            print("\n✅Login Successful")
            return
        else:
            attempt += 1
            print("Attempts left:", 3 - attempt)

    print("Too many attempts")
    exit()

def logout():
    with open(SESSION_FILE,"w") as f:
        f.write("False")
    print("Logged Out Successfully")

def check_session():
    if not os.path.exists(SESSION_FILE):
        return False
    with open(SESSION_FILE,"r") as f:
        return f.read().strip() == "True"

def get_valid_name():
    while True:
        name = input("Enter Name: ")
        if name.replace(" ", "").isalpha():
            return name
        print("Invalid Name")

def get_valid_mobile():
    while True:
        mobile = input("Enter Mobile Number: ")
        if len(mobile) == 10 and mobile.isdigit() and mobile[0] in "6789":
            return mobile
        print("Invalid Mobile Number")

def get_valid_email():
    while True:
        email = input("Enter Email ID: ")
        if "@" in email and "." in email and email.index("@") < email.rindex("."):
            return email
        print("Invalid Email")

def Voice_search():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Speak a Product or Category...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)
        return text

    except Exception as e:
        print("Error:", e)
        return ""

CATEGORY_KEYWORDS = {
    "Grocery": [
        "rice", "wheat", "atta", "oil", "milk", "bread", "egg", "vegetables",
        "fruits", "snacks", "biscuits", "juice", "soft drink", "coffee",
        "tea", "sugar", "salt", "spices", "dal", "soap"
    ],

    "Electronics": [
        "mobile", "smartphone", "laptop", "tablet", "tv", "television",
        "headphones", "earbuds", "speaker", "camera", "printer", "mouse",
        "keyboard", "monitor", "powerbank", "charger", "router", "ssd",
        "hard disk", "smartwatch"
    ],

    "Fashion & Lifestyle": [
        "shirt", "tshirt", "jeans", "dress", "kurti", "hoodie", "jacket",
        "saree", "leggings", "shorts", "blazer", "skirt", "top",
        "nightwear", "tracks", "shoes", "sandals", "slippers", "heels",
        "handbag"
    ],

    "Beauty & Personal Care": [
        "face wash", "cleanser", "serum", "moisturizer", "sunscreen",
        "lipstick", "foundation", "compact", "concealer", "mascara",
        "eyeliner", "face cream", "toner", "face pack", "body lotion",
        "perfume", "deodorant", "makeup", "primer", "blush"
    ],

    "Books & Stationery": [
        "novel", "storybook", "dictionary", "guide", "textbook",
        "notebook", "journal", "pen", "pencil", "eraser",
        "highlighter", "marker", "geometry box", "file", "diary"
    ],

    "Furniture & Home Decor": [
        "chair", "table", "sofa", "bed", "wardrobe", "cupboard",
        "bookshelf", "study table", "bean bag", "dining table",
        "tv unit", "computer table", "office chair", "shoe rack"
    ],

    "Toys & Baby Products": [
        "lego", "barbie", "car", "remote car", "drone", "teddy",
        "building blocks", "puzzle", "robot", "doll",
        "action figure", "baby toy", "board game"
    ],

    "Pet Supplies": [
        "dog food", "cat food", "pet shampoo", "pet toy",
        "pet leash", "collar", "pet bed", "cat litter",
        "pet treats", "pet bowl", "pet brush"
    ],

    "Sports & Fitness": [
        "cricket bat", "football", "volleyball", "basketball",
        "badminton racket", "tennis racket", "gym gloves",
        "dumbbells", "yoga mat", "cycling helmet", "treadmill"
    ],

    "Watches & Accessories": [
        "watch", "smartwatch", "analog watch", "digital watch",
        "fitness band", "luxury watch", "strap"
    ],

    "Jewellery": [
        "ring", "chain", "necklace", "bracelet", "earrings",
        "anklet", "bangle", "pendant", "nose pin"
    ],

    "Games": [
        "ps5", "xbox", "gamepad", "gaming mouse", "gaming keyboard",
        "gaming chair", "gaming headset", "steam card",
        "playstation game"
    ],

    "Gifts & Flowers": [
        "gift", "gift box", "bouquet", "flowers", "rose",
        "teddy", "chocolate", "greeting card", "photo frame"
    ],

    "Arts & Crafts": [
        "paint", "canvas", "brush", "colour pencils",
        "water colours", "acrylic colours", "craft paper",
        "glue gun", "origami paper", "sketchbook"
    ],

    "Automobile Accessories": [
        "helmet", "car cover", "seat cover", "engine oil",
        "bike cover", "air freshener", "car charger",
        "car vacuum", "tyre inflator", "phone holder"
    ]
}

CATEGORY_ALIASES = {
    "grocery": "Grocery",
    "food": "Food Delivery",
    "food delivery": "Food Delivery",
    "cake": "Cakes & Bakery",
    "cakes": "Cakes & Bakery",
    "bakery": "Cakes & Bakery",
    "fashion": "Fashion & Lifestyle",
    "lifestyle": "Fashion & Lifestyle",
    "beauty": "Beauty & Personal Care",
    "personal care": "Beauty & Personal Care",
    "electronics": "Electronics",
    "books": "Books & Stationery",
    "stationery": "Books & Stationery",
    "furniture": "Furniture & Home Decor",
    "home decor": "Furniture & Home Decor",
    "toys": "Toys & Baby Products",
    "baby": "Toys & Baby Products",
    "pets": "Pet Supplies",
    "pet": "Pet Supplies",
    "sports": "Sports & Fitness",
    "fitness": "Sports & Fitness",
    "watch": "Watches & Accessories",
    "watches": "Watches & Accessories",
    "jewellery": "Jewellery",
    "jewelry": "Jewellery",
    "gaming": "Games",
    "games": "Games",
    "gifts": "Gifts & Flowers",
    "flowers": "Gifts & Flowers",
    "arts": "Arts & Crafts",
    "crafts": "Arts & Crafts",
    "automobile": "Automobile Accessories",
    "car": "Automobile Accessories",
    "bike": "Automobile Accessories"
}

def detect_category(product_name):
    product_name = product_name.lower()

    # 1. Check aliases
    if product_name in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[product_name]

    # 2. Check full category names
    for category in CATEGORY_FUNCTIONS:
        if product_name == category:
            return category

    # 3. Check product keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in product_name:
                return category

    # 4. Default
    return "General E-Commerce"

# 1. Grocery
def Grocery():
    print("1.Jiomart",
          "2.Blinkit",
          "3.Zepto",
          "4.Swiggy Instamart",
          "5.BigBasket",
          "6.Flipkart Minutes",
          sep="\n"
          )
    groc_website = int(input("Enter your website:"))

    if groc_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.jiomart.com/sections/quick-grocery-new")
    elif groc_website == 2:
        print("Your magic shopping website")
        wb.open("https://blinkit.com/")
    elif groc_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.zepto.com/")
    elif groc_website == 4:
        print("Your magic shopping website")
        wb.open("https://instamart.in/")
    elif groc_website == 5:
        print("Your magic shopping website")
        wb.open("https://www.bigbasket.com/")
    elif groc_website == 6:
        print("Your magic shopping website")
        wb.open("https://www.flipkart.com/flipkart-minutes-store?marketplace=HYPERLOCAL")
    else:
        print("Please enter a valid website")

# 2.Food Delivery
def Food_delivery():
    print("1.Swiggy",
          "2.Zomato",
          sep="\n"
          )
    food_website = int(input("Enter your website:"))

    if food_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.swiggy.com/")
    elif food_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.zomato.com/")
    else:
        print("Please enter a valid website")

# 3.Cakes & Bakery
def Cake_Bakery():
    print("1.Ferns N Petals",
          "2.Bakingo",
          "3.Winni",
          "4.IGP",
          sep="\n"
          )
    Cake_website = int(input("Enter your website:"))

    if Cake_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.fnp.com/")
    elif Cake_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.bakingo.com/")
    elif Cake_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.winni.in/")
    elif Cake_website == 4:
        print("Your magic shopping website")
        wb.open("https://www.igp.com/")
    else:
        print("Please enter a valid website")

# 4.Fashion & Lifestyle
def Fashion_Lifestyle():
    print("1.Myntra",
          "2.Ajio",
          "3.Nykaa fashion",
          "4.Limeroad",
          sep="\n"
          )
    fashion_website = int(input("Enter your website:"))

    if fashion_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.myntra.com/")
    elif fashion_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.ajio.com/")
    elif fashion_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.nykaafashion.com/")
    elif fashion_website == 4:
        print("Your magic shopping website")
        wb.open("https://www.limeroad.com/")
    else:
        print("Please enter a valid website")

# 5.Beauty & Personal care
def Beauty_Personal_care():
    print("1.Nykaa",
          "2.Purplle",
          sep="\n"
          )
    Beauty_website = int(input("Enter your website:"))

    if Beauty_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.nykaa.com/")
    elif Beauty_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.purplle.com/")
    else:
        print("Please enter a valid website")

# 6.Watches & Accessories
def Watches_Accessories():
    print("1.Titan",
          "2.Fastrack",
          "3.Helios",
          sep="\n"
          )
    Watches_website = int(input("Enter your website:"))

    if Watches_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.titan.co.in/")
    elif Watches_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.fastrack.in/")
    elif Watches_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.helioswatchstore.com/")
    else:
        print("Please enter a valid website")

# 7.Jewellery
def Jewellery():
    print("1.Tanishq",
          "2.Bluestone",
          "3.Caratlane",
          sep="\n"
          )
    Jewellery_website = int(input("Enter your website:"))

    if Jewellery_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.tanishq.co.in/")
    elif Jewellery_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.bluestone.com/")
    elif Jewellery_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.caratlane.com/")
    else:
        print("Please enter a valid website")

# 8.Gifts & Flowers
def Gifts():
    print("1.Ferns N Petals",
          "2.IGP",
          "3.FlowerAura",
          "4.Winni",
          sep="\n"
          )
    Gifts_website = int(input("Enter your website:"))

    if Gifts_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.fnp.com/")
    elif Gifts_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.igp.com/")
    elif Gifts_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.floweraura.com/")
    elif Gifts_website == 4:
        print("Your magic shopping website")
        wb.open("https://www.winni.in/")
    else:
        print("Please enter a valid website")

# 9.Arts & Crafts
def Arts_Craft():
    print("1.Itsy Bitsy")
    ac_website = int(input("Enter your website:"))

    if ac_website == 1:
        print("Your magic shopping website")
        wb.open("https://itsybitsy.in/")
    else:
        print("Please enter a valid website")

# 10.Online Pharmacy
def Online_Pharmacy():
    print("1.Tata 1mg",
          "2.Apollo 24/7",
          "3.Netmeds",
          sep="\n"
          )
    Pharmacy_website = int(input("Enter your website:"))

    if Pharmacy_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.1mg.com/")
    elif Pharmacy_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.apollopharmacy.in/")
    elif Pharmacy_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.netmeds.com/")
    else:
        print("Please enter a valid website")

# 11.Furniture & Home Decor
def Furniture_HomeDecor():
    print("1.Pepperfry",
          "2.IKEA India",
          "3.Homecenter",
          "4.Urban Ladder",
          sep="\n"
          )
    Furniture_website = int(input("Enter your website:"))

    if Furniture_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.pepperfry.com/")
    elif Furniture_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.ikea.com/in/en/")
    elif Furniture_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.homecentre.in/")
    elif Furniture_website == 4:
        print("Your magic shopping website")
        wb.open("https://www.urbanladder.com/")
    else:
        print("Please enter a valid website")

# 12.Electronics
def Electronics():
    print("1.Croma",
          "2.Reliance Digital",
          sep="\n"
          )
    Electronics_website = int(input("Enter your website:"))

    if Electronics_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.croma.com/")
    elif Electronics_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.reliancedigital.in/")
    else:
        print("Please enter a valid website")

# 13.Toys & Baby Products
def Toys_Babycare():
    print("1.FirstCry",
          "2.Hamleys",
          "3.Hopscotch",
          sep="\n"
          )
    Toys_Babycare_website = int(input("Enter your website:"))

    if Toys_Babycare_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.firstcry.com/")
    elif Toys_Babycare_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.hamleys.in/")
    elif Toys_Babycare_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.hopscotch.in/")
    else:
        print("Please enter a valid website")

# 14.Pet Supplies
def Pet_care():
    print("1.Supertails",
          "2.Heads up for Tails",
          "3.PetShopIndia",
          sep="\n"
          )
    Pet_care_website = int(input("Enter your website:"))

    if Pet_care_website == 1:
        print("Your magic shopping website")
        wb.open("https://supertails.com/")
    elif Pet_care_website == 2:
        print("Your magic shopping website")
        wb.open("https://headsupfortails.com/")
    elif Pet_care_website == 3:
        print("Your magic shopping website")
        wb.open("https://petshopindia.com/")
    else:
        print("Please enter a valid website")

# 15.Books & Stationery
def Books_Stationery():
    print("1.Amazon Books",
          "2.Flipkart Books",
          "3.Bookswagon",
          "4.Crossword",
          sep="\n"
          )
    Book_website = int(input("Enter your website:"))

    if Book_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.amazon.in/books")
    elif Book_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.flipkart.com/books")
    elif Book_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.bookswagon.com/")
    elif Book_website == 4:
        print("Your magic shopping website")
        wb.open("https://www.crossword.in/")
    else:
        print("Please enter a valid website")

# 16.Gardening & Plants
def Gardening():
    print("1.Nursery Live",
          "2.Ugaoo",
          sep="\n"
          )
    Gardening_website = int(input("Enter your website:"))

    if Gardening_website == 1:
        print("Your magic shopping website")
        wb.open("https://nurserylive.com/")
    elif Gardening_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.ugaoo.com/")
    else:
        print("Please enter a valid website")

# 17. Sports & Fitness
def Sports():
    print("1.Decathlon",
          "2.Cultsport",
          sep="\n"
          )
    Sports_website = int(input("Enter your website:"))

    if Sports_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.decathlon.in/")
    elif Sports_website == 2:
        print("Your magic shopping website")
        wb.open("https://cultsport.com/")
    else:
        print("Please enter a valid website")

# 18. Games
def Games():
    print("1.Steam",
          "2.Epic Games",
          "3.Games The Shop",
          sep="\n"
          )
    Game_website = int(input("Enter your website:"))

    if Game_website == 1:
        print("Your magic shopping website")
        wb.open("https://store.steampowered.com/")
    elif Game_website == 2:
        print("Your magic shopping website")
        wb.open("https://store.epicgames.com/")
    elif Game_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.gamestheshop.com/")
    else:
        print("Please enter a valid website")

# 19. Music & Entertainment Merchandise
def Music_Merch():
    print("1.Weverse Shop",
          "2.The Entertainment Store India",
          "3.Redwolf",
          "4.The Soulful Store",
          "5.Hamleys",
          sep="\n"
          )
    Music_Merch_website = int(input("Enter your website:"))

    if Music_Merch_website == 1:
        print("Your magic shopping website")
        wb.open("https://shop.weverse.io/en/home")
    elif Music_Merch_website == 2:
        print("Your magic shopping website")
        wb.open("https://entertainmentstore.in/")
    elif Music_Merch_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.redwolf.in/")
    elif Music_Merch_website == 4:
        print("Your magic shopping website")
        wb.open("https://www.thesouledstore.com/")
    elif Music_Merch_website == 5:
        print("Your magic shopping website")
        wb.open("https://hamleys.in/")
    else:
        print("Please enter a valid website")

# 20.Automobile Accessories
def Automobile():
    print("1.Boodmo",
          "2.Carorbis",
          "3.Autofurnish",
          "4.AutoFreak",
          "5.Motoroids Store",
          "6.99RPM",
          sep="\n"
          )
    Automobile_website = int(input("Enter your website:"))

    if Automobile_website == 1:
        print("Your magic shopping website")
        wb.open("https://boodmo.com/")
    elif Automobile_website == 2:
        print("Your magic shopping website")
        wb.open("https://carorbis.com/")
    elif Automobile_website == 3:
        print("Your magic shopping website")
        wb.open("https://autofurnish.com/")
    elif Automobile_website == 4:
        print("Your magic shopping website")
        wb.open("https://autofreak.in/")
    elif Automobile_website == 5:
        print("Your magic shopping website")
        wb.open("https://motoroids.com")
    elif Automobile_website == 6:
        print("Your magic shopping website")
        wb.open("https://www.99rpm.com/")
    else:
        print("Please enter a valid website")

# 21.Luxury Shopping
def Luxury():
    print("1.Gucci",
          "2.Dior",
          "3.Chanel",
          "4.Celine",
          "5.Calvin Klein",
          "6.Prada",
          "7.Valentino",
          "8.Louis Vuitton",
          sep="\n"
          )
    Luxury_website = int(input("Enter your website:"))

    if Luxury_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.gucci.com/")
    elif Luxury_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.dior.com/")
    elif Luxury_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.chanel.com/")
    elif Luxury_website == 4:
        print("Your magic shopping website")
        wb.open("https://www.celine.com/")
    elif Luxury_website == 5:
        print("Your magic shopping website")
        wb.open("https://www.calvinklein.in/")
    elif Luxury_website == 6:
        print("Your magic shopping website")
        wb.open("https://www.prada.com/")
    elif Luxury_website == 7:
        print("Your magic shopping website")
        wb.open("https://www.valentino.com/")
    elif Luxury_website == 8:
        print("Your magic shopping website")
        wb.open("https://in.louisvuitton.com/")
    else:
        print("Please enter a valid website")

# 22.General
def General():
    print("1.Amazon",
          "2.Flipkart",
          "3.Meesho",
          "4.Snapdeal",
          sep="\n"
          )
    General_website = int(input("Enter your website:"))

    if General_website == 1:
        print("Your magic shopping website")
        wb.open("https://www.amazon.in/")
    elif General_website == 2:
        print("Your magic shopping website")
        wb.open("https://www.flipkart.com/")
    elif General_website == 3:
        print("Your magic shopping website")
        wb.open("https://www.meesho.com/")
    elif General_website == 4:
        print("Your magic shopping website")
        wb.open("https://www.snapdeal.com/")
    else:
        print("Please enter a valid website")

CATEGORY_FUNCTIONS = {

    "grocery": Grocery,
    "food delivery": Food_delivery,
    "cakes & bakery": Cake_Bakery,
    "fashion & lifestyle": Fashion_Lifestyle,
    "beauty & personal care": Beauty_Personal_care,
    "watches & accessories": Watches_Accessories,
    "jewellery": Jewellery,
    "gifts & flowers": Gifts,
    "Arts & crafts": Arts_Craft,
    "online pharmacy": Online_Pharmacy,
    "furniture & home decor": Furniture_HomeDecor,
    "electronics": Electronics,
    "toys & baby products": Toys_Babycare,
    "pet supplies": Pet_care,
    "books & stationery": Books_Stationery,
    "gardening & plants": Gardening,
    "sports & fitness": Sports,
    "games": Games,
    "music & entertainment merchandise": Music_Merch,
    "automobile accessories": Automobile,
    "luxury shopping": Luxury,
    "general e-commerce": General
}

def show_categories():
    print("\n========== AVAILABLE CATEGORIES ==========\n")

    print("1. Grocery 🥦")
    print("2. Food Delivery 🍕")
    print("3. Cakes & Bakery 🎂")
    print("4. Fashion & Lifestyle 👕")
    print("5. Beauty & Personal Care 💄")
    print("6. Watches & Accessories ⌚")
    print("7. Jewellery 💍")
    print("8. Gifts & Flowers 🎁")
    print("9. Arts & Crafts 🎨")
    print("10. Online Pharmacy 💊")
    print("11. Furniture & Home Decor 🛋️")
    print("12. Electronics 💻")
    print("13. Toys & Baby Products 🧸")
    print("14. Pet Supplies 🐶")
    print("15. Books & Stationery 📚")
    print("16. Gardening & Plants 🌱")
    print("17. Sports & Fitness ⚽")
    print("18. Gaming 🎮")
    print("19. Music & Entertainment Merchandise 🎵")
    print("20. Automobile Accessories 🚗")
    print("21. Luxury Shopping 💎")
    print("22. General E-Commerce 🛒")

    print("\nYou can say/type a PRODUCT or a CATEGORY.\n")

def start():
    if not os.path.exists(ACCOUNT_FILE):

        print("\n" + "=" * 50)
        print("STEP 1️⃣ : CREATE ACCOUNT")
        print("=" * 50)

        registration()

        print("\n✅ Account Created Successfully!")

        print("\n" + "-" * 50)
        print("STEP 2️⃣ : LOGIN")
        print("-" * 50)

        login()

    else:

        print("\n" + "=" * 50)
        print("STEP 2️⃣ : LOGIN")
        print("=" * 50)

        login()

def show_logo():
    logo = Image.open(r"C:\Users\ADMIN\Downloads\Magic Shop Logo.png")
    logo.show()

def play_intro_music():
    pg.init()
    pg.mixer.init()
    pg.mixer.music.load(r"C:\Users\ADMIN\Downloads\bts_bighit_intro.mp3")
    pg.mixer.music.set_volume(0.7)
    pg.mixer.music.play()
    t.sleep(5)
    pg.mixer.music.stop()

print("\n" + "=" * 50)
print("           ✨ MAGIC SHOP ✨")
print("=" * 50)

show_logo()

play_intro_music()

start()

print("\n" + "=" * 50)
print("STEP 3️⃣ : USER DETAILS")
print("=" * 50)
name = get_valid_name()
mobile = get_valid_mobile()
email = get_valid_email()

print("\n✅Welcome", name)

while True:
    print("\n" + "=" * 50)
    print("STEP 4️⃣ : PRODUCT SEARCH")
    print("=" * 50)

    print("_._._ Magic Shop ✨ _._._")
    print(d.datetime.now())

    print("\nHow would you like to search?")

    print("1. Voice Search 🎤")
    print("2. Type Product ⌨️")
    print("3. Exit ❌")

    choice = input("Enter your choice: ")

    if choice == "1":
        show_categories()
        product = Voice_search()

    elif choice == "2":
        show_categories()
        product = input("Enter Product/Category Name: ").lower()

    elif choice == "3":
        print("\n" + "=" * 50)
        print("STEP 5️⃣ : LOGOUT")
        print("=" * 50)
        logout()
        print("\n👋 Thank You For Using Magic Shop!")
        break

    else:
        print("Invalid Choice")
        continue

    category = detect_category(product)
    print("\nDetected Category :", category)
    category_key = category.lower()

    if category_key in CATEGORY_FUNCTIONS:
        CATEGORY_FUNCTIONS[category_key]()

    else:
        print("Category not available.")

    print("\n" + "=" * 45)
    print("          😊 THANK YOU FOR USING 😊")
    print("               ✨ MAGIC SHOP ✨")
    print("              🛍 Happy Shopping 🛍")
    print("              👋🏼 See you again 👋🏼")
    print("=" * 45)