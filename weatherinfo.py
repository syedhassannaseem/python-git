import requests 

def api():
    api_key = "2e8c8df0183371540a1b7add16162ce9" # This is api key
    city = input("Enter your city name: ")
    search_url = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}") # This is api
    data = search_url.json() # This is used to show api data in json nformate
    if "coord" in data: 
        Weather_data = data["weather"][0]
        des = Weather_data["description"]
        temp = data["main"]["humidity"]
        speed = data["wind"]["speed"]
        deg = data["wind"]["deg"]
        country = data["sys"]["country"]
        cel = ( int(deg )- 32) * 5/9  # This is used to convert fehrenheit to celsius
        return print(f"Weather: {des} \nDegree: {cel} C° \nHumidity: {temp} \nAir_Speed: {speed} \nCountry: {country}")
    
print(api())