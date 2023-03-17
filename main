import requests
from bs4 import BeautifulSoup

for i in range(1,3):
    url = "https://distiller.com/search?page="+str(i)+"&sort=total_num_of_ratings"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"lxml")

    images = soup.find_all("div",attrs={"class":"image"})

    for idx, image in enumerate(images):
    #print(image["style"])
        image_url = image['style'].split('url(')[1].split(')')[0]
        if image_url.startswith("//"):
            image_url = "https:"  + image_url

        print(image_url)
        image_res = requests.get(image_url)
        image_res.raise_for_status()

        with open("whiskey{}.jpg".format((i-1)*10+idx+1),"wb") as f:
            f.write(image_res.content)
