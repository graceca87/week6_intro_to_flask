from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, PostForm, LoginForm
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():   # also an endpoint
    posts = Post.query.all()
    return render_template('index.html', posts=posts)



@app.route('/signup', methods=['GET', 'POST'])
def signup():   # also an endpoint
    form = SignUpForm() # instantiate SignUpForm class
    # if the form is submitted and all the data is valid
    if form.validate_on_submit():
        print('Form has been validated! Hooray!!!')
        # each form field has a data attribute
        email = form.email.data
        username = form.username.data
        password = form.password.data
        
        # Before we add the user to the database, check to see if there is already a user with username or email
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash("A user with that username or email already exists.", "danger")
            return redirect(url_for('signup'))

        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.", "success")
        # the flash can have two parameters (message, category) in this case
        # our category is a color being added to our alert when submitting form
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)



@app.route('/create', methods=['GET', 'POST'])
@login_required
def create(): # also an endpoint
    form = PostForm() # instantiate PostForm class(module(model)) # so many ways to call it...

    if form.validate_on_submit():
        # Get the data from the form
        title = form.title.data
        body = form.body.data
        # Create new instance of Post with the form data
        new_post = Post(title=title, body=body, user_id=current_user.id)
        # flash a message saying the post was created
        flash(f'{new_post.title} has been created.', 'secondary')
        # Redirect back to home page0
        return redirect(url_for('index'))

    return render_template('createpost.html', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get username and password from form
        username = form.username.data
        password = form.password.data
        # Query the user table for a user with the same username as the form
        user = User.query.filter_by(username=username).first()

        # If the user exists and the passwrod is correct for that user
        if user is not None and user.check_password(password):
            # Log the user in with the login_user function from flask_login
            login_user(user)
            # Flash a success message
            flash(f"Welcome back {user.username}!", "success")
            # Redirect back to the home page
            return redirect(url_for('index'))
        # If no user with username or password incorrect
        else:
            # flash a danger message
            flash('Incorrect username and/or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'primary')
    return redirect(url_for('index'))



@app.route('/posts/<post_id>') # angle brackets means whatever inside is variable
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post_to_edit = Post.query.get_or_404(post_id)

    # make sure the post to edit is owned by the current user
    if post_to_edit.author != current_user:
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('view_post', post_id=post_id))
    form = PostForm()
    if form.validate_on_submit():
        # Get the form data
        title = form.title.data
        body = form.body.data
        # update the post with data from the form
        post_to_edit.update(title=title, body=body)
        flash(f"{post_to_edit.title} has been updated", "success")
        return redirect(url_for('view_post', post_id=post_id))

    return render_template('edit_post.html', post=post_to_edit, form=form)



@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    if post_to_delete.author != current_user:
        flash("You do not have persmission to delete this post", "danger")
        return redirect(url_for('index'))
    # delete the post
    post_to_delete.delete()
    flash(f"{post_to_delete.title} has been deleted", "info")
    # post_to_edit is still in the scope and can be used after the delete() method
    # is called, when this function is over then it will be deleted forever
    return redirect(url_for('index'))
