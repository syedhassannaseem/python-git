import requests
def jokeapi():
    try:
        kind = input("What kind of joke do u want (Any, Programming, Misc, etc.)?: ")
        lang = input("Enter language (Germany = de,English = en,Spanish = es): ")
        url = f"https://v2.jokeapi.dev/joke/{kind}?lang={lang}"
        response = requests.get(url)
        data = response.json()
        if data["type"] == "single":
            return data["joke"]
        elif data["type"] == "twopart":
            return data["setup"]
        else:
            return "No joke found"
    except Exception as e:
        print(f"Enter valid kind or language {e}")
print(jokeapi())