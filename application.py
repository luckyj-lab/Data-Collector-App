from enum import unique
from flask import Flask, render_template, request 
from send_email import send_email
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

application = app = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI']='mysql://height:Hello123@aa115mww7fg5bgl.cuev94lckpjr.us-east-1.rds.amazonaws.com:3306/aa115mww7fg5bgl'
db=SQLAlchemy(application)

class Data(db.Model):
    __tablename__ = "data"
    id=db.Column(db.Integer,primary_key=True)
    email_=db.Column(db.String(120),unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email,height):
        self.email_=email
        self.height_=height


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/success", methods=['POST'])    
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height_name"]
        
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data = Data(email,height)
            db.session.add(data)
            db.session.commit()
            ave_height=db.session.query(func.avg(Data.height_)).scalar()
            ave_height=round(ave_height,2)
            count=db.session.query(Data.height_).count()
            send_email(email,height,ave_height,count)
            return render_template("success.html")
    return render_template('index.html',
    text="Seems like we've got something from that email already")

if __name__ == '__main__':
    application.debug=True
    application.run()

