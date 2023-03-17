import requests
from bs4 import BeautifulSoup

for i in range(1, 5):
    url = "https://distiller.com/search?page="+str(i)+"&sort=total_num_of_ratings"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"lxml")

    images = soup.find_all("div", attrs={"class": "image"})
    names = soup.find_all("div", attrs={"class": "name"})
    for idx, image in enumerate(images):
        image_url = image['style'].split('url(')[1].split(')')[0]
        if image_url.startswith("//"):
            image_url = "https:"  + image_url

        name = names[idx].text.strip()  # 현재 이미지에 해당하는 이름 정보 추출
        filename = "{}.jpg".format(name.replace("/", "-"))  # 파일 이름 생성 (슬래시는 대시로 변경)

        image_res = requests.get(image_url)
        image_res.raise_for_status()

        with open(filename, "wb") as f:
            f.write(image_res.content)
