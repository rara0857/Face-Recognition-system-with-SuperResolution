import os
import cv2

# Generate by Chatgpt
# 設定圖片資料夾路徑
low_img_folder = "dataset/self_HQ_V_32_128/lr_32/"
results_folder = "experiments/self_sr_32_128/results/"

# 獲取兩個資料夾中的文件名稱
low_img_files = os.listdir(low_img_folder)
results_files = os.listdir(results_folder)

# 創建一個資料夾來保存合併後的圖片
merged_folder = "downloads/merged_images/"
if not os.path.exists(merged_folder):
    os.makedirs(merged_folder)

# 遍歷所有的圖片並進行合併
for low_img_file in low_img_files:
    if low_img_file.endswith(".png"):
        # 提取圖片編號
        img_number = os.path.splitext(low_img_file)[0]
        img_number = str(int(img_number))

        # 讀取對應的圖片
        low_img = cv2.imread(os.path.join(low_img_folder, low_img_file))
        sr_img = cv2.imread(os.path.join(results_folder, img_number + "_sr.png"))

        # 調整低解析度圖像的尺寸，使其與高解析度圖像相同
        height, width = sr_img.shape[:2]
        low_img_resized = cv2.resize(low_img, (width, height), interpolation=cv2.INTER_LINEAR)

        # 將圖片合併
        merged_img = cv2.hconcat([low_img_resized, sr_img])

        # 保存合併後的圖片
        cv2.imwrite(os.path.join(merged_folder, img_number + "_merged.png"), merged_img)
