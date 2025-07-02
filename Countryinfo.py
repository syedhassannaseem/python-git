import requests

def countryinfo():
    try:
        country_name = input("Enter the country name: ")
        url= f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url)
        data = response.json()
        if (data, list) and data:
            Name = data[0]["name"]["common"]
            Capital = data[0]["capital"][0]
            region = data[0]["region"]
            Subregion = data[0]["subregion"]
            pop = data[0]["population"]
            Timezone = data[0]["timezones"][0]
            flag = data[0]["flags"]["png"]
            lan =",".join(data[0]["languages"].values())
            return (f"Country Name: {Name}\nCapital: {Capital}\nRegion: {region}\nSubregion: {Subregion}\nPopulation: {pop}\nTimezone: {Timezone}\nFlag: {flag}\nLanguages: {lan}")
    except Exception as e:
        print(f"\n\nEnter the country name only {e}")

print(countryinfo())