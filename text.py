from datetime import datetime

def calucate_totat_price(date_from_str, date_to_str, price_per_night):
    date_from = datetime.strptime(date_from_str, "%d.%m.%Y")
    date_to = datetime.strptime(date_to_str, "%d.%m.%Y")
    
    num_nights = (date_to - date_from).days
    
    total_price = num_nights * price_per_night
    
    return total_price

date_from = "01.08.2024"
date_to = "03.08.2024"
price_per_night = 100

total_price = calucate_totat_price(date_from, date_to, price_per_night)
print(f"Total Price is {total_price}")