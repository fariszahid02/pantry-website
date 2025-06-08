# Authored by: Yat Nam
# view functions for user pages
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from users.forms import RegisterForm, LoginForm, ChangePasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User

users_blueprint = Blueprint('users', __name__, template_folder='templates')



@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    from app import create_app

    app = create_app()
    # Create signup form object
    form1 = RegisterForm()

    # If request method is POST or form is valid
    if form1.validate_on_submit():
        with app.app_context():
            u1 = User.query.filter_by(email=form1.email.data).first()
        # If this returns a user, then the email already exists in database

        # If email already exists redirect user back to signup page with error message so user can try again
        if u1:
            flash('Email address already exists')
            return render_template('user/register.html', form=form1)

        # Create a new user with the form data
        new_user = User(email=form1.email.data,
                        dob=form1.dob.data,
                        first_name=form1.first_name.data,
                        last_name=form1.last_name.data,
                        password=form1.password.data,
                        role='user'
                        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        app.logger.info(f"User registered: {form1.email.data}, IP: {request.remote_addr}")
        # Sends user to login page
        return redirect(url_for('users.login'))
    # If request method is GET or form not valid re-render signup page
    return render_template('user/register.html', form=form1)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    from app import create_app
    app = create_app()

    # Create login form object
    form = LoginForm(request.form)

    # If request method is POST and form is valid
    if request.method == 'POST' and form.validate_on_submit():
        user: User = User.query.filter_by(email=form.email.data).first()

        # Verify the user's password
        if user and user.verify_password(form.password.data):
            login_user(user)

            # Update user login details
            user.last_login = user.current_login
            user.current_login = datetime.utcnow()
            user.last_login_ip = user.current_login_ip or request.remote_addr
            user.current_login_ip = request.remote_addr
            user.total_logins += 1
            user.update_security_fields_on_login(ip_addr=request.remote_addr)  # Update security login fields.
            db.session.commit()

            # Set session variables
            session['logged_in'] = True
            session['user_id'] = user.id

            app.logger.info(
                f"User logged in: {form.email.data}, IP: {request.remote_addr}")
            flash('You have been logged in.', 'success')

            # Redirect to admin page if user is an admin
            if user.role == 'admin':
                return redirect(url_for('admin.admin'))
            return redirect(url_for('baseLogin'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('user/login.html', form=form)


@users_blueprint.route('/my_account')
def information():
    # Render the account information page for the current user
    return render_template('user/my_account.html', user=current_user)


@users_blueprint.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    # Create change password form object
    form = ChangePasswordForm()

    # If form is valid
    if form.validate_on_submit():
        user = current_user

        # Verify the current password
        if user.verify_password(form.current_password.data):
            if form.new_password.data != form.current_password.data:

                # Set the new password
                user.set_password(form.new_password.data)
                db.session.commit()
                flash('Your password has been updated.', 'success')
                return redirect(url_for('users.login'))
            else:
                flash('New password cannot be the same as the current password.', 'error')
        else:
            flash('Current password is incorrect.', 'error')
    return render_template('user/update_password.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    from app import create_app
    app = create_app()

    # Log out the user and update the session
    user_info = f"User logged out: {current_user.email}, IP: {request.remote_addr}"
    logout_user()
    session['logged_in'] = False
    app.logger.info(user_info)

    # Redirect to the home page
    return redirect(url_for('home'))
