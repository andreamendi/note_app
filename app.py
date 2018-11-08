from flask import Flask, render_template
# from data import Notes
from flask_mysqldb import MySQL


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

# @app.route('/note/<string:id>/')
# def note(id):
#     for note in notes:
#         if note['id'] == int(id):
#             data = note
#             break
#     return render_template("note.html", note = data)

if __name__ == '__main__':
    app.run(debug= True)
    #Debug = true, es para que se actualize solo, lo único que hay que hacer es refrescar el navegador.
    # Sí de desea establecer un puerto en particular es -> app.run(port = 4444)
