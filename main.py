from flask import Flask, render_template, url_for, redirect, flash, abort, request
from smtplib import SMTP
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_user, logout_user, login_required
from models import db, User, Project
from http import HTTPStatus
from email.message import EmailMessage
from twilio.rest import Client
from forms import *
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]

db.init_app(app)

with app.app_context():
    db.create_all()

Bootstrap5(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)




@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

def get_all_projects(): 
    return db.session.execute(db.select(Project).order_by(Project.date)).scalars().all()



@login_required
@app.route('/')
def index():

    return render_template(
        'index.html', 
        projects=get_all_projects(),
        title='Portfolio website'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.session.execute(db.select(User).where(User.email==email)).scalar()

        if not user or user.password != password:
            flash("Invalid email address or password!")
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('admin'))

    return render_template(
        'login.html', 
        form=LoginForm(),
        title='Login Portfolio website'
    )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():


    return render_template(
        'admin.html',
        title='Admin Portfolio website'
    )

@app.route('/project/<int:project_id>')
def project_details(project_id):
    project = db.get_or_404(Project, project_id)

    return render_template(
            'project_details.html',
            project=project,
            projects=get_all_projects(),
            title=f'{project.title} project'
    )

@app.post('/contact')
def contact():
    # send a well formatted email and message
    with SMTP('smtp.gmail.com') as connection:
        user = os.environ['SMTP_EMAIL']
        password = os.environ['SMTP_PASSWORD']
        
        connection.starttls()
        connection.login(user, password)

        customer_email = request.form.get('email')
        customer_name = request.form.get('name')
        customer_msg = request.form.get('message')

        msg = EmailMessage()

        # To customer
        msg['Subject'] = f"Thanks for reaching to us! {customer_name.title()}"
        msg['From'] = user
        msg['To'] = customer_email

        msg.set_content(
            f"""Hi {customer_name}\nThanks for reaching to me. I am committed to getting back
            to you as soon as possible. It is very wonderful to hear from you!\n\n
            Your message: {customer_msg}"""
        )

        msg.add_alternative(
            f""" <!DOCTYPE html>
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #0066cc;">Hello {customer_name.title()}!</h2>
                <p>Thanks 🙏 for reaching to me. I am committed to getting back
                to you as soon as possible. It is very wonderful to hear from you</p>
                <p>Check out the <a href="https://github.com/ChrisKabumba">my GitHub</a> to see what
                I have done in software engineer career.</p>
                <p>See you soon 👋</p>
                <p>Your message: {customer_msg}</p>
            </body>
            </html>
            """,
            subtype='html'
        )

        try:
            connection.send_message(msg)
        except:
            print("Could not send email to customer")

        msg_admin = EmailMessage()
        # To admin
        msg_admin['Subject'] = f"{customer_name.title()} wants to reach out!"
        msg_admin['From'] = user
        msg_admin['To'] = user
        
        msg_admin.set_content(
            f"""{customer_name} wants to reach to you via  the portfolio website!\n
            Email address: {customer_email}\n
            Message: {customer_msg}"""
        )
        
        msg_admin.add_alternative(
            f""" <!DOCTYPE html>
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #0066cc;">{customer_name.title()} wants to reach out!</h2>
                <p>His/her message is {customer_msg}</p>
                <p>Their email is {customer_email}</p>
                <p>Please get back to them as quickly as possible!</p>
            </body>
            </html>
            """,
            subtype='html'
        )
        try:
            connection.send_message(msg_admin)
        except:
            print("Could not send email to admin")

        # send whatsapp message to admin
        api_key = os.environ["TWILIO_API_KEY"]
        api_secret = os.environ["TWILIO_API_SECRET"]
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        sender_no = os.environ["TWILIO_SENDER_NO"]
        destination_no = os.environ["TWILIO_DESTINATION_NO"]
        client = Client(api_key, api_secret, account_sid)

        whatsapp_msg = f"""
        {customer_name.capitalize()} wants to reach!\n
        His/her message: {customer_msg}\n
        Email address: {customer_email}
        Get back as quicly as possible!
        """

        try:
            message = client.messages.create(
                from_=f"whatsapp:{sender_no}",
                to=f"whatsapp{destination_no}",
                msg=whatsapp_msg
            )

            print(message.body)
        except:
            print("Could not send message")

    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug=True)