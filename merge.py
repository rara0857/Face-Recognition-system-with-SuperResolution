import os
import cv2

low_img_folder = "dataset/self_HQ_V_32_128/lr_32/"
results_folder = "experiments/self_sr_32_128/results/"

low_img_files = os.listdir(low_img_folder)
results_files = os.listdir(results_folder)

merged_folder = "downloads/merged_images/"
if not os.path.exists(merged_folder):
    os.makedirs(merged_folder)

for low_img_file in low_img_files:
    if low_img_file.endswith(".png"):
        img_number = os.path.splitext(low_img_file)[0]
        img_number = str(int(img_number))

        low_img = cv2.imread(os.path.join(low_img_folder, low_img_file))
        sr_img = cv2.imread(os.path.join(results_folder, img_number + "_sr.png"))

        height, width = sr_img.shape[:2]
        low_img_resized = cv2.resize(low_img, (width, height), interpolation=cv2.INTER_LINEAR)

        merged_img = cv2.hconcat([low_img_resized, sr_img])

        cv2.imwrite(os.path.join(merged_folder, img_number + "_merged.png"), merged_img)
