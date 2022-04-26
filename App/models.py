from flask_sqlalchemy import SQLAlchemy,Model
from flask_migrate import Migrate

db = SQLAlchemy()

def get_migrate(app):
    return Migrate(app, db)

def create_db(app):
    db.init_app(app)
    db.create_all(app=app)
    
def init_db(app):
    db.init_app(app)

class Review(db.Model):
  id = db.Column(db.Integer,primary_key = True)
  text = db.Column('text',db.String,nullable = True)
  rating= db.Column('rating',db.Integer,nullable = True)
  isbn= db.Column('isbn',db.String,db.ForeignKey('book.isbn'))
  


class Book(db.Model):
  isbn = db.Column('isbn',db.String,primary_key=True)
  title = db.Column('title',db.String)
  publication_year =db.Column('publication_year',db.String)
  publisher = db.Column('publisher',db.String)
  author = db.Column('author',db.String)
  image = db.Column('image',db.String)
  reviews = db.relationship('Review', backref='book', lazy='dynamic')
  

  def get_avg_rating(code):
    Reviews = db.session.query.filter_by(Book.isbn == code).all()
    total = 0
    for r in Reviews:
      total += r.rating
    return total/len(Reviews)
      
    