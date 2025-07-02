import multiprocessing
import requests
def downloadFile(url,name):
    print(f"Started Downloading {name}")
    responce = requests.get(url)
    open(f"trash/file{name}.jpg","wb").write(responce.content)
    print(f"Finished Downloading {name}")

if __name__ == "__main__":
    url="https://picsum.photos/2000/3000"
    pro = []
    for i in range(1,5):
        # downloadFile(url , i)
       v = multiprocessing.Process(target=downloadFile , args=[url , i])
       v.start()
       pro.append(v)
    for v in pro:
        v.join()

