#!/usr/bin/env python3
"""
Allied Vision Camera and TM1637 Display Script
Controls a TM1637 4-digit display and captures images with Allied Vision camera

Usage:
    ./rpy_digits_and_photos --image_dir DIRECTORY --csv_file FILENAME --n_images NUMBER
"""

import cv2
import vmbpy
import random
import time
import os
import csv
import argparse
from datetime import datetime
from tm1637 import TM1637
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

# Configuration
TM1637_CLK_PIN = 23  # GPIO pin for TM1637 CLK
TM1637_DIO_PIN = 24  # GPIO pin for TM1637 DIO

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Capture images of TM1637 display showing random digits')
    parser.add_argument('--image_dir', type=str, default='captured_images',
                        help='Directory to save captured images')
    parser.add_argument('--csv_file', type=str, default='display_captures.csv',
                        help='CSV file to log captured images and digits')
    parser.add_argument('--n_images', type=int, default=10,
                        help='Number of images to capture')
    return parser.parse_args()

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def init_csv(csv_filename):
    """Initialize the CSV file with headers if it doesn't exist."""
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["filename", "digits"])

def log_to_csv(csv_filename, filename, digits):
    """Log information to the CSV file."""
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([filename, digits])

def generate_random_digits():
    """Generate a random 4-digit number with leading zeros."""
    return f"{random.randint(0, 9999):04d}"

def select_random_brightness():
    """Select a random brightness level between 1-7."""
    return random.randint(1, 7)

def capture_image(camera, digits, brightness, image_dir):
    """Capture an image using Allied Vision camera and save with unique filename."""
    # Create a unique filename based on timestamp, digits, and brightness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_digits{digits}_brightness{brightness}.jpg"
    filepath = os.path.join(image_dir, filename)
    
    # Capture a frame
    frame = camera.get_frame()
    frame.convert_pixel_format(vmbpy.PixelFormat.Mono8)
    
    # Save the image
    cv2.imwrite(filepath, frame.as_opencv_image())
    print(f"Image saved to {filepath}")
    
    return filename

def check_for_break_key():
    """Check if the break key (ESC) is pressed."""
    if KEYBOARD_AVAILABLE:
        try:
            if keyboard.is_pressed('esc'):
                print("\nProcess terminated by user (ESC key)")
                return True
        except:
            pass
    return False

def main():
    """Main function to control display, capture images and log data."""
    # Parse command line arguments
    args = parse_arguments()
    image_dir = args.image_dir
    csv_filename = args.csv_file
    n_images = args.n_images
    
    # Ensure the image directory exists
    ensure_directory_exists(image_dir)
    
    # Initialize the CSV file
    init_csv(csv_filename)
    
    print(f"Will capture {n_images} images, saving to {image_dir} and logging to {csv_filename}")
    if KEYBOARD_AVAILABLE:
        print("Press ESC at any time to terminate the process")
    else:
        print("Press Ctrl+C to abort the process")
    
    try:
        # Set up the TM1637 display once
        print("Connecting to TM1637 display...")
        tm = TM1637(clk=TM1637_CLK_PIN, dio=TM1637_DIO_PIN)
        
        # Initialize camera connection once
        print("Connecting to Allied Vision camera...")
        with vmbpy.VmbSystem.get_instance() as vmb: 
            cams = vmb.get_all_cameras()
            if not cams:
                print("No cameras found!")
                return
            print(f"Found {len(cams)} camera(s)")
            with cams[0] as camera:
                # Capture multiple images]
                for i in range(n_images):
                    if check_for_break_key():
                        break
                        
                    print(f"\nCapturing image {i+1} of {n_images}")
                    
                    # Generate random digits and brightness
                    digits = generate_random_digits()
                    brightness = select_random_brightness()
                    
                    print(f"Displaying digits: {digits} at brightness: {brightness}")
                    
                    # Set display
                    tm.brightness(brightness)
                    tm.show(digits)
                    
                    # Allow display to stabilize
                    time.sleep(0.8)
                    
                    # Capture image
                    try:
                        filename = capture_image(camera, digits, brightness, image_dir)
                        
                        if filename:
                            # Log to CSV
                            log_to_csv(csv_filename, filename, digits)
                            print(f"Logged to CSV: {filename}, digits: {digits}")
                    except Exception as e:
                        print(f"Error capturing image: {e}")
            
                # Brief pause between captures
                time.sleep(0.2)
            
    except KeyboardInterrupt:
        print("\nProcess interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        print("Cleaning up resources...")
        try:
            # Clear the display
            tm.show("    ")
        except:
            pass
        print("Done.")

if __name__ == "__main__":
    main()
