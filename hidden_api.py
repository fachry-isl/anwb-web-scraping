import requests
import csv

url = "https://api.anwb.nl/v2/privatelease"

# Specify the CSV file path
csv_file_path = "anwb_api.csv"

payload = "q=*&start=0&rows=2275"
headers = {
    "cookie": "ak_bmsc=FC86E9FDCB646CB1B79C48F7163C45D6~000000000000000000000000000000~YAAQRYfIFzC0nyyNAQAA1%2FXGMRZOIsQOUOHF%2Fk6bPMT85cInREzBzglS8CyU1GHvREOs24GTcChSlHDLlj8H51y%2BbsCQyAMBbijtHVL8T41soeUTwBDNAJlNewBl%2F%2Bn76WQNTJL5T5PEjeIy3%2BytFPSqXS%2Fy8j0pExU0%2FaJawshUBRCJQyft0vVMyOx6rjthV9koNzZ6pQnsGbWpPhC87myrKG5TaqxpmdelFpoYgoDMZkwuTmHktwIuR0kcbXvLKv6yoylUAlq2sBYPgpo7V4CbjKIUZ8kd%2FdRL%2FBoKWh%2BQUB0v91k8VVJ9FOITqcJ4qczB0Hof4oGKwVpoJHCC05aCMKjlh%2BO5RR2Z71oYvxyX8j3fCLSHEB%2FIBWbMxAsDL4%2BVKRrLu0cRcVEQ1hGRHYDkt3BSjvA%2BOffOM8bO2gdWt4weR0EkPgjSe%2BFEO93W; bm_sv=1C92E57AE559A7EF94A6B80B6173E580~YAAQRYfIF960nyyNAQAADjPKMRa7QYLidHv0uNy3gi8VoR8LMimlu5nU6jNqS%2F1ao9SvS5stNM4j6ilmRXg8a1GHtWCqWmkM6GGUJpVjQHe3dOPDXL9Rl6SpbFSi6vXujRhMsb0SeFY%2B%2FBcXTq0w7ohStIcuc0%2Bf6Ej0VdVQBdaUYJaEwUOWHfvs3c6cNsI6GJZXNoBxpHnTeeA6vgue5TIQX5sww3RlON6d0RXE%2FdsLfDwtsLbA5AP8N9ia~1",
    "authority": "api.anwb.nl",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "dnt": "1",
    "origin": "https://www.anwb.nl",
    "referer": "https://www.anwb.nl/",
    "sec-ch-ua": "^\^Not_A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "x-anwb-client-id": "86AhuFzAtaqLVRGLpfk7SGboVcLzCsnQ"
}

response = requests.request("POST", url, data=payload, headers=headers)

# Parse the response JSON
data = response.json()

# Open the CSV file in write mode
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow(["Manufacturer", "Model", "Price", "Fuel Type", "Vehicle Chassis"])

    # Iterate through items in the response and write rows to the CSV file
    for item in data.get("items", []):
        
        # Get product_group
        product_group = item.get("productGroup")
        manufacturer = product_group.split('_')[0]
        
        # Get model
        model = item.get("model")

        # Get price
        price = item.get("price")
        
        # Get fuel type
        fuel_type = item.get("fuelType")
        
        # Get chassis
        vehicle_chassis = item.get("vehicleChassis")
        
        # Write a row to the CSV file
        csv_writer.writerow([manufacturer, model, price, fuel_type, vehicle_chassis])