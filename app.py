from flask import Flask, render_template, send_from_directory
import os
from datetime import datetime
from threading import Thread
import webbrowser

app = Flask(__name__)

# Premium Configuration
app.config.update({
    'SEND_FILE_MAX_AGE_DEFAULT': 3600,
    'STATIC_FOLDER': 'static',
    'AUDIO_FOLDER': 'audio',
    'IMAGES_FOLDER': 'images'
})

# Create premium folders structure
for folder in [app.config['STATIC_FOLDER'], app.config['AUDIO_FOLDER'], app.config['IMAGES_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

@app.route('/')
def home():
    now = datetime.now()
    return render_template("index.html", 
                         current_year=now.year)

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'], filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Create default files if they don't exist
    default_files = {
        'audio/birthday_song.mp3': b'',
        'images/sandhya_photo.jpg': b''
    }
    
    for filepath, content in default_files.items():
        if not os.path.exists(filepath):
            with open(filepath, 'wb') as f:
                f.write(content)
    
    # Open browser automatically
    Thread(target=open_browser).start()
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )