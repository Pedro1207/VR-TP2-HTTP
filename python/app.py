from flask import Flask, request, url_for, redirect, render_template, make_response
from werkzeug.utils import secure_filename
import os
import auth

# Files stored in
UPLOAD_FOLDER = 'static/'

# Allowed files extensions for upload
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Check file has an allowed extension
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET','POST'])
def home():
	user = request.cookies.get('vr_username')
	token = request.cookies.get('vr_token')

	if not user or not token:
		return redirect("http://172.20.0.11/elogin?redirect=http://172.21.0.12/loginreturn")
	else:
		check = auth.check_login(user, token)
		if not check:
			return redirect("http://172.20.0.11/elogin?redirect=http://172.21.0.12/loginreturn")
		else:
			if auth.check_admin(user):
				return redirect(url_for('admin'))
			else:
				return redirect(url_for('user'))


@app.route('/loginreturn')
def loginreturn():
	print("login_return")
	user = request.args.get('user')
	token = request.args.get('token')
	if not user or not token:
		return redirect(url_for('home'))
	else:
		resp = make_response(redirect(url_for('admin')))
		resp.set_cookie('vr_username', user)
		resp.set_cookie('vr_token', token)
		return resp


@app.route('/admin', methods=['GET','POST'])
def admin():
	user = request.cookies.get('vr_username')
	token = request.cookies.get('vr_token')

	if(auth.check_login(user, token)):
		if(not auth.check_admin(user)):
			return redirect(url_for('user'))
	else:
		return redirect(url_for('home'))


	# If a post method then handle file upload
	if request.method == 'POST':
		if 'file' not in request.files:
			return redirect('/')
		file = request.files['file']

		if file.filename == '':
			return redirect('/')

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


	# Get Files in the directory and create list items to be displayed to the user
	file_list = []
	for f in os.listdir(app.config['UPLOAD_FOLDER']):
		# Create link html
		file_list.append(f)

	return render_template("index_admin.html", files=file_list)

@app.route('/user', methods=['GET'])
def user():

	user = request.cookies.get('vr_username')
	token = request.cookies.get('vr_token')

	if(not auth.check_login(user, token)):
		return redirect(url_for('home'))


	# Get Files in the directory and create list items to be displayed to the user
	file_list = []
	for f in os.listdir(app.config['UPLOAD_FOLDER']):
		# Create link html
		file_list.append(f)

	return render_template("index_user.html", files=file_list)

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0', port=80)
