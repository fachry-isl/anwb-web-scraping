# List of manufactures
manufacturers = [
    "Alfa Romeo", "Audi", "BMW", "BYD", "Citroen", "Cupra", "DS", "Dacia",
    "Fiat", "Ford", "Hyundai", "Jeep", "Kia", "Land Rover", "Lexus",
    "Lynk & Co", "MG", "Mazda", "Mercedes-Benz", "Mitsubishi", "Nissan",
    "Opel", "Peugeot", "Polestar", "Renault", "Seat", "Skoda", "Subaru",
    "Suzuki", "Tesla", "Toyota", "VinFast", "Volkswagen", "Volvo",
    "Xpeng", "Zeekr"
]
# List of fuel types
fuel_types = ["MHEV", "Elektrisch", "Hybrid", "PHEV"]

async def get_fuel_type_bycarname(item):
    carname = item['carname']
    if "MHEV" in carname:
        return "Benzine"
    elif "Elektrisch" in carname:
        return "Elektriciteit"
    elif "Hybrid" in carname:
        return "Hybrid benzine"
    elif "PHEV" in carname:
        return "PHEV benzine"
    else:
        return item['fuel_type']
    
async def parse_car_manufacture(item):
    carname = item['carname']

    for manufacturer in manufacturers:
        if manufacturer in carname:
            return manufacturer

async def parse_car_model(item):
    carname = item['carname']
    
    for manufacturer in manufacturers:
        carname = carname.replace(manufacturer, "")
    
    for fuel_type in fuel_types:
        carname = carname.replace(fuel_type, "")
    
    # Remove unicode
    carname = carname.replace("\u00e9", "e")
    
    
    return carname.strip()

async def parse_fuel_type(item):
    fuel_type = item['fuel_type']
    
    # Remove Brandstof: 
    fuel_type = fuel_type.replace("Brandstof: ", "")
    
    # Elektriciteit / benzine == 
    
    return fuel_type.strip()

async def parse_chassis(item):
    chassis = item['chassis'].lower()
    
    if "cabrio" in chassis:
        return "Cabriolet"
    elif "hatchback" in chassis:
        return "Hatchback"
    elif "mpv" in chassis:
        return "MPV"
    elif "suv" in chassis:
        return "SUV"
    elif "sedan" in chassis:
        return "Sedan"
    elif "stationwagen" in chassis:
        return "Stationwagen"
    elif "stationwagon" in chassis:
        return "Stationwagen"
    elif "sportback" in chassis:
        return "Sportback"
    

async def parse_price(item):
    # Remove unicode
    return item['price'].replace('\u20ac\u00a0', '')
    
    
    
