from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
import telebot

app = Flask(__name__, static_url_path='/static')
app_dir = os.path.dirname(os.path.abspath(__file__)) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///redline.db'
app.config['SECRET_KEY'] = '4LceOr3wdHDusCXt6bzioyK8f12NXCcvXGhIP0XgPRm6GGHlWhP8dA'
bot_token = '6926337764:AAFHR2riRBsBtItfc5M_fC-C92_mtuUX5g4'
bot = telebot.TeleBot(bot_token)

db=SQLAlchemy(app)


class MainImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)

    def __str__(self) -> str:
        return self.filename

class MainText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __str__(self) -> str:
        return self.title

class Featured(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    discount = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(255), nullable=False)

    def __str__(self) -> str:
        return self.title

class EndWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    discount = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(255), nullable=False)
    stars = db.Column(db.Integer)

    def __str__(self) -> str:
        return self.title
    
    
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    stars = db.Column(db.Integer, default=1)

    def __str__(self) -> str:
        return self.title

# Представление для MainImages
@app.route('/admin/main_images/', methods=['GET', 'POST'])
def admin_main_images():
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = os.path.join('images/main-images/', file.filename)
            file.save(filename)
            
            new_image = MainImages(filename=filename)
            db.session.add(new_image)
            db.session.commit()

    main_images = MainImages.query.all()
    return render_template('admin_main_images.html', main_images=main_images)


@app.route('/admin/main_images/delete/<int:image_id>')
def delete_main_image(image_id):
    image_to_delete = MainImages.query.get_or_404(image_id)
    db.session.delete(image_to_delete)
    db.session.commit()
    return redirect(url_for('admin_main_images'))


# Представление для MainText
@app.route('/admin/main_text/', methods=['GET', 'POST'])
def admin_main_text():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_text = MainText(title=title, description=description)
        db.session.add(new_text)
        db.session.commit()

    main_texts = MainText.query.all()
    return render_template('admin_main_text.html', main_texts=main_texts)

@app.route('/admin/main_text/delete/<int:text_id>')
def delete_main_text(text_id):
    text_to_delete = MainText.query.get_or_404(text_id)
    db.session.delete(text_to_delete)
    db.session.commit()
    return redirect(url_for('admin_main_text'))


# Представление для Featured
@app.route('/admin/featured/', methods=['GET', 'POST'])
def admin_featured():
    if request.method == 'POST':
        filename = request.form.get('filename')
        title = request.form.get('title')
        discount = request.form.get('discount')
        price = request.form.get('price')
        new_featured = Featured(filename=filename, title=title, discount=discount, price=price)
        db.session.add(new_featured)
        db.session.commit()

    featured_items = Featured.query.all()
    return render_template('admin_featured.html', featured_items=featured_items)

@app.route('/admin/featured/delete/<int:featured_id>')
def delete_featured(featured_id):
    featured_to_delete = Featured.query.get_or_404(featured_id)
    db.session.delete(featured_to_delete)
    db.session.commit()
    return redirect(url_for('admin_featured'))


# Представление для EndWork
@app.route('/admin/end_work/', methods=['GET', 'POST'])
def admin_end_work():
    if request.method == 'POST':
        filename = request.form.get('filename')
        title = request.form.get('title')
        discount = request.form.get('discount')
        price = request.form.get('price')
        stars = request.form.get('stars')
        new_end_work = EndWork(filename=filename, title=title, discount=discount, price=price, stars=stars)
        db.session.add(new_end_work)
        db.session.commit()

    end_work_items = EndWork.query.all()
    return render_template('admin_end_work.html', end_work_items=end_work_items)

@app.route('/admin/end_work/delete/<int:end_work_id>')
def delete_end_work(end_work_id):
    end_work_to_delete = EndWork.query.get_or_404(end_work_id)
    db.session.delete(end_work_to_delete)
    db.session.commit()
    return redirect(url_for('admin_end_work'))


# Представление для Employee
@app.route('/admin/employee/', methods=['GET', 'POST'])
def admin_employee():
    if request.method == 'POST':
        filename = request.form.get('filename')
        title = request.form.get('title')
        description = request.form.get('description')
        stars = request.form.get('stars')
        new_employee = Employee(filename=filename, title=title, description=description, stars=stars)
        db.session.add(new_employee)
        db.session.commit()

    employees = Employee.query.all()
    return render_template('admin_employee.html', employees=employees)

@app.route('/admin/employee/delete/<int:employee_id>')
def delete_employee(employee_id):
    employee_to_delete = Employee.query.get_or_404(employee_id)
    db.session.delete(employee_to_delete)
    db.session.commit()
    return redirect(url_for('admin_employee'))

@app.route('/admin')
def admin():
    return render_template('admin_base.html')

@app.route('/')
def index():
    image_names = MainImages.query.all()
    featureds = Featured.query.all()
    works = EndWork.query.all()
    employees = Employee.query.all()
    return render_template('index.html', image_names=image_names, featureds=featureds, works=works, employees=employees) #['main-image1.png','main-image2.png','main-image3.png','main-image4.png']

@app.route('/images/<path:filename>')
def get_image(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'images'), filename)

@app.route('/<path:filename>')
def get_image2(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir), filename)

def get_image_names():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(root_dir, 'images')
    return [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)) if not f.startswith('.') and not f.startswith('h')]


@app.route('/static/js/<path:filename>')
def serve_js(filename):
    # Постройте абсолютный путь к папке с JavaScript файлами
    js_folder = os.path.join(app_dir, 'static', 'js')

    # Используйте send_from_directory для отправки файла
    return send_from_directory(js_folder, filename)

def send_to_telegram(chat_id, message_text):
    bot.send_message(chat_id, message_text)


@app.route('/submit_form_bot', methods=['GET', 'POST'])
def submit_form_bot():
    if request.method == 'POST':
        try:
            phone = request.form['phone']
            message = request.form['message']
            chat_id = '1022475729'
            
            # Отправка данных в телеграм
            send_to_telegram(chat_id, f'Новая заявка:\nтел:{phone}\nсообщение:{message}')
            flash('Успешно отправлено', 'success')
        except:
            flash('Успешно отправлено', 'error')
        return redirect(url_for('index'))


@app.route('/consult_form_bot', methods=['GET', 'POST'])
def consult_form_bot():
    if request.method == 'POST':
        try:
            phone = request.form['phone']
            chat_id = '1022475729'
            
            # Отправка данных в телеграм
            send_to_telegram(chat_id, f'Новая заявка на консультацию:\nтел:{phone}')
            flash('Успешно отправлено', 'success')
        except:
            flash('Успешно отправлено', 'error')
        return redirect(url_for('index'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

#https://www.youtube.com/watch?v=b7eJQSHhuO8&list=PL07efmqYWHZ_cxA1GvuXQMA-VYk8dhuiv&index=3
    



# @app.route('/upload', methods=['GET','POST'])
# def upload():
#     if 'file' not in request.files:
#         return render_template('upload.html')

#     file = request.files['file']

#     if file.filename == '':
#         return redirect(request.url)

#     if file:
#         filename = os.path.join('images/featured/', file.filename)
#         file.save(filename)
#         title = request.form['title']
#         discount = request.form['discount']
#         price = request.form['price']
#         new_image = Featured(filename=file.filename, title=title, discount=discount, price=price)
#         db.session.add(new_image)
#         db.session.commit()

#         return redirect(url_for('index'))
    

# @app.route('/works', methods=['GET','POST'])
# def upload_works():
#     if 'file' not in request.files:
#         return render_template('works.html')

#     file = request.files['file']

#     if file.filename == '':
#         return redirect(request.url)

#     if file:
#         filename = os.path.join('images/works/', file.filename)
#         file.save(filename)
        
#         title = request.form['title']
#         discount = request.form['discount']
#         price = request.form['price']
#         stars = int(request.form['stars']) if not isinstance(request.form['stars'], int) else request.form['stars']
        
#         new_image = EndWork(filename=file.filename, title=title, discount=discount, price=price, stars=stars)
#         db.session.add(new_image)
#         db.session.commit()

#         return redirect(url_for('index'))
    

# @app.route('/employee', methods=['GET','POST'])
# def upload_employee():
#     if 'file' not in request.files:
#         return render_template('employee.html')

#     file = request.files['file']

#     if file.filename == '':
#         return redirect(request.url)

#     if file:
#         filename = os.path.join('images/employee/', file.filename)
#         file.save(filename)
        
#         title = request.form['title']
#         description = request.form['description']

#         stars = int(request.form['stars']) if not isinstance(request.form['stars'], int) else request.form['stars']
        
#         new_image = Employee(filename=file.filename, title=title, description=description, stars=stars)
#         db.session.add(new_image)
#         db.session.commit()

#         return redirect(url_for('index'))