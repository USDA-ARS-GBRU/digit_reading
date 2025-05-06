# Test code for reading digital IDs from the back of a rotary dairy milker.

## Hardware

I took images with my phone of the milking setup at the distance the cameras would be placed.
The phone camera and the Luxonis camera are fairly wide angle and the pixels per digit were small, about 15x30. 
The plastic cover over the digits was also shiny and hazy, casing both diffusion and reflections that made it hard to
read the digits. Errors in ID OCR are a fixable issue, and one that should not be an additional source of error.

## New Camera and Lens

We needed a monochrome computer vision camera with a Zoom lens dedicated to reading IDs.  We need a monochrome computer vision camera with a C-mount zoom lens to increase the number of pixels per digit.  We selected an Allied Vision Alvium 1800 U-158m camera 
with 1,456 x 1,088 pixels, 3.45um pixel size and and a 50mm zoom lens.  This gives an effective 
imaging area of 246x184mm  at 2.5m. and about 75x150 pixels per digit.

# New filters
To maximize contrast even in sunlight we need a color bandpass filters and polarizer. The lens needs M22.5 x 0.50 filters

1. [A bandpass light red filter 633/70nm #89-813, $180](https://www.edmundoptics.com/p/light-red-m225-x-050-machine-vision-filter/32251/)
2. [A bandpass dark red filter 660/66nm #89-823, $180](https://www.edmundoptics.com/p/dark-red-m225-x-050-machine-vision-filter/32261/)
2. [A polarizing light filter, #21-545, $75.00](https://www.edmundoptics.com/f/mounted-machine-vision-glass-linear-polarizers/39895/)

Testing indoors and outdoors indicates that both filters are important. The Light red filter tested reduced background
images. In direct sunlight, a polarizer was essential to read the display. The filters made it possible t read displays that could not be read by eye alone.    


## Software for OCR.
 

There are several popular OCR models available. Tesseract was a popular model for OCR on paper. It is older and does not perform well on images. EasyOCR seems promising. Online tools like Google computer vision API and LLMs can be used but are slower and more expensive and require a lot of bandwidth.

Seven segment text is an odd font and the ghosting of off segments can cause problems. We should train a custom OCR model for our camera/ display combination. See `seven_segment_training/README.md` for the details on  data collection and training.