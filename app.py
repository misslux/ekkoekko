from crypt import methods
from flask import Flask, render_template, flash, request, redirect, url_for, session
import os
import pandas as pd

# PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
app.secret_key = "siemens"
app.config['UPLOAD_FOLDER'] = 'static/images'
app.secret_key = 'QWERTYUIOP'

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getFoundItems(name=None):
    df = pd.read_csv('static/found_items.csv')
    if name is not None:
        df = df.loc[df['Contact Name']==name]
    return df.to_dict(orient='records')

def getLostItems(name=None):
    df = pd.read_csv('static/lost_items.csv')
    if name is not None:
        df = df.loc[df['Contact Name']==name]
    return df.to_dict(orient='records')


@app.route('/')
def homepage():
    found_items = getFoundItems()
    lost_items = getLostItems()
    return render_template('index.html',lost=lost_items, found=found_items, lost_length=len(lost_items), found_length=len(found_items))

@app.route('/delete_found', methods=['POST'])
def delete_found():
    id = request.form['id']
    print('delete found item', id)
    df = pd.read_csv('static/found_items.csv')
    df = df.loc[df.ID != int(id)]
    df.to_csv('static/found_items.csv', index=False)
    return redirect(f"/my/{session['user_info']}")

@app.route('/delete_lost', methods=['POST'])
def delete_lost():
    id = request.form['id']
    print('delete lost item', id)
    df = pd.read_csv('static/lost_items.csv')
    df = df.loc[df.ID != int(id)]
    df.to_csv('static/lost_items.csv', index=False)
    return redirect(f"/my/{session['user_info']}")

@app.route('/index')
def index():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    return redirect('index')


@app.route('/my/')
@app.route('/my/<name>')
def my(name=None):
    found_items = getFoundItems(name)
    lost_items = getLostItems(name)
    return render_template('my.html', lost=lost_items, found=found_items, lost_length=len(lost_items), found_length=len(found_items))


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
    if user == 'Xiao' and pwd == '123':
        session['user_info'] = user
        return redirect(f'/my/{user}')
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
