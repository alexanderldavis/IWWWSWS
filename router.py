# from flask.ext.sqlalchemy import SQLAlchemy
# import json
# from json import load
# import os
# from bs4 import BeautifulSoup
# import urllib.parse
# import requests as req
# from flask import Flask, render_template, request
# from flask_wtf import Form
# from flask_sqlalchemy import SQLAlchemy
# from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
# from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy.sql import select
# import init
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import os
from flask_wtf import Form
from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
from wtforms import StringField, SelectField

app = Flask(__name__)
# urllib.parse.uses_netloc.append("postgres")
# url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
# db = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)


app.config['SQLALCHEMY_DATABASE_URI']=os.environ["DATABASE_URL"]
# db = SQLAlchemy(app)
# engine = create_engine(os.environ["DATABASE_URL"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'wtforms more like wtf forms'
db = SQLAlchemy(app)

class SearchForm(Form):
    options = SelectField('Search By:', [validators.Required()], choices=[('FamilyNight', 'Family Night'), ('DateNight', 'Date Night'),('GirlsNight', 'Girls Night'),('GuysNight', 'Guys Night'), ('NerdNight', 'Nerd Night'), ('CulturedNight', 'Cultured Movie Night'), ('SurpriseMe', 'Surprise Me')])

@app.route("/", methods=['GET'])
def index():
    form = SearchForm()
    return render_template('welcome.html', form=form)


### SEARCH FOR RECCOMMENDATONS ###
@app.route("/search")
def search():
    activity=request.args['selected_activity']
    print(activity)
    # cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar';""")
    if activity=="FamilyNight":
        # cur.execute("""SELECT movies.id, movies.title, movies.poster, movies.rated, movies.rating from movies join activities_movies on (activities_movies.movie_id=movies.id) join activity on (activities_movies.activity_id=acitvities.id) WHERE activities.name='%s' limit 5;"""%activity)
        # s = select([movie]).where(title == 'Avatar')
        # result = db.session.execute(s)
        # print(result)
        res = db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated from \
                                    genre join movie_genre on (genre.id=movie_genre.genre_id) join movie on (movie_genre.movie_id=movie.id)\
                                    where (((genre.genre='Adventure') or (genre.genre='Comedy') or (genre.genre='Animation') or (genre.genre='Mistery') or (genre.genre='Fantasy')) and ((movie.rated='PG13') or (movie.rated='PG')))\
                                    order by rating limit 5;""")
    res = res.fetchall()
    return render_template('searchresults.html', movieList = res)



# import psycopg2
# from flask import Flask, render_template, request
# import os
# import urllib.parse
# import json
#
# urllib.parse.uses_netloc.append("postgres")
# url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
# conn = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
#
#
# app = Flask(__name__)
#
# ### WELCOME ###
# @app.route("/")
# def index():
#     cur = conn.cursor()
#     # cur.execute("""SELECT id, title, description, year, rated, runtime from movies where title = 'Avatar';""")
#     # cur.execute("""SELECT id, title, poster, rated FROM movies where title = 'Avatar';""")
#     cur.execute("""SELECT * from genres;""")
#     genreList = cur.fetchall()
#     # cur.execute("""SELECT * from services;""")
#     # serviceList=cur.fetchall()
#     cur.execute("""SELECT * from activities;""")
#     activityList=cur.fetchall()
#     return render_template('welcome.html', genreList = genreList,activityList=activityList)
#
# # @app.route("/activitysearch")
# # def activity():
# #     return render_template('searchresults.html', movieList = res)
#
# ### SEARCH FOR RECCOMMENDATONS ###
# @app.route("/search")
# def search():
#     cur = conn.cursor()
#     activity=request.args['selected_activity']
#     goodfor=request.args['group']
#     genre=request.args['genre']
#     starring=request.args['actor']
#     # cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar';""")
#     if activity!="":
#         # cur.execute("""SELECT movies.id, movies.title, movies.poster, movies.rated, movies.rating from movies join activities_movies on (activities_movies.movie_id=movies.id) join activity on (activities_movies.activity_id=acitvities.id) WHERE activities.name='%s' limit 5;"""%activity)
#         cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar';""")
#     res = cur.fetchall()
#     return render_template('searchresults.html', movieList = res)
#
# ### SEARCH FOR KNOWN MOVIE ###
# @app.route("/searchMovie")
# def searchMovie():
#     args = request.url.split('?')[1]
#     title = args.split("=")[1]
#     title = title.title()
#     title = title.replace("+", " ")
#     cur = conn.cursor()
#     cur.execute("""SELECT id, title, poster, rated FROM movies where title like '%"""+title+"""%' LIMIT 5;""")
#     res = cur.fetchall()
#     return render_template('searchresults.html', movieList = res)
#
# ### SHOW MOVIE INFORMATION ###
# @app.route("/movieInfo/<id>")
# def showMovieInfo(id):
#     cur = conn.cursor()
#     cur.execute("""SELECT id, title, poster, rated FROM movies where id = %s""", (str(id),))
#     res = cur.fetchall()
#     return render_template('getmovieinfo.html', movieInformation = res)
#
#
if __name__=='__main__':
    app.run(debug=True)
