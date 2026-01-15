'''crop_training_images.py a script to use NVIDIA GPUs and the DocTR resnet-50 detection model to identify digits
  then filter the boxes by their expected size and save small images for recogntion model training 
'''

import argparse
import cv2
import os
import glob
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import torch
import math

# Filtering Constants
TARGET_MIN_H, TARGET_MAX_H = 110, 180
TARGET_MIN_W, TARGET_MAX_W = 310, 450
PIXEL_MARGIN = 20 
FIXED_HEIGHT = 32
BATCH_SIZE = 128

def main():
    parser = argparse.ArgumentParser(description="Batch Crop based on DocTR OCR Lines.")
    parser.add_argument("--det_model", type=str, default="db_resnet50")
    parser.add_argument("--rec_model", type=str, default="crnn_mobilenet_v3_large")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    model = ocr_predictor(det_arch=args.det_model, reco_arch=args.rec_model, 
                          pretrained=True, assume_straight_pages=True).cuda().half()

    image_paths = sorted(glob.glob(os.path.join(args.input, '*.[jJ][pP][gG]')))
    total_files = len(image_paths)
    total_batches = math.ceil(total_files / BATCH_SIZE)

    # Process in chunks
    for b_idx, i in enumerate(range(0, total_files, BATCH_SIZE), 1):
        batch_paths = image_paths[i : i + BATCH_SIZE]
        
        try:
            docs = DocumentFile.from_images(batch_paths)
            batch_results = model(docs)
        except Exception as e:
            print(f"Error in Batch {b_idx}/{total_batches}: {e}")
            continue

        images_with_hits = 0
        
        for img_path, doc_result in zip(batch_paths, batch_results.pages):
            canvas = cv2.imread(img_path)
            if canvas is None: continue
            h, w = canvas.shape[:2]
            
            found_in_this_image = 0
            for block in doc_result.blocks:
                for line in block.lines:
                    (xmin, ymin), (xmax, ymax) = line.geometry
                    abs_xmin, abs_xmax = int(xmin * w), int(xmax * w)
                    abs_ymin, abs_ymax = int(ymin * h), int(ymax * h)
                    
                    pixel_w, pixel_h = abs_xmax - abs_xmin, abs_ymax - abs_ymin
                    
                    if (TARGET_MIN_W <= pixel_w <= TARGET_MAX_W) and \
                       (TARGET_MIN_H <= pixel_h <= TARGET_MAX_H):
                        
                        c_xmin, c_ymin = max(0, abs_xmin - PIXEL_MARGIN), max(0, abs_ymin - PIXEL_MARGIN)
                        c_xmax, c_ymax = min(w, abs_xmax + PIXEL_MARGIN), min(h, abs_ymax + PIXEL_MARGIN)
                        
                        crop = canvas[c_ymin:c_ymax, c_xmin:c_xmax]
                        if crop.size > 0:
                            ch, cw = crop.shape[:2]
                            resized = cv2.resize(crop, (int(cw * (FIXED_HEIGHT / ch)), FIXED_HEIGHT), interpolation=cv2.INTER_AREA)
                            
                            base_name = os.path.splitext(os.path.basename(img_path))[0]
                            cv2.imwrite(os.path.join(args.output, f"{base_name}_l{found_in_this_image}.jpg"), resized)
                            found_in_this_image += 1

            if found_in_this_image > 0:
                images_with_hits += 1

        # Calculate percentage for this batch
        hit_rate = (images_with_hits / len(batch_paths)) * 100
        print(f"Batch {b_idx}/{total_batches} | Success Rate: {hit_rate:.1f}% ({images_with_hits}/{len(batch_paths)} files)")

if __name__ == "__main__":
    main()