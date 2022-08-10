from form import FormRegister
from model import UserReister
from flask_register import db,app
from flask import render_template

@app.route('/register', methods=['GET', 'POST'])
def register():

    form =FormRegister()
    if form.validate_on_submit():
        user = UserReister(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return 'Success Thank You'
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()