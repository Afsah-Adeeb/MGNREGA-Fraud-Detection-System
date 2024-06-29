from flask import Flask, render_template, request, redirect, url_for
import os
from blur_detection import process_video

app = Flask(__name__, static_url_path='/static')

# # Set the path for the uploaded videos folder
# app.config['UPLOAD_FOLDER'] = 'uploads'

# # Set a secret key for the session
# app.config['SECRET_KEY'] = 'your_secret_key'

# # Set the maximum allowed file size (in bytes)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Function to check if a video is blurred
def is_blurred(video_path):
    # Add your blur detection logic here
    return process_video(video_path).startswith("\nThe video is NOT good")

# Route for the main page
@app.route('/')
def index():
    result = request.args.get('result', default=None)
    return render_template('index.html', result=result)

# Route for video processing
@app.route('/process_video', methods=['POST'])
def process_video_route():
    if 'videoFile' not in request.files:
        return redirect(url_for('index', result="No video file provided"))
    # print(f{video_file})
    video_file = request.files['videoFile']
    
    # Save the uploaded video
    video_path = os.path.join('uploads', video_file.filename)
    video_file.save(video_path)
    
    
    # Check if the video is blurred
    if is_blurred(video_path):
        return redirect(url_for('index', result="Video is blurred! Try again..."))
    else:
        # Pass the video to main.py for further processing
        os.system(f"python main.py {video_path}")
        
        # Read the result from main.py (modify as needed)
        with open('output.txt', 'r') as result_file:
            result = result_file.read()

        return redirect(url_for('index', result=result))
        # return result

if __name__ == '__main__':
    app.run(debug=True)
