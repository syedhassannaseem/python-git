import requests
def api():
    url = "https://api.freeapi.app/api/v1/public/books?page=1&limit=10&inc=kind%2Cid%2Cetag%2CvolumeInfo&query=tech"
    responce = requests.get(url)
    data = responce.json()
    h = []
    if data["success"] and "data" in data:
            userdata = data["data"]
            for i in range(0,10):
              user = userdata["data"][i]["volumeInfo"]["title"]
              h.append(user)
            for i in h:
                 print(i)
        

print(api())



