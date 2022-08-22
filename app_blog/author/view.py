from app_blog import app,db
from flask import render_template,flash,url_for,redirect
from app_blog.author.model import UserRegister
from app_blog.author.form import FormRegister
#from app_blog.sendmail import send_mail
from app_blog.author.email import send_email
from flask_login import current_user, login_required,login_user
from app_blog.author.tokens import generate_confirmation_token,confirm_token
import datetime

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegister()

    if form.validate_on_submit():
        
        user = UserRegister(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            confirmed=False
        )
        db.session.add(user)
        
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('author/mail/activate.html', confirm_url=confirm_url)
        subject = "來自新寶島的愛"
        send_email(user.email, subject, html)
        login_user(user)
        '''
        msg_title = 'Hello It is Flask-Mail'
        #  寄件者，若參數有設置就不需再另外設置
        msg_sender = 'sean940106@gmail.com'
        #  收件者，格式為list，否則報錯
        msg_recipients = ['AFD3456789LE@gmail.com']
        #  郵件內容
        #msg_body = 'Hey, I am mail body!'
        
        send_mail(sender=msg_sender,
                recipients=msg_recipients,
                subject=msg_title, 
                #template='sendmailtest', 
                user=user,
                token=token
                )
        
        '''
        return '<font size="7">去驗證信箱RA</font>'


        
        
    return render_template('author/register.html', form=form)


@app.route('/register/<token>')
#@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('NTM也拖太久了，都多久了才來驗證，給我重來', 'danger')
    user = UserRegister.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('已經驗證了，去登入阿匪類', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return render_template('author/mail/welcome.html')


