import os
from PIL import Image

# 이미지 폴더 경로
dir_path = '/Users/seojuncheol/Desktop/Whiky_Wiki/선별 위스키 목록/test_img'

# 새로운 폴더 생성
new_dir_path = os.path.join(dir_path, 'resized_images')
os.makedirs(new_dir_path, exist_ok=True)

# 폴더 내 이미지 파일들을 순서대로 불러와서 리사이즈 후 저장
for filename in sorted(os.listdir(dir_path)):
    if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
        # 이미지를 불러와서 img 변수에 할당
        img = Image.open(os.path.join(dir_path, filename))
        
        # 이미지 사이즈 변경
        img_resized = img.resize((224,224))
        
        # 변경한 이미지 저장
        new_filename = f'{os.path.splitext(filename)[0]}_resized{os.path.splitext(filename)[1]}'
        img_resized.save(os.path.join(new_dir_path, new_filename))
