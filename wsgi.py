import click
from flask import Flask
from App import create_db, db, app
import csv
from App.models import*

@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')

@app.cli.command("populate")
def pop():
  with open(r'books.csv') as books:
    reader = csv.DictReader(books)
    for row in reader:
      print(row)
      newBook = Book(
          isbn = row["ISBN"],
          title = row["Book-Title"],
          author = row["Book-Author"],
          publication_year =row["Year-Of-Publication"],
          publisher = row["Publisher"],
          image = row["Image-URL-M"]
      )
      db.session.add(newBook)
      db.session.commit()