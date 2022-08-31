from flask import Flask, render_template,flash, request, redirect, url_for
import os
import pandas as pd

# PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
app.secret_key = "siemens"
app.config['UPLOAD_FOLDER'] = 'static/images'

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getFoundItems():
    df = pd.read_csv('static/lost_items.csv')
    return df.Image.values, df.Description.values

def getLostItems():
    df = pd.read_csv('static/lost_items.csv')
    return df.to_dict(orient='records')
	
@app.route('/')
def homepage():
    records = getLostItems()
    return render_template('index.html',lost=records, found=records, lost_length=len(records), found_length=len(records))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/newlost', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='images/' + filename), code=301)

if __name__ == "__main__":

    app.run(debug=True)
