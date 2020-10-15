import peeweedbevolve # new; must be imported before models
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Store
import os



app = Flask(__name__)


app.secret_key = os.getenv('SECRET_KEY')


@app.before_request
def before_request():
   db.connect()

@app.after_request
def after_request(response):
   db.close()
   return response

@app.cli.command() # new
def migrate(): # new 
   db.evolve(ignore_tables={'base_model'}) # new

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/store")
def store():
   return render_template('store.html')

@app.route("/store_form")
def store_form():
    s = Store(name=request.args['name'])

    if s.save():
        flash("Successfuly save")
        return redirect(url_for('store'))
    else:
        return render_template('store.html', name=request.args['name'] )

if __name__ == '__main__':
   app.run()