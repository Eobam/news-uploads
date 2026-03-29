# imports, will include all at top cuz i don't feel like organizing them by type as i normally do
from flask import Flask, render_template, request, send_from_directory, jsonify
import os

app = Flask(__name__)

#folders
video_uploadfolder = 'uploads'
os.makedirs(video_uploadfolder, exist_ok=True)

a_pass = '1234567890'

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        video_file = request.files.get('video_file')
        password = request.form.get('password')
        

        if password != a_pass:
            return jsonify({'error': 'incorrect password'}), 403


        if video_file:
            video_file.save(os.path.join(video_uploadfolder, video_file.filename))
            return jsonify({'filename': video_file.filename})

    return render_template('index.html')

@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory(video_uploadfolder, filename)

@app.route('/videos')
def list_videos():
    files = os.listdir(video_uploadfolder)
    files.sort(key=lambda f: os.path.getmtime(os.path.join(video_uploadfolder, f)), reverse=True)
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True)