import csv
import requests
from bs4 import BeautifulSoup
from ast import literal_eval
di = "https://distiller.com"
cnt = 0

# CSV 파일 생성 및 헤더 추가
with open("whiskey_taste_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Smoky" ,"Peaty", "Spicy" , "Herbal", "Oily", "Full_bodied", "Rich", "Sweet", "Briny", "Salty", "Vanilla", "Tart", "Fruity", "Floral"])

    # 페이지 수 조절
    page_count = 1

    for page in range(1, page_count + 1):
        # 페이지 URL 생성
        url = f"https://distiller.com/search?page="+str(page)+"&sort=total_num_of_ratings"

        # 요청 보내기
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # 각 위스키 페이지에 접근하여 정보 크롤링
        for whiskey in soup.select(".whiskey-content"):
            # 위스키 페이지 URL 추출
            whiskey_url = whiskey.find("a")["href"]
            true_url = di+whiskey_url

            # 위스키 페이지에 접근하여 정보 크롤링
            response_whiskey = requests.get(true_url)
            soup_whiskey = BeautifulSoup(response_whiskey.text, "html.parser")

            split_data = soup_whiskey.find("div", class_="secondary-details").text.strip().split("\n")
            split_data2 = split_data[2].split("//")

            try:
                name = split_data2[0].replace(" " , "") #이름
            except:
                name = "None"

            try:
                canvas = soup_whiskey.find('canvas', class_='js-flavor-profile-chart')
                data_flavors = canvas['data-flavors']
                dict_flavors = literal_eval(data_flavors)  # 문자열을 딕셔너리 형식으로 변환
                numbers_list = list(dict_flavors.values()) # 값들의 리스트를 얻음

            except:
                numbers_list = ["None" ,"None" ,"None" ,"None" ,"None" ,"None" ,"None" ,"None" ,"None" ,"None" ,"None" ,"None" ,"None" ,"None"]
            cnt = cnt+1
            print(cnt)

            # 결과 CSV 파일에 저장
            writer.writerow([name] + numbers_list)
