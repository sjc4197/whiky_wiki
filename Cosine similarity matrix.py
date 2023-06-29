from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import re
import numpy as np
import csv

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

#맛 데이터 불러오기
tasting_notes = []
whiskey_names = []
whisky_kind = []
with open('whiskey_info.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader) # 헤더 제거
    for row in reader:
        name = row[0] # 이름
        kind = row[1] # 위스키 종류
        tasting_note = row[10] # 맛 정보
    

        # 텍스트 전처리및 토큰화
        tokens = preprocessing([tasting_note])

        whiskey_names.append(name)
        tasting_notes.append(tokens)
        whisky_kind.append(kind)

# CountVectorizer를 사용하여 토큰화된 문장을 벡터화
vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform([' '.join(tokens) for tokens in tasting_notes])

# 코싸인 유사도 계산
similarities = cosine_similarity(vectors)

def recommend_similar_whiskies(name, n=5):
    # 주어진 위스키의 맛 데이터 가져오기
    idx = whiskey_names.index(name)

    # 코싸인 유사도 내림차순으로 정렬
    similarity_row = similarities[idx]
    similar_indices = np.argsort(-np.array(similarity_row))

    # 유사한 위스키 n개 추천
    print(f"Recommendations for {name}:")
    for i in similar_indices[1:n+1]:
        print(f"- {whiskey_names[i]} [{whisky_kind[i]}] : {round(similarity_row[i], 2)}")

whisky_name = input("whisky name : ")
recommend_similar_whiskies(whisky_name)
