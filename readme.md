# Code for training OCR models and reading digital seven-segment displays from a rotary milking parlor

## Hardware

Training data ware collected with a monochrome computer vision camera with a 50mm Zoom lens dedicated to reading IDs. We selected an Allied Vision Alvium 1800 U-158m camera 
with 1,456 x 1,088 pixels, 3.45um pixel size and and a 50mm zoom lens. The camera in the dairy is an Alvium G1-158m PoE camera with a wider angle lens so it is less sensitive to the exact udder detection time. 


## New filters
To maximize contrast even in sunlight we need a color bandpass filters and polarizer. The lens needs M22.5 x 0.50 filters

1. [A bandpass light red filter 633/70nm #89-813, $180](https://www.edmundoptics.com/p/light-red-m225-x-050-machine-vision-filter/32251/)
2. [A bandpass dark red filter 660/66nm #89-823, $180](https://www.edmundoptics.com/p/dark-red-m225-x-050-machine-vision-filter/32261/)
2. [A polarizing light filter, #21-545, $75.00](https://www.edmundoptics.com/f/mounted-machine-vision-glass-linear-polarizers/39895/)

Testing indoors and outdoors indicates that both filters are important. The Light red filter tested reduced background
images. In direct sunlight, a polarizer was essential to read the display. The filters made it possible t read displays that could not be read by eye alone.    


## Software for OCR

We evaluated many OCR tools including Tesseract, EasyOCR, PaddleOCR, Parseq, and DocTR Online tools like Google computer vision API and LLMs can be used and work well, but are slower and more expensive and require a lot of bandwidth. Seven segment text is an odd font and the ghosting of off segments can cause problems.

## DocTR

We needed flexibility in detection and recognition models and the ability to custom train models after testing off the shelf models.  DocTR is a modular systems that allows the user to select from many different models

## Text Recognition

For text recognition we evaluated multiple models but have gone forward with `resnet-50`. The base models performs sell when OCR text is small as at the dairy. When the text is large as in our training date it did not perform as well.

## color inversion

Most OCR models perform better with dark text on light backgrounds, the opposite of what we collect. so we will reverse each image for training and analysis

## Text detection

Text detecton models did not perform well with our data by default. the are also trained on all characters not just digits which makes mistakes more likely.  We have retrained `rcnn-mobilenet-v3-large` on our data.

# Training approach

Our training approach was:

1. Collect 222,003 images in the directory `captured images2`
2. Invert the images with the the script `invert_multithread.py` for this and save them to `captured_images2_inverted`
3. Use off the shelf DocTR `resnet-50` to  identify the text region and crop them and resize them to 32 px high submiting the job to Atlas. 
3. Modify the [custom training script train.py](https://github.com/mindee/doctr/blob/main/references/recognition) to use complicated [Albumentations](https://albumentations.ai/) distortions of the data to prevent memorization.
4. Train  the `rcnn-mobilenet-v3-large` models with Albumentations distortions.
5. Visualize the results of using the `resnet-50` detection models and the custom recognition model on actual photos collected from our camera at the dairy.
6. Convert the model to onnx format with 


# Data

- `Captured_images2_inverted` 222,203 jpeg images with an avaerge size of 194kb.
- `Cropped_images2_inverted` XXX,XXX jpeg images with a height of 32 px and an average file size of  2kb.