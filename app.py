from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQlALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

# > python
# >>> from app import app, db
# >>> app.app_context().push()
# >>> db.create_all()
# >>> exit()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')  # отслеживание
@app.route('/home')  # отслеживание
def index():
    return render_template("index.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()  # все записи отсортированные по дате
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/agile')
def agile():
    return render_template("agile.html")


@app.route('/aqa')
def aqa():
    return render_template("aqa.html")


@app.route('/css')
def css():
    return render_template("css.html")


@app.route('/git')
def git():
    return render_template("git.html")


@app.route('/sql')
def sql():
    return render_template("sql.html")


@app.route('/create-article', methods=['POST', 'GET'])  # отслеживание
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        # intro = request.form["intro"]
        text = request.form["text"]
        # article = Article(title=title, intro=intro, text=text)
        article = Article(title=title, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form["title"]
        # article.intro = request.form["intro"]
        article.text = request.form["text"]
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При обновлении статьи произошла ошибка"
    else:
        return render_template("post_update.html", article=article)


if __name__ == "__main__":
    app.run(debug=True)
