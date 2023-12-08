from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    image_names = get_image_names()
    return render_template('index.html', image_names=['main-image1.png','main-image2.png','main-image3.png','main-image4.png'])

@app.route('/images/<path:filename>')
def get_image(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'images'), filename)

def get_image_names():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(root_dir, 'images')
    return [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

if __name__ == '__main__':
    app.run(debug=True)

#timecode 33:20
#https://www.youtube.com/watch?v=b7eJQSHhuO8&list=PL07efmqYWHZ_cxA1GvuXQMA-VYk8dhuiv&index=3