import os
import time
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    entrys = db.execute("SELECT * FROM diary").fetchall()
    return render_template("index.html", entrys=entrys)

@app.route("/entry",methods=["POST"])
def entry():
    id=request.form.get('entry_id')
    content=db.execute("SELECT * FROM diary WHERE id=:id", {"id":id})
    for con in content:
        return render_template("entry.html",content=con)


@app.route("/add",methods=["POST"])
def add():
    Date=time.strftime('%Y%m%d')
    title=request.form.get('title')
    content=request.form.get('content')
    if title != '' and content !='':
        db.execute("insert into diary(date,title,content) values(:date,:title,:content)",{"date":Date,"title":title,"content":content})
        db.commit()
        return render_template("error.html",message=' Your entry was added Sucessfully ')
    else:
        return render_template("error.html",message=' You might have entered blank fields ')

@app.route("/entrys/<string:headin>")
def entrys(headin):
    res=db.execute("select * from diary where title=:title",{'title':headin}).fetchall()
    for content in res:
        return render_template("entry.html",content=content)

#@app.route("/admin")
#def admin():
#    sql = request.form.get('sql')
#    if sql is None:
 #       return render_template("admin.html")
  #  else:
   #     res db.execute(sql)

