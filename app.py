from flask import Flask, render_template, flash, request, redirect, url_for, session
import os

# PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
app.secret_key = "siemens"
app.config['UPLOAD_FOLDER'] = 'static/images'
app.secret_key = 'QWERTYUIOP'

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getFoundItems():
    return


def getLostItems():
    return


@app.route('/')
def homepage():
    # 改成读文件和文件名避免写死
    path = "static/img/items/"
    files = os.listdir(path)
    items = []
    description = []
    for file in files:
        items.append(path + file)
        description.append(str(file).split('.')[0])

    # items = ['static/img/iPhone.jpg', 'static/img/rolex.jpg',
    #          'static/img/mi.jpg', 'static/img/latiao.jpg',
    #          'static/img/latiao.jpg']
    # description = ['Iphone手机', '手表', '小米手机', '辣条', '辣条']

    return render_template('index.html', len=len(items), items=items, description=description)


@app.route('/index')
def index():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    return redirect('index')


@app.route('/my')
def my():
    return render_template('my.html')


@app.route('/myinfo')
def myinfo():
    return render_template('myinfo.html')


@app.route('/surprise')
def surprise():
    return render_template('surprise.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('form-username')
    pwd = request.form.get('form-password')
    if user == 'admin' and pwd == '123':
        session['user_info'] = user
        return redirect('/my')
    else:
        return render_template('login.html', msg='用户名or密码错误~~')


@app.route('/logout')
def logout():
    del session['user_info']
    return redirect('login')




# @app.route('/', methods=['POST'])
# def upload_image():
# 	if 'file' not in request.files:
# 		flash('No file part')
# 		return redirect(request.url)
# 	file = request.files['file']
# 	if file.filename == '':
# 		flash('No image selected for uploading')
# 		return redirect(request.url)
# 	if file and allowed_file(file.filename):
# 		filename = secure_filename(file.filename)
# 		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 		#print('upload_image filename: ' + filename)
# 		flash('Image successfully uploaded and displayed below')
# 		return render_template('upload.html', filename=filename)
# 	else:
# 		flash('Allowed image types are -> png, jpg, jpeg, gif')
# 		return redirect(request.url)

# @app.route('/display/<filename>')
# def display_image(filename):
# 	#print('display_image filename: ' + filename)
# 	return redirect(url_for('static', filename='images/' + filename), code=301)

if __name__ == "__main__":
    app.run()
