import cv2
import pytesseract

# Load the image
image = cv2.imread("form.png")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use Tesseract to extract text
text = pytesseract.image_to_string(gray)

# Print the extracted text
print(text)
