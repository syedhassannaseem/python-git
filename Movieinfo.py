import requests
try:
    movie_title = input("Enter The Movie Name: ")
    url = f"http://www.omdbapi.com/?apikey=301f0598&t={movie_title}"
    response = requests.get(url).json()
    print(f"Movie Title: {response["Title"]}")
    print(f"Type: {response["Type"]}")
    print(f"Year: {response["Year"]}")
    print(f"RunTime: {response["Runtime"]}")
    print(f"Rating: {response["imdbRating"]}")
    print(f"Released: {response["Released"]}")
    print(f"Writer: {response["Writer"]}")
    print(f"Country: {response["Country"]}")
    print(f"Poster: {response["Poster"]}")
    if response["Type"] == "series":
      print(f"Total seasons: {response["totalSeasons"]}")
except Exception as e:
    print(f"\n⚠️ An error occurred: {str(e)}")