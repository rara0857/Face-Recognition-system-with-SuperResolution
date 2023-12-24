# -*- coding: UTF-8 -*-
import os
import glob,shutil

for file in glob.glob("dataset/input/*"):
  os.remove(file)
  print("Deleted "+ str(file))

for file in glob.glob("dataset/low_img/*"):
  os.remove(file)
  print("Deleted "+ str(file))

for file in glob.glob("downloads/merged_images/*"):
  os.remove(file)
  print("Deleted "+ str(file))

for file in glob.glob("downloads/failed_img/*"):
  os.remove(file)
  print("Deleted "+ str(file))

for file in glob.glob("experiments/self_sr_32_128/results/*"):
  os.remove(file)
  print("Deleted "+ str(file))

if os.path.isfile("attendance.txt"):
  os.remove("attendance.txt")
  print("Deleted attendance.txt")

path = 'dataset/self_HQ_V_32_128/'
if os.path.isdir(path):
  shutil.rmtree(path)
  print("Deleted "+ str(path))

path = 'experiments/'
for folder in next(os.walk(path))[1]:
  if folder.find("3090")!=-1:
    shutil.rmtree(path+folder)
    print("Deleted "+ str(path+folder))