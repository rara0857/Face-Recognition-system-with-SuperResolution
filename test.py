import glob
import codecs
import csv
import os
import datetime
from deepface import DeepFace
import shutil
from PIL import Image

faces_folder_path = "./Faces"
input_folder_path = "./experiments/self_sr_32_128/results"
failed_img_folder = "./downloads/failed_img"

input_images = [f for f in glob.glob(os.path.join(input_folder_path, "*.*")) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
input_images.sort()

candidate = []

models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "ArcFace", 
  "SFace",
]

folders = glob.glob(os.path.join(faces_folder_path, "*"))
folders.sort()

for folder in folders:
    if os.path.isdir(folder):
        candidate_name = os.path.basename(folder)
        candidate.append(candidate_name)

mylist = [[name, 0] for name in candidate]

def update_csv_file(filename, mylist, date, total_images):
    success_count = sum([int(item[1]) for item in mylist])
    if total_images!=0:
        success_rate = round(success_count / total_images,4)
        print('總人數:',total_images)
        print('誤點名人數:',success_count)
    else:
        success_rate=0
    if not os.path.exists(filename):
        with codecs.open(filename, 'w', 'utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['姓名', '學號', date, '總出席次數'])
            for name, count in mylist:
                name, sid = name.split('_', 1)
                writer.writerow([name, sid, count] + [count])
            writer.writerow('')
            writer.writerow(['辨識成功率', '',success_rate])
    else:
        with codecs.open(filename, 'r', 'utf-8-sig') as csvfile:
            lines = csvfile.readlines()

        success_rate_line = -1
        for i, line in enumerate(lines):
            if '辨識成功率' in line:
                success_rate_line = i
                break

        with codecs.open(filename, 'w', 'utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            for i, line in enumerate(lines):
                values = line.strip().split(',')
                if i == 0:
                    header_row = values[:-1]
                    row = header_row + [date, '總出席次數']
                elif i == success_rate_line:
                    row = values + [success_rate]
                elif i == success_rate_line-1:
                    row=''
                else:
                    if len(values) >= 3:
                        name, sid, *attendance, total_attendance = values
                        for item in mylist:
                            if item[0] == name + '_' + sid:
                                count = item[1]
                                break
                            else:
                                count = 0
                        row = values[:-1] + [count] + [str(int(total_attendance) + int(count))]
                    else:
                        continue
                writer.writerow(row)

for img_path in input_images:
    result = DeepFace.find(img_path=img_path, db_path=faces_folder_path, model_name=models[2],enforce_detection=False)
    closest_identity = result[0]['identity']
    closest_identity = os.path.basename(os.path.dirname(str(closest_identity)))

    if closest_identity != "unknown" and closest_identity != "":
        for j in range(len(mylist)):
            if mylist[j][0] == closest_identity:
                #mylist[j][1] = str(int(mylist[j][1]) + 1)
                mylist[j][1] = 1
                break
    else:
        print("not found")
        failed_img_path = os.path.join(failed_img_folder, os.path.basename(img_path))
        shutil.copy(img_path, failed_img_path)

print(mylist)

total_input_images = len(input_images)
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
update_csv_file('downloads/output.csv', mylist, current_date, total_input_images)