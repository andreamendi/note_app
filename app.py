from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
import forms
from _mysql_exceptions import OperationalError

app = Flask(__name__)


#Config MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'note_app'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config.from_object(DevelopmentConfig)


#Init MySQL
mysql = MySQL(app)


@app.errorhandler(404)
def page_not_found(e):
  print(e)

  return render_template('error_404.html')




@app.route('/')
def index():
  if 'logged_in' in session:
    message = "{}'s notes".format(session['username'])
   
  else:
    message = 'Hello user!'
  
  return render_template('home.html', message = message)





@app.route('/notes')
def my_notes():
  cur = mysql.connection.cursor()

  result = cur.execute("SELECT * FROM notes WHERE id_user = %s", [session['id_user']])

  notes = cur.fetchall()

  cur.close()
  if result > 0 :
    return render_template('notes.html', notes = notes)
  else: 
    mensaje = 'No tienes notas'
    return render_template('notes.html', mensaje = mensaje)
    


  

@app.route('/note/<string:id>/')
def note(id):
  cur = mysql.connection.cursor()

  cur.execute("SELECT * FROM notes WHERE id = %s",(id))

  note = cur.fetchone()

  cur.close()
  return render_template('note.html', note = note)





@app.route('/search', methods=['POST'])
def search():
  form = request.form
  param = form['search']
  cur = mysql.connection.cursor()

  query = "SELECT * FROM notes WHERE (id_user = {}) AND (title LIKE '%{}%' OR description LIKE '%{}%')".format(session['id_user'],param,param)
  result = cur.execute(query)
  
  if result > 0:
    
    # cur.fetchone() te trae el primero
    # cur.fetchall() te trae todoooo lo que encuentra
    notes = cur.fetchall()

    cur.close()
    return render_template('notes.html', notes = notes)
  else:
    mensaje = 'No hay notas compatibles'
    return render_template('notes.html', mensaje = mensaje)
    




@app.route('/add-note', methods=['GET', 'POST'])
def add_note():
  form = forms.NoteForm(request.form)
  print(request.method)

  if request.method == 'POST' and form.validate():
    title = form.title.data
    description = form.description.data

    #Create cursor
    cur = mysql.connection.cursor()

    #Execute
    cur.execute("INSERT INTO notes(title, description, id_user) VALUES (%s,%s,%s)", 
    (title, description,session['id_user']))
    mysql.connection.commit()
    cur.close()
    flash('Agregaste un post', 'success')
    return redirect(url_for('add_note'))

  return render_template('add_note.html', form = form)





@app.route('/edit-note/<string:id>/',methods=['GET', 'POST'])
def edit_note(id):
  cur = mysql.connection.cursor()

  cur.execute("SELECT * FROM notes WHERE id = %s",(id))
  note = cur.fetchone()

  cur.close()

  form = forms.NoteForm(request.form)
  form.title.data = note['title']
  form.description.data = note['description']

  if request.method == 'POST' and form.validate():
    print(request.method)
    title = request.form['title']
    description = request.form['description']
    #Create cursor
    cur = mysql.connection.cursor()
    #Execute
    cur.execute("UPDATE notes SET title = %s, description = %s WHERE id = %s", (title, description,id))
    # Commit to DB
    mysql.connection.commit()
    # Close connection 
    cur.close()
    return redirect(url_for('my_notes'))

  return render_template('edit_note.html', form = form)





@app.route('/delete-note/<string:id>', methods = ['POST'])
def delete_note(id):
  print(request.method)
  #Create cursor
  cur = mysql.connection.cursor()
  #Execute
  cur.execute ("DELETE FROM notes WHERE id = %s", [id])
  # Commit to DB
  mysql.connection.commit()
  # Close connection 
  cur.close() 
  return redirect(url_for('my_notes'))





@app.route('/register', methods=['GET','POST'])
def register():
  form = forms.RegisterForm(request.form)
  print(request.method)

  if request.method == 'POST' and form.validate():
    name = form.name.data
    username = form.username.data
    password = sha256_crypt.encrypt(str(form.password.data))
    email = form.email.data

    #Create cursor
    cur = mysql.connection.cursor()

    #Execute
    cur.execute("INSERT INTO users(name, username, email, password) VALUES (%s,%s,%s,%s)", 
    (name, username, email, password))
    mysql.connection.commit()
    cur.close()
    flash('Muy bien, ya estas registrad@', 'success')
    return redirect(url_for('log_in'))
  return render_template('register.html', form = form) 





@app.route('/log-in', methods=['GET', 'POST'])
def log_in():
  form = forms.LoginForm(request.form)
  print(request.method)
  if request.method == 'POST' and form.validate():
    username_candidate = form.username.data
    
    print(username_candidate)
    print('Hola')
    password_candidate = form.password.data

    #Vamos a conectarnos con SQL
    cur = mysql.connection.cursor()
    try:
      cur.execute("SELECT * FROM users WHERE username = %s",[username_candidate])
      user = cur.fetchone()
      print(user['password'])
      
      password_verify =  sha256_crypt.verify(password_candidate, user['password'])
      print(password_verify)
      if password_verify:
          session['logged_in'] = True
          session['username'] = user['username']
          session['id_user'] = user['id']
          cur.close()
          return redirect(url_for('index'))
      else:
        flash("Password or Username incorrect", 'danger')
    except OperationalError:
      flash("No hay contexión a la DataBase", 'danger')
    except:
      flash("Password or Username incorrect", 'danger')
      
  return render_template('log_in.html', form = form) 





@app.route('/edit-profile/<string:id>/',methods=['GET', 'POST'])
def edit_profile(id):
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM users WHERE id = %s",(id))
  user_edit = cur.fetchone()
  cur.close()

  form = forms.EditForm(request.form)
  form.name.data = user_edit['name']
  form.email.data = user_edit['email']

  print(form.validate())

  if request.method == 'POST' and form.validate():
    print(request.method)
    
    if request.form['password']:
      password = sha256_crypt.encrypt(str(request.form['password']))
    else:
      password = user_edit['password']

    name = request.form['name']
    email = request.form['email']

    print(name)
    print(email)
    print(password)

    #Create cursor
    cur = mysql.connection.cursor()
    #Execute
    if user_edit['name'] != name:
      cur.execute("UPDATE users SET name = %s WHERE id = %s", (name,id))
      flash('Tu nombre quedo editado', 'success')
    if user_edit['email'] != email:
      cur.execute("UPDATE users SET email = %s WHERE id = %s", (email,id))
      flash('Tu email quedo editado', 'success')
    if user_edit['password'] != password:
      cur.execute("UPDATE users SET password = %s WHERE id = %s", (password,id))
      flash('Tu password quedo editado', 'success')

    # Commit to DB
    mysql.connection.commit()
    # Close connection 
    cur.close()
    return redirect(url_for('my_notes'))

  return render_template('edit_profile.html', form = form)





@app.route('/logout')
def logout ():
  session.clear()
  flash("You're now logged out", 'success')
  return redirect(url_for('log_in'))








if __name__ == '__main__':
  csrf = CSRFProtect(app)
  app.run()