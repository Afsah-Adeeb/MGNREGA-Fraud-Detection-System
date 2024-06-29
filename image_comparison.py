import cv2
import numpy as np

def compare_images(image1, image2):
    # Convert the images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Define a template size (region of interest)
    template_width, template_height = 100, 100  # Adjust the size as needed

    # Resize both images to the same dimensions
    resized_image1 = cv2.resize(gray_image1, (template_width, template_height))
    resized_image2 = cv2.resize(gray_image2, (template_width, template_height))

    # Calculate the mean squared error between the resized images
    mse = np.mean((resized_image1 - resized_image2) ** 2)

    # Calculate a dynamic threshold based on the image size
    image_size = gray_image1.shape 
    dynamic_threshold = np.prod(image_size) / 1000 

    # Initialize the SIFT detector
    sift = cv2.SIFT_create()

    # Find the keypoints and descriptors with SIFT
    keypoints1, descriptors1 = sift.detectAndCompute(gray_image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray_image2, None)

    # Create a Brute-Force Matcher
    bf = cv2.BFMatcher()

    # Match descriptors
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Apply ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # If the images are pixel-wise identical or have enough good matches, consider them similar
    if mse < 1 or len(good_matches) > 45:
        return True
    else:
        return False
