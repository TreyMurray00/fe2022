import os
from flask import Flask, redirect, render_template, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
from sqlalchemy.exc import OperationalError
from App.models import db, get_migrate, create_db,Book,Review

def create_app():
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'MySecretKey'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    create_db(app)
    app.app_context().push()
    return app

app = create_app()

migrate = get_migrate(app)


@app.route('/', methods=['GET'])
def home():
  books = Book.query.all()
  return render_template('app.html',books=books)


@app.route('/book/<id>',methods=['GET'])
def show(id):
  books = Book.query.all()
  book = Book.query.filter_by(isbn = id).first()
  
  print(book.reviews.all())
  revs = book.reviews.all()
  if len(revs) != 0:
    return render_template('app.html',reviews = revs,books = books, isbn = id)

  return render_template('app.html',books = books, isbn = id)


@app.route('/review/<id>',methods=['POST'])
def review(id):
  data = request.form
  data = data.to_dict()
  if len(data) > 1:
    newReview = Review(  
      text = data['review'],
      rating= data['rating'],
      isbn= id
    )
    db.session.add(newReview)
    db.session.commit()
  return redirect('/')

@app.route('/delete/<id>',methods=['GET'])
def delete_review(id):
  rev = Review.query.filter_by(id = id).first()
  db.session.delete(rev)
  db.session.commit()
  return redirect('/')



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)