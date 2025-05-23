#!/usr/bin/env python3
"""

Controls a TM1637 4-digit display showing random values very second
"""


import random
import time
import os

from tm1637 import TM1637

# Configuration
TM1637_CLK_PIN = 23  # GPIO pin for TM1637 CLK
TM1637_DIO_PIN = 24  # GPIO pin for TM1637 DIO



def generate_random_digits():
    """Generate a random 4-digit number with leading zeros."""
    return f"{random.randint(0, 9999):04d}"

def select_random_brightness():
    "s""Select a random brightness level between 1-7."""
    return random.randint(1, 7)

def main():
    """Main function to control display, capture images and log data."""

    
    try:
        # 1. Open connection to the TM1637 display
        print("Connecting to TM1637 display...")
        tm = TM1637(clk=TM1637_CLK_PIN, dio=TM1637_DIO_PIN)
        
        while True:
            # 3. Generate a random 4-digit number
            digits = generate_random_digits()
            print(f"Generated random digits: {digits}")
        
            # 5. Select a random brightness level
            brightness = select_random_brightness()
            print(f"Selected brightness level: {brightness}")
        
            # 6. Display the number
            tm.brightness(brightness)
            tm.show(digits)
            print(f"Displaying digits on TM1637")
        
            # Allow time for the display to stabilize
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up by clearing the display
        try:
            tm.show("    ")
        except:
            pass

if __name__ == "__main__":
    main()
