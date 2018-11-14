from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from flask_wtf import CSRFProtect
import forms

app = Flask(__name__)


#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mars24601@'
app.config['MYSQL_DB'] = 'note_app'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Init MySQL
mysql = MySQL(app)
csrf = CSRFProtect(app)

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/notes')
def my_notes():
  cur = mysql.connection.cursor()

  result = cur.execute("SELECT * FROM notes")

  notes = cur.fetchall()

  cur.close()
  if result > 0 :
    return render_template('notes.html', notes = notes)
  else: 
    return 'No data'

  

@app.route('/note/<string:id>/')
def note(id):
  cur = mysql.connection.cursor()

  cur.execute("SELECT * FROM notes WHERE id = %s",(id))

  note = cur.fetchone()

  cur.close()
  return render_template('note.html', note = note)




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
    cur.execute("INSERT INTO notes(title, description) VALUES (%s,%s)", 
    (title, description))
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
    return redirect(url_for('index'))
  return render_template('register.html', form = form) 



if __name__ == '__main__':
  app.secret_key = 'secret12345'
  app.run(debug=True)