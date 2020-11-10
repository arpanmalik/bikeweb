from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from bikeweb.application import RegistrationForm, LoginForm, RefistrationAsUser, BulletItems
import requests
from bs4 import BeautifulSoup
import smtplib
import os
from datetime import datetime
from bikeweb import app, db, bcrypt
from bikeweb.models import Applicant, User
from flask_login import login_user, current_user, logout_user, login_required
import time
from sqlalchemy import column
from sqlalchemy.dialects.postgresql import insert
#from bikeweb import app

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager





@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        applicant = Applicant(username=form.username.data, firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, phone=form.phone.data, address=form.address.data, password=hashed_pwd)
        db.session.add(applicant)
        db.session.commit()
        flash("Account createf has been created !", "success")
        return redirect(url_for("home"))
    return render_template("register.html",form=form)

@app.route("/registerasuser", methods=['GET','POST'])
def registration_as_user():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RefistrationAsUser()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("Account createf has been created !", "success")
        return redirect(url_for("home"))
    return render_template("registerasuser.html",form=form)


@app.route("/signin", methods=['GET','POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    global form
    form = LoginForm()
    if form.validate_on_submit():
        user = Applicant.query.filter_by(email=form.email.data).first()
        #user = User.query.filter_by(email=form.email.data).first()
        if  user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            #return render_template('choice.html')
            return redirect(url_for('bikes'))
        else:
            return redirect(url_for('signin'))
    return render_template("signin.html",form=form)
'''
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    global form
    form = LoginForm()
    if form.validate_on_submit():
        #user = Applicant.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            #return render_template('choice.html')
            return redirect(url_for('bikes'))
        else:
            return redirect(url_for('login'))
    return render_template("login.html",form=form)
'''
@app.route("/bikes",methods=['GET','POST'])
def bikes():
    return render_template("bikes.html")

@app.route("/policy", methods=['GET','POST'])
def policy():
    form = LoginForm()
    data = Applicant.query.filter_by(email=form.email.data)
    return render_template("policy.html",data=data)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/review")
#@login_required
def review():
    if current_user.is_authenticated:
        name = current_user.username
        return render_template("review.html",name=name)
    return redirect(url_for("home"))

@app.route("/royal-enfield",methods=['GET','POST'])
def royal_enfield():
    global weight_gen
    url = "https://www.bikewale.com/royalenfield-bikes/classic"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    #cc = soup.find(id="key-specs-list").find("li").get_text()
    #bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    #weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)

    url = "https://www.bikewale.com/royalenfield-bikes/bullet"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price2 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()


    url = "https://www.bikewale.com/royalenfield-bikes/himalayan"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    price3 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/royalenfield-bikes/meteor-350"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    price4 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/royalenfield-bikes/continental-gt"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    price5 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/royalenfield-bikes/interceptor"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    price6 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    bike_name = ""
    form = BulletItems()
    if form.validate_on_submit():
        bike_name = form.item.data
        url = "https://www.bikewale.com/royalenfield-bikes/" + bike_name
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
        price_gen = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
        cc_gen = soup.find(id="key-specs-list").find("li").get_text()
        bhp_gen = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
        if(bike_name == "meteor-350"):
            weight_gen = ""
        else:
            weight_gen = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
        return render_template("bullet.html",form=form,price_gen=price_gen,cc_gen=cc_gen,bhp_gen=bhp_gen,weight_gen=weight_gen)


    return render_template("royalenfield.html",form=form,price=price,price2=price2,price3=price3,price4=price4,price5=price5,price6=price6)

@app.route("/classic",methods=['GET','POST'])
def classic():
    url = "https://www.bikewale.com/royalenfield-bikes/classic"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("classic.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/bullet",methods=['GET','POST'])
def bullet():
    url = "https://www.bikewale.com/royalenfield-bikes/bullet"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("bullet.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/himalayan",methods=['GET','POST'])
def himalayan():
    url = "https://www.bikewale.com/royalenfield-bikes/himalayan"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("himalayan.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/meteor",methods=['GET','POST'])
def meteor():
    url = "https://www.bikewale.com/royalenfield-bikes/meteor-350"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    #weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("meteor.html",price=price,cc=cc,bhp=bhp,wt=191)


@app.route("/hero",methods=['GET','POST'])
def hero():
    url = "https://www.bikewale.com/hero-bikes/splendor-plus"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/hero-bikes/passion-pro"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price2 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/hero-bikes/hf-deluxe"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price3 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/hero-bikes/super-splendor"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price4 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/hero-bikes/glamour"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price5 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/hero-bikes/xtreme"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price6 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    return render_template("hero.html",price=price,price2=price2,price3=price3,price4=price4,price5=price5,price6=price6)

@app.route("/splendorplus",methods=['GET','POST'])
def splendor_plus():
    url = "https://www.bikewale.com/hero-bikes/splendor-plus"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("splendorplus.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/passionpro",methods=['GET','POST'])
def passion_pro():
    url = "https://www.bikewale.com/hero-bikes/passion-pro"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("passionpro.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/hfdeluxe",methods=['GET','POST'])
def hf_deluxe():
    url = "https://www.bikewale.com/hero-bikes/hf-deluxe"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("hfdeluxe.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/supersplendor",methods=['GET','POST'])
def super_splendor():
    url = "https://www.bikewale.com/hero-bikes/super-splendor"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("supersplendor.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/honda",methods=['GET','POST'])
def honda():
    url = "https://www.bikewale.com/honda-bikes/sp-125"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/honda-bikes/shine"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price2 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/honda-bikes/hornet"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price3 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/honda-bikes/unicorn"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price4 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/honda-bikes/hness-cb350"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price5 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/honda-bikes/livo"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price6 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    return render_template("honda.html",price=price,price2=price2,price3=price3,price4=price4,price5=price5,price6=price6)


@app.route("/hondasp",methods=['GET','POST'])
def hondasp():
    url = "https://www.bikewale.com/honda-bikes/sp-125"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("hondasp.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/shine",methods=['GET','POST'])
def shine():
    url = "https://www.bikewale.com/honda-bikes/shine"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("shine.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/hornet",methods=['GET','POST'])
def hornet():
    url = "https://www.bikewale.com/honda-bikes/hornet"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("hornet.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/unicorn",methods=['GET','POST'])
def unicorn():
    url = "https://www.bikewale.com/honda-bikes/unicorn"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("unicorn.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/yamaha",methods=['GET','POST'])
def yamaha():
    url = "https://www.bikewale.com/yamaha-bikes/fz-s"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/yamaha-bikes/yzf-r15"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price2 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/yamaha-bikes/mt-15"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price3 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()

    url = "https://www.bikewale.com/yamaha-bikes/fz25"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price4 = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()


    return render_template("yamaha.html",price=price,price2=price2,price3=price3,price4=price4)

@app.route("/fzs",methods=['GET','POST'])
def fzs():
    url = "https://www.bikewale.com/yamaha-bikes/fz-s"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("fzs.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/yzf",methods=['GET','POST'])
def yzf():
    url = "https://www.bikewale.com/yamaha-bikes/yzf-r15"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("yzf.html",price=price,cc=cc,bhp=bhp,wt=weight)

@app.route("/mt15",methods=['GET','POST'])
def mt():
    url = "https://www.bikewale.com/yamaha-bikes/mt-15"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # img = soup.find(class_="bw-tabs-data connected-carousels carousel-controls")
    price = soup.find(class_="model-price-content padding-top5").find(id="new-bike-price").get_text()
    cc = soup.find(id="key-specs-list").find("li").get_text()
    bhp = soup.find(id="key-specs-list").find("li").next_sibling.get_text()
    weight = soup.find(id="key-specs-list").find("li").next_sibling.next_sibling.get_text()
    #print(cc)
    return render_template("mt.15html",price=price,cc=cc,bhp=bhp,wt=weight)











