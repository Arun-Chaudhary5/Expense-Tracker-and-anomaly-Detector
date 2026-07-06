import random
import pandas as pd 
from faker import Faker
fake = Faker("en_IN")

BANKS=["HDFC Bank", "ICICI Bank", "Axis Bank", "State Bank of India", "Kotak Mahindra Bank", "Yes Bank", "IndusInd Bank", "Punjab National Bank", "Bank of Baroda", "Canara Bank"]
CITIES=["New Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
PAYMENT_MODES=["Credit Card", "Debit Card", "Net Banking", "UPI", "Wallet", "Cash on Delivery", "EMI", "BNPL"]

#This Method is prone to errors as we are working with large number of categories with two dictionaries.
#we can use a single dictionary to store the merchant database and amount ranges to avoid errors.
"""MERCHANT_DATABASE={"Food":["Zomato", "Swiggy Instamart","Swiggy Dineout" ,"Domino's", "McDonald's", "KFC", "Pizza Hut", "Burger King", "Subway", "Starbucks", "Cafe Coffee Day"]
                   ,"Clothing":["Myntra", "Ajio", "Flipkart", "Amazon India","Amazon.com", "H&M", "Zara Online","Zara Offline", "Levi's", "Nike", "Adidas", "Puma"],
                   "Electronics":["Croma Online", "Reliance Digital", "Vijay Sales", "Sony Center", "Samsung Store", "Apple Store India","Apple Store Online", "LG Store", "OnePlus Store", "Mi Store", "Motorola Store"],
,
                   "Travel":["MakeMyTrip", "Yatra", "Goibibo", "Cleartrip", "Expedia", "Booking.com", "Airbnb", "OYO Rooms", "Treebo Hotels", "FabHotels"],
                   "Entertainment":["BookMyShow", "PVR Cinemas", "INOX", "Cinepolis", "Carnival Cinemas", "Fun Cinemas", "Wave Cinemas", "City Gold Cinema", "SRS Cinemas", "Big Cinemas"],
                   "Health":["Apollo Pharmacy", "MedPlus", "1mg", "Netmeds", "PharmEasy", "Practo", "Lybrate", "DocPrime","HealthKart", "Pharmeasy"],
                   "Books":["Amazon Kindle", "Flipkart Books", "Book Depository", "Oxford Bookstore", "Landmark", "Crossword", "Sapna Book House", "Rupa Publications", "Penguin Random House India", "HarperCollins India"],
                   "Jewelry":["Tanishq", "Kalyan Jewellers", "Malabar Gold", "PC Jeweller", "CaratLane", "Senco Gold & Diamonds", "Joyalukkas", "GRT Jewellers", "Jubilee Diamonds", "Shubh Jewellers"],
                   "Sports":["Decathlon Online","Decathlon Offline", "Nike Store", "Adidas Store", "Puma Store", "Reebok Store", "Under Armour Store", "Asics Store", "New Balance Store", "Skechers Store", "Columbia Sportswear Store"],
                   "Home Appliances":["LG Store", "Samsung Store", "Sony Center", "Whirlpool Store", "Bosch Store", "IFB Store", "Panasonic Store", "Haier Store", "Videocon Store", "Godrej Appliances Store"],
                   "Furniture":["Urban Ladder", "Pepperfry", "IKEA India", "HomeTown", "Godrej Interio", "Nilkamal Furniture", "Durian Furniture", "Evok", "FabFurnish", "Wooden Street"],
                   "Automotive":["Maruti Suzuki Arena", "Hyundai Showroom", "Honda Showroom", "Toyota Showroom", "Mahindra Showroom", "Tata Motors Showroom", "Kia Showroom", "Renault Showroom", "Ford Showroom", "Volkswagen Showroom"],
                   "Education":["BYJU'S", "Unacademy", "Vedantu", "Toppr", "Khan Academy", "Coursera", "Udemy", "edX", "Skillshare", "LinkedIn Learning"],
                   "Real Estate":["99acres", "MagicBricks", "Housing.com", "NoBroker", "CommonFloor", "Makaan.com", "PropTiger", "Square Yards", "NestAway", "Zolo Stays"],
                   "Beauty":["Nykaa", "Purplle", "Sephora India", "The Body Shop India", "Forest Essentials", "Kama Ayurveda", "Mamaearth", "Plum Goodness", "Sugar Cosmetics", "Colorbar Cosmetics"]}

def generate_transaction_id(index):
    return f"TXN{index:06d}"

def generate_date():
    return fake.date_between(start_date='-1y', end_date='today')

category=random.choice(list(MERCHANT_DATABASE.keys()))
merchant = random.choice(MERCHANT_DATABASE[category])

AMOUNT_RANGE = {
    "Food": (150, 1200),
    "Shopping": (500, 12000),
    "Transport": (80, 1500),
    "Bills": (300, 4000),
    "Entertainment": (200, 3000),
    "Health": (300, 6000),
    "Education": (500, 25000),
    "Automobile": (500, 15000),
    "Travel": (1000, 30000),
    "Sports": (500, 8000),
    "Beauty": (200, 5000),
    "Home": (300, 15000),
    "Books": (150, 3000),
    "Jewelry": (5000, 100000)
}

amount = round(random.uniform(*AMOUNT_RANGE[category]), 2)

transaction = {
    "Transaction_ID": generate_transaction_id(1),
    "Date": str(generate_date()),
    "Category": category,
    "Merchant": merchant,
    "Amount": amount,
    "Bank": random.choice(BANKS),
    "City": random.choice(CITIES),
    "Payment_Mode": random.choice(PAYMENT_MODES)
}

print(transaction)"""


CATEGORY_INFO = {
    "Food": {
        "amount_range": (150, 1200),
        "merchants": ["Swiggy Instamart","Swiggy Dineout","Zomato","Blinkit","Domino's Online","Domino's Dineout","McDonald's","KFC","Pizza Hut","Burger King","Subway","Starbucks","Cafe Coffee Day"]
    },

    "Clothing": {
        "amount_range": (500, 8000),
        "merchants": ["Myntra","Ajio","Zara Online","Zara Offline","H&M","Flipkart","Amazon India","Amazon.com","Levi's","Nike","Adidas","Puma"]
    },
    "Home": {
        "amount_range": (300, 15000),
        "merchants": ["Urban Ladder","Pepperfry","IKEA India","HomeTown","Godrej Interio","Nilkamal Furniture","Durian Furniture","Evok","FabFurnish","Wooden Street"]
    },
    "Electronics": {
        "amount_range": (1000, 50000),
        "merchants": ["Croma Online","Reliance Digital","Vijay Sales","Sony Center","Samsung Store","Apple Store India","Apple Store Online","LG Store","OnePlus Store","Mi Store","Motorola Store"]
    },
    "Travel": {
        "amount_range": (1000, 30000),
        "merchants": ["MakeMyTrip","Yatra","Goibibo","Cleartrip","Expedia","Booking.com","Airbnb","OYO Rooms","Treebo Hotels","FabHotels","Uber","Ola","Redbus","Indigo","Spicejet","Goair","AirAsia"]
    },
    "Entertainment": {
        "amount_range": (200, 3000),
        "merchants": ["BookMyShow","PVR Cinemas","INOX","Cinepolis","Carnival Cinemas","Fun Cinemas","Wave Cinemas","City Gold Cinema","SRS Cinemas","Big Cinemas","Netflix","Prime Video","Hotstar","Zee5","Sony Liv","Voot","ALT Balaji"]
    },
    "Health": {
        "amount_range": (300, 6000),
        "merchants": ["Apollo Pharmacy","MedPlus","1mg","Netmeds","PharmEasy","Practo","Lybrate","DocPrime","HealthKart","Pharmeasy"]
    },
    "Books": {
        "amount_range": (150, 3000),
        "merchants": ["Kindle","Book Depository","Oxford Bookstore","Crossword","Sapna Book House","Rupa Publications","Penguin Random House India","HarperCollins India"]
    },
    "Jewelry": {
        "amount_range": (5000, 100000),
        "merchants": ["Tanishq","Kalyan Jewellers","Malabar Gold","PC Jeweller","CaratLane","Senco Gold & Diamonds","Joyalukkas","GRT Jewellers","Jubilee Diamonds","Shubh Jewellers"]
    },
    "Sports":  {
        "amount_range": (500, 8000),
        "merchants": ["Decathlon Online","Decathlon Offline","Reebok Store","Under Armour Store","Asics Store","New Balance Store","Skechers Store","Columbia Sportswear Store"]
    },
    "Beauty": {
        "amount_range": (200, 5000),
        "merchants": ["Nykaa","Purplle","Sephora India","The Body Shop India","Forest Essentials","Kama Ayurveda","Mamaearth","Plum Goodness","Sugar Cosmetics","Colorbar Cosmetics"]
    },
    "Education": {
        "amount_range": (500, 25000),
        "merchants": ["BYJU'S Online","BYJU'S Offline","Unacademy","Vedantu","Toppr","Khan Academy","Coursera","Udemy","edX","Skillshare","LinkedIn Learning"]
    },
    "Real Estate": {
        "amount_range": (10000, 500000),
        "merchants": ["99acres","MagicBricks","Housing.com","NoBroker","CommonFloor","Makaan.com","PropTiger","Square Yards","NestAway","Zolo Stays"]
    }
}

category = random.choice(list(CATEGORY_INFO.keys()))

merchant = random.choice(CATEGORY_INFO[category]["merchants"])

amount = round(
    random.uniform(*CATEGORY_INFO[category]["amount_range"]),
    2
)

def generate_transaction_id(index):
    return f"TXN{index:06d}"

def generate_date():
    return fake.date_between(start_date='-1y', end_date='today')


transaction = {
    "Transaction_ID": generate_transaction_id(1),
    "Date": str(generate_date()),
    "Category": category,
    "Merchant": merchant,
    "Amount": amount,
    "Bank": random.choice(BANKS),
    "City": random.choice(CITIES),
    "Payment_Mode": random.choice(PAYMENT_MODES)
}

print(transaction)

#Now I will create a function to generate multiple transactions and store them in a pandas DataFrame.

def generate_transaction(index):
    


    category = random.choice(list(CATEGORY_INFO.keys()))

    merchant = random.choice(CATEGORY_INFO[category]["merchants"])

    amount = round(
        random.uniform(*CATEGORY_INFO[category]["amount_range"]),
        2
    )

    def generate_transaction_id(index):
        return f"TXN{index:06d}"

    def generate_date():
        return fake.date_between(start_date='-1y', end_date='today')


    transaction = {
        "Transaction_ID": generate_transaction_id(index),
        "Date": str(generate_date()),
        "Category": category,
        "Merchant": merchant,
        "Amount": amount,
        "Bank": random.choice(BANKS),
        "City": random.choice(CITIES),
        "Payment_Mode": random.choice(PAYMENT_MODES)
    }

    return transaction
        
    

transactions = []
for i in range(1,5001):
    transactions.append(generate_transaction(i))

df = pd.DataFrame(transactions)
df = df.sort_values("Date")
df.to_csv(
    "data/transactions.csv",
    index=False
)


raw_df = df.drop(columns=["Category"])
raw_df.to_csv("data/Raw transactions.csv", index=False)
print(df.head())
print(df.shape)
print(raw_df.head())
print(raw_df.shape)