from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///redline.db'
db=SQLAlchemy(app)

class Featured(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    discount = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(255), nullable=False)

    def __str__(self) -> str:
        return self.title

@app.route('/upload', methods=['GET','POST'])
def upload():
    if 'file' not in request.files:
        return render_template('upload.html')

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join('images/featured/', file.filename)
        file.save(filename)
        title = request.form['title']
        discount = request.form['discount']
        price = request.form['price']
        new_image = Featured(filename=file.filename, title=title, discount=discount, price=price)
        db.session.add(new_image)
        db.session.commit()

        return redirect(url_for('index'))
    

@app.route('/')
def index():
    image_names = get_image_names()
    featureds = Featured.query.all()
    return render_template('index.html', image_names=image_names, featureds=featureds) #['main-image1.png','main-image2.png','main-image3.png','main-image4.png']

@app.route('/images/<path:filename>')
def get_image(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'images'), filename)

def get_image_names():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(root_dir, 'images')
    return [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) if not f.startswith('.') and not f.startswith('h')]

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

#timecode 58:47
#https://www.youtube.com/watch?v=b7eJQSHhuO8&list=PL07efmqYWHZ_cxA1GvuXQMA-VYk8dhuiv&index=3