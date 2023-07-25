from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBRsuYl7S92TFNLFI7Sm9OHBAR-h_FGCVw",
  "authDomain": "afu-khoury.firebaseapp.com",
  "projectId": "afu-khoury",
  "storageBucket": "afu-khoury.appspot.com",
  "messagingSenderId": "821050514392",
  "appId": "1:821050514392:web:c91cf121ccb9d8c161b0ad",
  "databaseURL":"https://afu-khoury-default-rtdb.europe-west1.firebasedatabase.app/"
}
fireBase = pyrebase.initialize_app(config)
auth = fireBase.auth()
db = fireBase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        username = request.form['username']
        bio = request.form['bio']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email": email, "name" : name, "username" : username, "bio" : bio}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
           error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            tweet = {"title": title,"text": text}
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))

        except:
            print("Couldn't add a tweet")
    return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    auth.current_user = None
    login_session['user'] = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("all_tweets.html", tweets = tweets)



if __name__ == '__main__':
    app.run(debug=True)