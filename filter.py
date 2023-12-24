# -*- coding: UTF-8 -*-
import cv2
import glob
count1,count2=1,1
sr_path= "./dataset/low_img/"
withoutsr_path='./experiments/self_sr_32_128/results/'

for file in glob.glob("dataset/input/*"):
  img=cv2.imread(file)
  a=img.shape[0]
  b=img.shape[1]
  print("img resolution:",a,'*',b)
  if (a >= 36 and b >= 36):
    cv2.imwrite(withoutsr_path + "withoutsr_"+str(count1) + '.png', img )
    count1+=1
  else:
    cv2.imwrite(sr_path + str(count2) + '.png', img )
    count2+=1
  