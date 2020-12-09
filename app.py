# import flask
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskDatabase.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    intro = db.Column(db.String(300), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    articles = User.query.order_by(User.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def posts_details(id):
    article = User.query.get(id)
    return render_template('posts-detail.html', article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        users = User(title=title, intro=intro, text=text)
        try:
            db.session.add(users)
            db.session.commit()
            return redirect('/posts')
        except TypeError:
            return 'при добавлении статьи произошла ошибка'
    else:
        return render_template("create-article.html")


if __name__ == '__main__':
    app.run(debug=True)
