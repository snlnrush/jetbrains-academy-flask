from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean, Integer
import sys
import re


app = Flask(__name__)


db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'


class RegexTester(db.Model):
    __tablename__ = 'record'
    regex = Column(String(50), nullable=False)
    text = Column(String(1024), nullable=False)
    result = Column(Boolean, nullable=False)
    id = Column(Integer, primary_key=True)


db.create_all()


def save_db(regex, text, result):
    regex_tester = RegexTester(regex=regex, text=text, result=result)
    db.session.add(regex_tester)
    db.session.commit()
    entry = RegexTester.query.order_by(RegexTester.id).all()[-1]
    return entry.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        regex = request.form['regex']
        text = request.form['text']
        match = re.match(regex, text)
        result = bool(match)
        count_id = save_db(regex, text, result)
        return redirect(f'/result/{count_id}/')
        # return render_template('index.html', result=str(result))


@app.route('/history/', methods=['POST', 'GET'])
def history():
    if request.method == 'GET':
        entries = RegexTester.query.all()
        return render_template('history.html', entries=entries[:: -1])


@app.route('/result/<int:id>/', methods=['POST', 'GET'])
def result(id):
    if request.method == 'GET':
        entry = RegexTester.query.filter_by(id=id).all()
        return render_template('result.html', result=entry)
    if request.method == 'POST':
        regex = request.form['regex']
        text = request.form['text']
        match = re.match(regex, text)
        result = bool(match)
        count_id = save_db(regex, text, result)
        return render_template('index.html', result=str(result))


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
