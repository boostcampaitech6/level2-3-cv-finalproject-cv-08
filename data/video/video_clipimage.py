import cv2

face_cascade = cv2.CascadeClassifier('code/file/haarcascade_frontalface_default.xml')

# 이미지 읽기
img = cv2.imread('code/file/image.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 얼굴 감지
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# 각 얼굴에 대해 반복
for (x, y, w, h) in faces:
    # 얼굴 영역에 사각형 그리기
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # 얼굴 영역을 256x256 크기로 조정
    face_crop = cv2.resize(img[y:y+h, x:x+w], (256, 256))
    
    # 얼굴 이미지 저장
    cv2.imwrite('code/file/face_detected_256x256.png', face_crop)

# 이미지 보여주기
cv2.imshow('Image view', img)

# 'q' 키를 누를 때까지 대기
while cv2.waitKey(0) & 0xFF != ord('q'):
    pass

cv2.destroyAllWindows()

