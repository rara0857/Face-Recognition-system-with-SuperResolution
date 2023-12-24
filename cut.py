import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import sys
import numpy as np
import cv2
from mtcnn import MTCNN

detector = MTCNN()
def detect_face (img):
    # img =  height * weight * 3  (RGB)
    shapes = np.array(img).shape

    # face_arr

    face_arr = []

    # 得到高度和寬度 做異常處理
    height = shapes[0]
    weight = shapes[1]

    #檢測人臉
    detect_result = detector.detect_faces(img)

    #如果檢測不到人臉、 返回空

    if len(detect_result )== 0:
        return []
    else :
        for item in detect_result:


            box = item['box']

            #因為預測是 給出左上角的點座標【0，1】  以及 長寬【2，3】  所以需要轉換
            top = box[1]
            buttom = box[1] + box[3]
            left = box[0]
            right = box[0] + box[2]
            #因為左上角的點可能會在圖片範圍外 所以要異常處理
            if top < 0:
                top = 0
            if left < 0:
                left = 0
            if buttom > height:
                buttom = height
            if right > weight:
                right = weight

            face_arr.append(img[top: buttom, left: right])

    return face_arr

file_path=sys.argv[1]
print(file_path)
img = cv2.imread(file_path)
face_arr = detect_face(img)
foldername= "./dataset/input/"
if not len(face_arr) == 0:
    count = 0
    for item in face_arr:
        count = count + 1
        cv2.imwrite(foldername + str(count) + '.png', item ) 
else:
    print("No face is detected")
