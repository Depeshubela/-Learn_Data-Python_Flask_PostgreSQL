from app_blog import app,db,bcrypt
from flask import render_template,flash,url_for,  redirect,  request
from app_blog.author.model import UserRegister
from app_blog.author.form import FormRegister,FormLogin, FormChangePWD,FormResetMail,FormResetPassword
from app_blog.author.email import send_email
from flask_login import current_user, login_required,login_user,logout_user
from app_blog.author.tokens import generate_confirmation_token,confirm_token,reset_token
import datetime,time

#註冊介面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
        subject = "Please confirm your email"
        send_email(user.email, subject, html)
        login_user(user)
        return '<br><br><br><br><br><br><br><br><center><font size="7">去驗證信箱RA</font></center>'


        
        
    return render_template('author/register.html', form=form)





#驗證信連結點擊後
@app.route('/register/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = UserRegister.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))

#登入介面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = FormLogin()
    if form.validate_on_submit():
        #  當使用者按下login之後，先檢核帳號是否存在系統內。
        user = UserRegister.query.filter_by(email=form.email.data).first()
        if user:
            #  當使用者存在資料庫內再核對密碼是否正確。
            if user.check_password(form.password.data):

                #  加入參數『記得我』
                login_user(user, form.remember_me.data)
                #  使用者登入之後，將使用者導回來源url。
                #  利用request來取得參數next
                next = request.args.get('next')
                #  自定義一個驗證的function來確認使用者是否確實有該url的權限
                if not next_is_valid(next):
                    #  如果使用者沒有該url權限，那就reject掉。
                    return 'Bad Boy!!'
                return redirect(next or url_for('index'))
                # return 'Welcome' + current_user.username
                
            else:
                #  如果密碼驗證錯誤，就顯示錯誤訊息。
                flash('Wrong Email or Password')
        else:
            #  如果資料庫無此帳號，就顯示錯誤訊息。
            flash('Wrong Email or Password')
    return render_template('author/login.html', form=form)
                
#  加入function
def next_is_valid(url):
    """
    為了避免被重新定向的url攻擊，必需先確認該名使用者是否有相關的權限，
    舉例來說，如果使用者調用了一個刪除所有資料的uri，那就GG了，是吧 。
    :param url: 重新定向的網址
    :return: boolean
    """
    return True

#登入後頁面， @login_required使未登入引導至login
@app.route('/') 
@login_required  
def index():  
    return 'Hello Welcome My HomePage'

#登出介面
@app.route('/logout') #登出
@login_required 
def logout():
    logout_user()
    flash('Log Out See You.')
    return redirect(url_for('login'))



#測試flash
@app.route('/test')  
def test_index():  
    flash('flash-1')  
    flash('flash-2')  
    flash('flash-3')  
    return render_template('base.html')

#測試
@app.route('/userinfo')  
def userinfo():  
    return 'Here is userinfo'

#如果未驗證帳號操作會被此攔截要求驗證
@app.before_request
def before_request(): 
    """
    在使用者登入之後，需做一個帳號是否啟動的驗證，啟動之後才能向下展開相關的應用。
    條件一：需登入
    條件二：未啟動
    條件三：endpoint不等於static，這是避免靜態資源的取用異常，如icon、js、css等..
    :return:
    """
    if (current_user.is_authenticated and
            not current_user.confirmed and #登入但未確認
            request.endpoint not in ['re_userconfirm', 'logout', 'user_confirm','reset_password','confirm_email','register'] and #例外清單
            request.endpoint != 'static'):
        #  條件滿足就引導至未啟動說明
        flash('Hi, please activate your account first. Your endpoint:%s' % request.endpoint)
        return render_template('author/unactivate.html')

#重新寄送驗證信
@app.route('/reusreconfirm')
@login_required
def re_userconfirm():
    """
    當使用者點擊重新寄送的時候就引導到這個route
    因為已經使用current_user綁定user了，所以可以直接透過current_user使用user的相關方法
    重新寄送啟動信件必需要登入狀態
    :return:
    """

    #  產生用戶認證令牌
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('author/mail/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('Please Check Your Email..')
    return redirect(url_for('index'))

#更換密碼
@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = FormChangePWD()
    if form.validate_on_submit():
        #  透過current_user來使用密碼認證，確認是否與現在的密碼相同
        if current_user.check_password(form.password_old.data) == current_user.check_password(form.password_new.data):
            flash('The old and new passwords cannot be the same')
        elif current_user.check_password(form.password_old.data):
            current_user.password = form.password_new.data
            db.session.add(current_user)
            db.session.commit()
            flash('You Have Already Change Your Password, Please Login Again.')
            time.sleep(2)
            return redirect(url_for('logout'))
        else:
            flash('Wrong Old Password...')
    return render_template('author/changepassword.html', form=form)

#找回密碼
@app.route('/resetpassword', methods=['GET', 'POST'])
def reset_password():
    #  只允許未登入的匿名帳號可以申請遺失密碼
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = FormResetMail()
    if form.validate_on_submit():
        #  取得使用者資料
        user = UserRegister.query.filter_by(email=form.email.data).first()
        if user:
            #  產生一個token
            #  產生用戶認證令牌
            token = confirm_token(user)
            confirm_url = url_for('reset_password_recive', token=token, _external=True)
            html = render_template('author/mail/resetmail.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
            flash('Please Check Your Email. Then Click link to Reset Password')
            #  寄出之後將使用者導回login，並且送出flash message
            return redirect(url_for('login'))
    return render_template('author/resetemail.html', form=form)

#透過找回密碼驗證信連至此
@app.route('/resetpassword/<token>', methods=['GET', 'POST'])
def reset_password_recive(token):
    """使用者透過申請連結進來之後，輸入新的密碼設置，接著要驗證token是否過期以及是否確實有其user存在
    這邊使用者並沒有登入，所以記得不要很順手的使用current_user了。
    """
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    form = FormResetPassword()

    if form.validate_on_submit():
        user = UserRegister()
        data = reset_token(token)
        if data:
            #  如果未來有需求的話，還要確認使用者是否被停權了。
            #  如果是被停權的使用者，應該要先申請復權。
            #  下面注意，複製過來的話記得改一下id的取得是reset_id，不是user_id
            user = UserRegister.query.filter_by(id=data.get('user_id')).first()

            
            print(bcrypt.check_password_hash(user.password_hash,form.password.data))
            print(data)
            print(token)
            
            print(UserRegister.query.filter_by(id=1).first())

            #  再驗證一次是否確實的取得使用者資料
            if not bcrypt.check_password_hash(user.password_hash,form.password.data):
                user.password = form.password.data
                db.session.commit()
                flash('Sucess Reset Your Password, Please Login')
                return redirect(url_for('login'))
            else:
                flash('The old and new passwords cannot be the same')
        else:
            flash('Worng token, maybe it is over 24 hour, please apply again')
            return redirect(url_for('login'))
    return render_template('author/resetpassword.html', form=form)
