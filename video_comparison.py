import cv2
import os
import shutil
from image_comparison import compare_images

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_rate = int(cap.get(5))  # Get the frame rate of the video
    count = 0

    # Remove existing content in the output folder
    shutil.rmtree(output_folder, ignore_errors=True)

    os.makedirs(output_folder, exist_ok=True)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_path = os.path.join(output_folder, f'frame_{count}.png')
        cv2.imwrite(frame_path, frame)

        count += 1

        # Skip frames to match the frame rate
        for _ in range(frame_rate - 1):
            cap.read()

    cap.release()

def save_similar_frame_pair(pair_count, frame1_path, frame2_path, output_folder):
    pair_folder = os.path.join(output_folder, f'pair{pair_count}')
    os.makedirs(pair_folder, exist_ok=True)

    frame1_name = os.path.basename(frame1_path)
    frame2_name = os.path.basename(frame2_path)

    frame1_first_path = os.path.join(pair_folder, f'{os.path.splitext(frame1_name)[0]}_first.png')
    frame2_sec_path = os.path.join(pair_folder, f'{os.path.splitext(frame2_name)[0]}_sec.png')

    frame1 = cv2.imread(frame1_path)
    frame2 = cv2.imread(frame2_path)

    cv2.imwrite(frame1_first_path, frame1)
    cv2.imwrite(frame2_sec_path, frame2)

def compare_videos(video1_path, video2_path):
    frames1_folder = 'frames1'
    frames2_folder = 'frames2'
    similar_frames_folder = 'SimilarFrames'

    # Remove existing content in the folders
    shutil.rmtree(frames1_folder, ignore_errors=True)
    shutil.rmtree(frames2_folder, ignore_errors=True)
    shutil.rmtree(similar_frames_folder, ignore_errors=True)

    # Extract frames from video1 and video2
    extract_frames(video1_path, frames1_folder)
    extract_frames(video2_path, frames2_folder)

    similarity_count = 0
    total_comparisons = 0

    # Compare each frame from video1 with each frame from video2
    for frame1_file in os.listdir(frames1_folder):
        frame1_path = os.path.join(frames1_folder, frame1_file)

        for frame2_file in os.listdir(frames2_folder):
            frame2_path = os.path.join(frames2_folder, frame2_file)

            # Compare frames
            total_comparisons += 1
            if compare_images(cv2.imread(frame1_path), cv2.imread(frame2_path)):
                similarity_count += 1
                save_similar_frame_pair(similarity_count, frame1_path, frame2_path, similar_frames_folder)

    # Calculate and print the percentage of similar comparisons
    percentage_similarity = (similarity_count / total_comparisons) * 100

    return percentage_similarity
