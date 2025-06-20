"""
A Blueprint is a way to organize a group of related views and other code. 
Rather than registering views and other code directly with an application, 
they are registered with a blueprint. Then the blueprint is registered with 
the application when it is available in the factory function.

Flaskr will have two blueprints, 
- one for authentication functions and 
- one for the blog posts functions. 

The code for each blueprint will go in a separate module. 
Since the blog needs to know about authentication, 
you'll write the authentication one first.
"""


import functools

from flask import (Blueprint,
                   flash,
                   g,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for
)

from werkzeug.security import (check_password_hash, 
                               generate_password_hash
)

from flaskr.db import get_db



bp = Blueprint('auth', __name__, url_prefix='/auth')


# the first VIEW register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
            
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)
        
    return render_template('auth/register.html')


# Login VIEW
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
        
    return render_template('auth/login.html')


# Now that the user’s id is stored in the session, 
# it will be available on subsequent requests. 
# At the beginning of each request, 
# if a user is logged in their information should be 
# loaded and made available to other views.

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
# logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


## require authentication in othwe views
# Creating, editing, and deleting blog posts will require a user to be logged in. 
# A decorator can be used to check this for each view it's applied to.

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view


