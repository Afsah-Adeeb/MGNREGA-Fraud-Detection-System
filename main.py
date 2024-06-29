import os
import sys
from video_comparison import compare_videos

# Get the path of the uploaded video from the command-line argument
uploaded_video_path = sys.argv[1]
# uploaded_video_path = "Videos/video 1.2.mp4"
print(f"{uploaded_video_path}")

# Set the path for the existing videos folder
videos_folder = 'videos'

# Get the list of video files in the "Videos" folder
video_files = [f for f in os.listdir(videos_folder) if f.endswith('.mp4')]

# Initialize variables to store information about the similar video
similar_video_found = False
similar_video_name = ""

# Compare the uploaded video with each video in the "Videos" folder
for video_file in video_files:
    video_path = os.path.join(videos_folder, video_file)
    percentage_similarity = compare_videos(uploaded_video_path, video_path)

    # Check if the percentage similarity is greater than 10%
    if percentage_similarity > 10:
        similar_video_found = True
        similar_video_name = video_file
        print(f"There is a similar existing video: {similar_video_name}!")
        result = f"There is a similar existing video: {similar_video_name}!"
        with open('output.txt', 'w') as result_file:
            result_file.write(result)
        break

# If no similar video is found, print "This video is a new one!"
if not similar_video_found:
    result = "This video is a new one!"
    with open('output.txt', 'w') as result_file:
        result_file.write(result)
    print("This video is a new one!")
