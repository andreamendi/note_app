from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# from data import Notes



app = Flask(__name__) 
# notes = Notes()

# Config SQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mars24601@'
app.config['MYSQL_DB'] = 'note_app'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'



#Init MySQL
mysql  = MySQL(app)



@app.route('/')
def index():  
    return render_template("home.html")

@app.route('/notes')
def my_notes():
    return render_template("notes.html")

# El debajo se comento ya que era prueba.
# @app.route('/note/<string:id>/')
# def note(id):
#     for note in notes:
#         if note['id'] == int(id):
#             data = note
#             break
#     return render_template("note.html", note = data)



class NoteForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=45)])
    description = TextAreaField('Description', [validators.Length(min=5)])

@app.route('/add-note', methods=['GET','POST'])
def add_note():
    form = NoteForm(request.form)
    
    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data

        #Create a Cur -> o sea una conexion con la DB
        cur = mysql.connection.cursor()

        #Execute
        cur.execute('INSERT INTO notes(title, description) VALUES (%s,%s)', (title,description))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('add_note'))

    return render_template('add_note.html', form=form)


# El "if" debe de ir al final sino no va a correr

if __name__ == '__main__':
    app.run(debug= True)
    #Debug = true, es para que se actualize solo, lo único que hay que hacer es refrescar el navegador.
    # Sí de desea establecer un puerto en particular es -> app.run(port = 4444)