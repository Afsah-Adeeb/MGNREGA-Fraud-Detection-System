import cv2
import os

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def is_blurry(frame, threshold):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    return fm < threshold

def process_video(video_path):
    video_capture = cv2.VideoCapture(video_path)

    # Create an output folder to save frames
    output_folder = 'frames'
    os.makedirs(output_folder, exist_ok=True)

    frame_count = 0
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    extraction_interval = total_frames // 10  # Adjust this for the desired number of frames.

    # List to store paths of the extracted images
    image_paths = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Extract a frame and save it
        if frame_count % extraction_interval == 0:
            frame_filename = os.path.join(output_folder, f'frame_{frame_count}.jpg')
            cv2.imwrite(frame_filename, frame)
            image_paths.append(frame_filename)

        frame_count += 1

    video_capture.release()

    # Check each extracted image for blur
    blurry_count = 0
    threshold = 100  # Set your desired threshold value here

    for image_path in image_paths:
        image = cv2.imread(image_path)
        blurry = is_blurry(image, threshold)

        # Highlight the blurred images with a red border
        if blurry:
            image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[0, 0, 255])

    # Loop over the input images
    for image_path in image_paths:
        # Load the image, convert it to grayscale, and compute the
        # focus measure of the image using the Variance of Laplacian method
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)

        # If the focus measure is less than the threshold, consider the image blurry
        if fm < threshold:
            blurry_count += 1

    # Determine the validity of the video based on the number of blurry frames
    if blurry_count >= 5:
        result = f"\nThe video is NOT good. {blurry_count} frames are blurry."
    else:
        result = f"\nThe video is good. {blurry_count} frames are blurry."

    return result
