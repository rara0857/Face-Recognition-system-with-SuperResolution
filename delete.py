# -*- coding: UTF-8 -*-
import os
import glob
import shutil

paths_to_clear = [
    "dataset/input/*",
    "dataset/low_img/*",
    "downloads/merged_images/*",
    "downloads/failed_img/*",
    "experiments/self_sr_32_128/results/*"
]

for path in paths_to_clear:
    for file in glob.glob(path):
        os.remove(file)
        print(f"Deleted {file}")

attendance_file = "attendance.txt"
if os.path.isfile(attendance_file):
    os.remove(attendance_file)
    print(f"Deleted {attendance_file}")

hq_dir = 'dataset/self_HQ_V_32_128/'
if os.path.isdir(hq_dir):
    shutil.rmtree(hq_dir)
    print(f"Deleted {hq_dir}")

experiment_dir = 'experiments/'
for folder in next(os.walk(experiment_dir))[1]:
    if "3090" in folder:
        shutil.rmtree(os.path.join(experiment_dir, folder))
        print(f"Deleted {os.path.join(experiment_dir, folder)}")
