from functools import wraps
from flask import render_template, redirect, url_for, flash, session, request
from routes import user_bp
from models import db
from models.user import User
from forms import RegisterForm, LoginForm, EditProfileForm

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('user_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('user_bp.user_list'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('user_bp.login'))
    return render_template('register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('user_bp.user_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Bienvenido de nuevo, {user.username}.', 'success')
            return redirect(url_for('user_bp.user_list'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('user_bp.login'))

@user_bp.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)

@user_bp.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    form = EditProfileForm(original_username=user.username, original_email=user.email)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        if session.get('user_id') == user.id:
            session['username'] = user.username
        flash('Perfil actualizado con éxito.', 'success')
        return redirect(url_for('user_bp.profile', id=user.id))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    return render_template('edit_profile.html', form=form, user=user)

@user_bp.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    is_current_user = (session.get('user_id') == user.id)
    db.session.delete(user)
    db.session.commit()
    if is_current_user:
        session.pop('user_id', None)
        session.pop('username', None)
        flash('Tu cuenta ha sido eliminada.', 'info')
        return redirect(url_for('user_bp.register'))
    flash('Usuario eliminado con éxito.', 'success')
    return redirect(url_for('user_bp.user_list'))