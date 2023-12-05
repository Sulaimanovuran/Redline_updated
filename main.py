from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    context = [
        "main-image1.jpg",
        "main-image2.jpg",
        "main-image3.jpg",
        "main-image4.jpg",
    ]
    return render_template('base.html', context=context)

if __name__ == '__main__':
    app.run(debug=True)

#timecode 33:20