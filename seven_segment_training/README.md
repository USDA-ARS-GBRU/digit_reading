# Creating a real seven segment training dataset for easyOCR model training

Most OCR models work pretty poorly for seven segment displays EAsyOCR is a 
good open model for detecting text in images, but it's accuracy on a 
seven segment benchmary was only [29%](https://blog.roboflow.com/best-ocr-models-text-recognition/)
Easy OCR can be [retrained](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md)

## code to automatically create a training dataset

While Generalized training is hard, we should be able to train a performant model using out camera and a red LED seven segment display.
I have purchases a red seven segment display that we can control generate 4 digit numbers using an Arduino and a serial connection. This involves two scripts:

1. An arduino script using the [TM1637 library](https://www.instructables.com/How-to-Use-the-TM1637-Digit-Display-With-Arduino/) (.ino file_)
2. A python script that  generates random numbers, and random display intensity, displays them on the LCD and captures an image, writing the file as a .jpg and adding a line to the CSV with the filename and label. 


## Image Acquisition setup  

We could set this up under the garage at CMAVE to acquire throughout a sunny day. 
This would capture sunlight interference throughout the day.
