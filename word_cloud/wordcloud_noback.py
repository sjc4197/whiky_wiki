from wordcloud import WordCloud
from nltk.corpus import stopwords
import re
from PIL import Image
import numpy as np
import csv
from PIL import ImageOps
cnt = 1

# 불필요한 공백이나 캐리지리턴 문자 제거하는 함수
def strip_cr(words):
    output = []
    for word in words:
        output.append(word.strip())
    return output

# 전처리 및 토큰화 작업
def preprocessing(text):
    output1 = []
    for line in text:
        # 공백라인 건너뛰기
        if line == '':
            continue

        # 소문자로 통일
        line = line.lower()

        # 알파벳과 공백을 제외한 모든 기호는 제거
        p = re.compile('[^a-z ]+')
        line = p.sub('', line)
        # 문장 속 단어를 토큰으로 분리
        words = line.split()
        output1 += words
    #불용어 제거
    output2 = []
    for word in output1:
        if word not in stopwords.words('english'):
            output2.append(word)
    return output2


# 토큰 리스트로부터 도수분포 딕셔너리 만들기
def make_token_freq_dict(token_list):
    output_dict = {}
    for token in token_list:
        if token in output_dict.keys():
            output_dict[token] += 1
        else:
            output_dict[token] = 1
    return output_dict

#맛 데이터 불러오기
def taste_words():
    with open('/Users/seojuncheol/Desktop/Whiky_Wiki/word_cloud/taste.txt', 'r') as f:
        document_n = f.readlines()
        document_n = strip_cr(document_n)
    return document_n

#이미지 마스크 불러오기
img = Image.open('/Users/seojuncheol/Desktop/Whiky_Wiki/word_cloud/whisky_bottle.png')
img_array = np.array(img)

#맛 데이터 불러오기
taste_words = taste_words()

from PIL import ImageOps

# 워드클라우드 생성 후 저장
with open('/Users/seojuncheol/Desktop/Whiky_Wiki/data/whiskey_top1100_info.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader) # 헤더 제거
    for row in reader:
        name = row[0] # 이름
        tasting_note = row[12] # 맛 정보

        # 텍스트 전처리
        tokens = preprocessing([tasting_note])
        word_count = make_token_freq_dict(tokens)
        print(word_count)

        # 워드클라우드 생성
        wc = WordCloud(font_path='/Users/seojuncheol/Desktop/Whiky_Wiki/word_cloud/font/SourceSansPro-Semibold.otf', background_color='rgba(0, 0, 0, 0)', width=400, height=400, scale=2.0, max_font_size=250, mask=img_array)
        gen = wc.generate_from_frequencies(word_count)
        
        # 이미지 객체 생성
        image = gen.to_image()

        # 배경을 투명하게 만듦
        image = image.convert("RGBA")
        data = image.getdata()
        new_data = []
        for item in data:
            # 검정색(0, 0, 0)인 픽셀의 알파값을 0으로 설정하여 투명하게 만듦
            if item[:3] == (0, 0, 0):
                new_data.append((0, 0, 0, 0))
            else:
                new_data.append(item)
        image.putdata(new_data)

        # PNG 형식으로 저장
        image.save(str(cnt)+"."+name + '.png', "PNG")
        cnt += 1
