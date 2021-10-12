from flask import Flask, render_template, redirect, url_for, request, session, flash

from Utils.LoggerUtil import LoggerUtil
from Core.UserAuthentication import UserAuthentication
from Core.UserRegistration import UserRegistration
from Core.UpdateProfile import UpdateProfile

log = LoggerUtil(__name__).get()
auth = UserAuthentication()
reg = UserRegistration()
update1 = UpdateProfile()
#cabReq = PostCabReq()

app = Flask(__name__)

from Core.PostCabReq import PostCabReq
cabReq = PostCabReq()
@app.route('/post_cab_req', methods=['GET'])
def post_cab_req():
   cabReq.post_request()
   return ''

@app.route('/index', methods=['GET'])
def hello():
    return 'Welcome to cab sharing site :)'


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        is_username_available = auth.is_username_available(username=email)
        if is_username_available:
            reg.add_user(name=name, email=email, contact=contact, password=password)
            return redirect(url_for('login'))
        else:
            error = 'Email id is already taken. Please login'
    return render_template('registration.html', error=error)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/offer_ride_form', methods=['GET'])
def offer_ride_form():
    return render_template('update.html')


@app.route('/login_method', methods=['POST'])
def login_page():
    error = None
    if request.method == 'POST':

        email_id = request.form['email_id']
        password = request.form['password']
        import ipdb; ipdb.set_trace()
        is_existing_user = auth.check_in_db(email_id, password)
        if is_existing_user:
            session['logged_in'] = True
            flash('You were successfully logged in')
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('logged_out.html')


@app.route('/update', methods=['POST'])
def update():
    print('date0000', request.form['date'])
    print('hey emailllllllllllllllll', request.form['hour'] + ':' + request.form['hour'])
    try:
        # If session alive then use this method. else redirect to login.
        source = request.form['source']
        destination = request.form['destination']
        time = request.form['hour'] + ':' + request.form['minute']
        date = request.form['date']
        num_seats_req = request.form['num_seats_req']
        # Contact details. If any value
        phone_num = request.form['phone_num']
        email = request.form['email']
        # Below is a text field. If any value
        print("before update")
        update1.update(source=source, destination= destination, time= time, date= date, num_seats_req= num_seats_req, phone_num= phone_num, email= email)
        return redirect(url_for('home'))
    except Exception as e:
        print('errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr0',e)
        error = e
    return render_template('update.html', error=error)


@app.route('/post', methods=['POST'])
def post():
    try:
        pass
    except Exception as e:
        error = e
    return render_template('post.html', error=error)


if __name__ == '__main__':
    app.run()
