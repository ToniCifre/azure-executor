from container import app, db
from container.models.user import User

from flask import Flask, render_template, request, jsonify, redirect
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route('/toni', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        return jsonify(result="okay", probability="por_los_dos_lados")

    return render_template("error/404.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and user.check_password(request.form['password']):
            if not user.confirmed:
                return render_template('login.html', error="Wait to be validated")
            login_user(user)
            flash('LOGGED in Succesfully')

            next = request.args.get('next')

            if next is None:
                next = '/'
            return redirect(next)

        return render_template('login.html', error="Bad credentials")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None:
            return render_template('signup.html', error="Logical error")
        user_data = User(email=request.form['email'], password=request.form['password'])
        db.session.add(user_data)
        db.session.commit()
        flash('Thanks for registering, you can proceed...')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
