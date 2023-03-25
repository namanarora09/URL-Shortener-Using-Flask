import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pyshorteners

app = Flask(__name__)

############# SQL Alchemy Configuration #################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#######################################################

type_tiny = pyshorteners.Shortener()

############# Create a Model #################


class URL(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.Text)
    short_url = db.Column(db.Text)

    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url

    def __repr__(self):
        return "Long URL - {} and Short URL - {}".format(self.long_url, self.short_url)
##############################################


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/showUrl', methods=["GET", "POST"])
def showUrl():
    if request.method == "POST":
        long_url = request.form.get('longUrl')
        short_url = type_tiny.tinyurl.short(long_url)
        new_uri = URL(long_url, short_url)
        db.session.add(new_uri)
        db.session.commit()
    return render_template('display.html', short_url=short_url)


@app.route('/history')
def history():
    urls = URL.query.all()
    return render_template('history.html', urls=urls)


if __name__ == '__main__':
    app.run(debug=True)
