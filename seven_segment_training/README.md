# Creating a real seven segment training dataset for easyOCR model training

Most OCR models work pretty poorly for seven segment displays EAsyOCR is a 
good open model for detecting text in images, but it's accuracy on a 
seven segment benchmark was only [30%](https://blog.roboflow.com/best-ocr-models-text-recognition/)
Easy OCR can be [retrained](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md)

## Image Acquisition setup

The best EasyOCR training should come from training on images from our actual imaging setup. To simulate reading the red displays at the dairy we have purchased a 7 segment LED display that we can control. Using a Raspberry Pi that can control both our camera and the serial display we can gather a large number of images in sunlight and shade that  closely mimic the actual conditions in the dairy.

### Hardware

1. Raspberry Pi 4 Model B mounded in a [Smarti Touch 2](https://smarticase.com/products/smartipi-touch-2) with a 7" display
2. Allied Vision Alvium 1800 U-158m camera
3. [A bandpass light red filter 633/70nm #89-813, $180](https://www.edmundoptics.com/p/light-red-m225-x-050-machine-vision-filter/32251/)
4. [A polarizing light filter, #21-545, $75.00](https://www.edmundoptics.com/f/mounted-machine-vision-glass-linear-polarizers/39895/)
5. [WWZMDiB 4 Digit 7 Segment Digital Tube LED Display Board for Arduino](https://www.amazon.com/WWZMDiB-Module，LED-Brightness-Adjustable-Accessories/dp/B0BFQNFX6D)

Both filters were actually the wrong size but just taped to the lens. Hopefully the real lenses will work better.

We taped the lens to one end of a lab cart and the Raspberry Pi to the other end with the seven segment display attached to it at a distance of about 90 cm.  The display height was about 1/3 the height of the dairy display which will be about 3 m away so it was a similar image. We set this up at the edge of the garage at CMAVE to acquire images in sunlight and shade. 


## Code to automatically create a training dataset

While generalized training is hard, we should be able to train a performant model using our camera and a red LED seven segment display. I wrote two python scripts to aid in collecting training data:

1. `rpy_and_digits.py`. This script simply displays random digits of random brightness for focusing and calibration of the camera 
with the [Allied Vision Vimba X Viewer software](https://www.alliedvision.com/en/products/software/vimba-x-sdk/).  The viewer has display issues on Raspberry Pi but works on the Mac laptop.

2. `rpy_digits_and_photos.py`. A python script that generates random numbers, and random display intensity, displays them on the LCD and captures images, writing the file as a .jpg and adding a line to the CSV with the filename and label.

```{bash}
usage: rpy_digits_and_photos.py [-h] [--image_dir IMAGE_DIR] [--csv_file CSV_FILE] [--n_images N_IMAGES]

Capture images of TM1637 display showing random digits

options:
  -h, --help            show this help message and exit
  --image_dir IMAGE_DIR
                        Directory to save captured images
  --csv_file CSV_FILE   CSV file to log captured images and digits
  --n_images N_IMAGES   Number of images to capture
```

Using this setup we collected 2194 images in `training_data/test_img` and a CSV with file names and labels in `training_data/test.csv`.

The `test_img` directory is 261 MB so it is not in this repo but authorized users can access it [here](https://usdagcc-my.sharepoint.com/:f:/r/personal/adam_rivers_usda_gov/Documents/seven_segment_training?csf=1&web=1&e=ZpTF89) 

The next steps are to use this dataset to train a custom model with code from this repository:  https://github.com/clovaai/deep-text-recognition-benchmark and compare it to the baseline EasyOCR english model.



