# Test code for reading digital IDs from the back of a rotary dairy milker.

## Hardware

I took images with my phone of the milking setup at the distance the luxonis camera would be placed.
The phone camera and the luxonis camera  are fairly wide angle and the pixels perdigit were small about 15x30. 
The plastic cover over the digits was also shony and hazy, casing both diffusion and reflections that made it hard to
read the digits. Errors in ID OCR are a fixaable issue, and one that should not be an additional source of error.

## New hardware

We will buy an additional camera dedicated to reading IDs.  We need a monochrome computer vision camera with a c/CS zoom lens
to increase the number of pixels per digit.  We selected an Allied Vision Alvium 1800 U-158m camera 
with 1,456 x 1,088 pixels, 3.45um pixel size and and a 50mm zoom lens.  This gives an effective 
imaging area of 246x184mm  at 2.5m. and about 75x150 pixels per digit.

We also selected a bandpass red light filter 633/70nm to cut out glare and make digit recognition easier.

## Software for OCR.

The recognition tas consists of several steps.  

1. identify when the full display is in frame and segment the pixels containing the display. This can be done by training 
yolo on images of the display on the milking machine
2. Make any preprocessing adjustments to enhance the contrast of the image. OpenCV can perform a number of steps.  Lesseract 5 does many of these too so opencv may not be needed.
    a. sharpening 
    b. [adaptive thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html#:~:text=Adaptive%20Thresholding,-In%20the%20previous&text=Here%2C%20the%20algorithm%20determines%20the,for%20images%20with%20varying%20illumination)
    c. find contours
3. Use a trained OCR image detection package ot extract the text. [Tesseract](https://tesseract-ocr.github.io) and [pytesseract](https://github.com/madmaze/pytesseract) are  two robust OCR tools. For the most accurate optimization Tesseract can be trained on the font used which in this case is the seven segment display. you can manually  collect images and annotate them with [jTessBoxEditor](https://vietocr.sourceforge.net/training.html). there are also some open source datasets and trained models for seven segment displays like [tesdata_ssd](https://github.com/Shreeshrii/tessdata_ssd) . But... google research says this should not generally be neccicary. See https://github.com/tesseract-ocr/tessdoc/blob/main/ImproveQuality.md
4. Setting `tesseract_write_images = True`  then you can see the image processing done by tesseract and see if it  make sense or needs to be preprocessed
4. Finally we need a control script that asynchronously acquires images and runs yolo then tesseract to identify the id then passes the ID to th control program


TL/DR: think if we get high-quality images running this command will be good enough: 

```
pytesseract.image_to_string(Image.open('image.png'))
```