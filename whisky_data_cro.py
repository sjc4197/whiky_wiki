import csv
import requests
from bs4 import BeautifulSoup
di = "https://distiller.com"
cnt = 0

# CSV 파일 생성 및 헤더 추가
with open("whiskey_info.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name","kind_of_whisky" ,"Country", "Region" , "age", "abv", "Cask type", "Style", "Taste Note"])

    # 페이지 수 조절
    page_count = 2

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

            # 해설, 숙성년수, 정보 추출
            basic_data = soup_whiskey.find("div", class_="secondary-details").text.strip()
            split_data = basic_data.split("\n")
            split_data2 = split_data[2].split("//")

            try:
                name = split_data2[0].replace(" " , "") #이름
            except:
                name = "None"
                
            try:
                kind_of_whisky = split_data[0].replace(" " , "") #위스키 종류
            except:
                kind_of_whisky = "None"
                
            try:
                country = split_data2[1].replace(" " , "").split(",")[1] #만들어진 나라
            except:
                country = "None"
                
            try:
                region = split_data2[1].replace(" " , "").split(",")[0] #만들어진 지역
            except:
                region = "None"
                
            try:
                age = soup_whiskey.find("li", class_="age").text.strip().split("\n")[1] #숙성연수
            except:
                age = "None"
                
            try:
                abv = soup_whiskey.find("li", class_="abv").text.strip().split("\n")[1] #알코올 도수
            except:
                abv = "None"
                
            try:
                cask = soup_whiskey.find("li", class_="cask-type").text.strip().split("\n")[1] #캐스크 타입
            except:
                cask = "None"
                
            try:
                style = soup_whiskey.find("li", class_="whiskey-style").text.strip().split("\n")[1] #위스키 스타일
            except:
                style = "None"
                
            try:
                taste = soup_whiskey.find('blockquote').text.strip() #위스키 테이스팅 노트
            except:
                taste = "None"
            cnt = cnt+1
            print(cnt)

            # 결과 CSV 파일에 저장
            writer.writerow([name, kind_of_whisky, country, region, age, abv, cask, style, taste])
