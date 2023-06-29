import csv
import requests
from bs4 import BeautifulSoup
from ast import literal_eval
di = "https://distiller.com"
cnt = 0

# CSV 파일 생성 및 헤더 추가
with open("whiskey_top1000_info.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name","Rating","Rating count","kind_of_whisky" ,"Country", "Region" , "Cost level", "Flavor Proflie", "age", "abv", "Cask type", "Style", "Taste Note","Smoky" ,"Peaty", "Spicy" , "Herbal", "Oily", "Full_bodied", "Rich", "Sweet", "Briny", "Salty", "Vanilla", "Tart", "Fruity", "Floral"])

    # 페이지 수 조절
    page_count = 130

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
            split_data = soup_whiskey.find("div", class_="secondary-details").text.strip().split("\n")
            split_data2 = split_data[2].split("//")

            try:
                name = soup_whiskey.find("h1", class_="secondary-headline").text.strip() #이름
            except:
                name = "None"

            try:
                rating = soup_whiskey.find("span", itemprop="ratingValue").text.strip() #평점
            except:
                rating = "None"

            try:
                rating_count = soup_whiskey.find("span", itemprop="ratingCount").text.strip() #평점매긴 횟수
            except:
                rating_count = "None"
                
            try:
                kind_of_whisky = split_data[0].replace(" " , "") #위스키 종류
            except:
                kind_of_whisky = "None"
                
            try:
                country = split_data2[1].replace(" " , "").split(",")[1] # 만들어진 나라
            except:
                country = "None"
                
            try:
                region = split_data2[1].replace(" " , "").split(",")[0] #만들어진 지역
            except:
                region = "None"

            try:
                cost = soup_whiskey.find('div', class_='spirit-cost')['class'][1][5] #대략적인 맛
            except:
                cost = "None"

            try:
                flavor = soup_whiskey.find("h3", class_="middleweight").text.strip() #대략적인 맛
            except:
                flavor = "None"
                
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
                
            try:
                canvas = soup_whiskey.find('canvas', class_='js-flavor-profile-chart')
                data_flavors = canvas['data-flavors']
                dict_flavors = literal_eval(data_flavors)  # 문자열을 딕셔너리 형식으로 변환
                numbers_list = list(dict_flavors.values()) # 값들의 리스트를 얻음
            except:
                numbers_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            cnt = cnt+1
            print(cnt)

            # 결과 CSV 파일에 저장
            writer.writerow([name, rating, rating_count, kind_of_whisky, country, region, cost, flavor, age, abv, cask, style, taste] + numbers_list)