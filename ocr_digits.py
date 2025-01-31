# USAGE
# python ocr_digits.py --image apple_support.png
# python ocr_digits.py --image apple_support.png --digits 0

# import the necessary packages
import pytesseract
import argparse
import cv2
import numpy as np

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-d", "--digits", type=int, default=1,
	help="whether or not *digits only* OCR will be performed")
args = vars(ap.parse_args())

# load the input image, convert it from BGR to RGB channel ordering,
# and initialize our Tesseract OCR options as an empty string
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Input Image", rgb)  # Add a window name
cv2.waitKey(0)  # Wait for a key press to close the window

# Apply erosion and dilation
kernel = np.ones((11, 11), np.uint8)

# Erode the image
eroded = cv2.erode(rgb, kernel, iterations=1)
cv2.imshow("Eroded Image", eroded)
cv2.waitKey(0)

eroded_inv = cv2.bitwise_not(eroded)
cv2.imshow('inverted', eroded_inv)
cv2.waitKey(0)

# Use the processed image for OCR
options = ""

# check to see if *digit only* OCR should be performed, and if so,
# update our Tesseract OCR options
if args["digits"] > 0:
	options = "--oem 3 --psm 8 outputbase digits"

# OCR the input image using Tesseract
text = pytesseract.image_to_string(eroded, config=options)
print(text)