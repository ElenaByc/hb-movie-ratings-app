"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# re-create a database
os.system('dropdb ratings')
os.system('createdb ratings')

# Connect to the database and call db.create_all:
model.connect_to_db(server.app)
model.db.create_all()

# Load data from data/movies.json and save it to a variable
# movie_data is a list of dictionaries
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings
movies_in_db = []
for movie in movie_data:
    # Get the title, overview, and poster_path from the movie dictionary
    title, overview, poster_path = (
        movie["title"],
        movie["overview"],
        movie["poster_path"],
    )
    # Get the release_date and convert it to a datetime object
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    # Create a movie and append it to movies_in_db
    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

# Add all movies to the SQLAlchemy session and commit them to db
model.db.session.add_all(movies_in_db)
model.db.session.commit()

# Create 10 users; each user will make 10 ratings
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for i in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(user, random_movie, score)
        model.db.session.add(rating)

model.db.session.commit()
