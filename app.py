from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='Template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.app_context().push()

db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(200))


@app.route('/add', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        new = Notes(title=title, content=content)
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/')

        except:
            return 'There are ERROR'
    else:
        return render_template('index.html')
    

@app.route('/')
def home():
    note = Notes.query.order_by(Notes.id).all()
    return render_template('home.html', data=note)


@app.route('/delete/<int:id>')
def delete(id):
    delete = Notes.query.get(id)

    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a ERROR'
    
@app.route('/edit/<int:id>', methods=["POST", "GET"])
def update(id):
    update_id = Notes.query.get(id)
    if request.method == 'POST':
        update_id.title = request.form['title']
        update_id.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There's ERROR"
    else:
        return render_template('edit.html', note=update_id)

if __name__ == "__main__":
    app.run(debug=True)