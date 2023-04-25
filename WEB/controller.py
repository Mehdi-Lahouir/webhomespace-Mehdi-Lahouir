from datetime import datetime
import hashlib
import os
import subprocess
from flask import(
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
    send_file,
    session,
    url_for,
)
from dal import UserAccount
from model import user
app=Flask(__name__)
app.secret_key='1234'
size=0
@app.route('/')
def index():
    return render_template('login.html') 

@app.route('/signupView')
def signupView():
    return render_template('signup.html')

@app.route('/loginView')
def loginView():
    return render_template('login.html')

@app.route('/loginView', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form['email']
        pwd = request.form['password']
        user_account = UserAccount()  
        if user_account.Login(user(name, pwd)):
            response = app.make_response(render_template('app.html'))
            session['user_id'] = name
            session['password']= pwd
            return response
        else:
            return render_template('signup.html', error_auth='login or password incorrect')
    else:
        if 'user_id' in session:
            return render_template('app.html')
        return redirect('/') 
    
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('password',None)
    return redirect('/')

@app.route('/download')
def Download():
    if session['user_id'] is None or session['password'] is None: 
        return redirect('/')
    else:
        user_account = UserAccount()  
        user_account.zipfile(user(session['user_id'],session['password']))
        return send_file('/tmp/homedir.zip', as_attachment=True)
    
@app.route('/files')
def get_files():
    username = session['user_id']  
    files=UserAccount().getFiles(username)
    return jsonify(files)

@app.route('/num_files')
def get_num_files():
    username = session['user_id']
    password = session['password']
    num_files=UserAccount().get_nume_files(username,password)
    return jsonify(num_files)

@app.route('/num_dirs')
def get_num_dirs():
    username = session['user_id']
    password = session['password']
    num_dirs=UserAccount().get_num_dirs(username,password)
    return jsonify(num_dirs)

@app.route('/total_size')
def get_total_size():
    username = session['user_id']
    password = session['password']
    total_size = UserAccount().get_total_size(username,password)
    return jsonify(total_size)
@app.route('/search',methods=["POST"])
def get_searched():
    if request.method == "POST":
        username = session['user_id']  
        name = request.form['search']
        files=UserAccount().getFiles(username,name)
        return jsonify(files)
#aksdokmw;;qownvcewlnmkqvea
if(__name__ == "__main__"):
    app.run(host="0.0.0.0",port=8800, debug=True)