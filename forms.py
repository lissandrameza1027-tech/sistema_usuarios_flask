from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models.user import User

class RegisterForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[
            DataRequired(),
            Length(min=3, max=80)
        ]
    )
    email = StringField(
        'Correo Electrónico',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    confirm_password = PasswordField(
        'Confirmar Contraseña',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Registrarse')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('El nombre de usuario ya está registrado.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('El correo electrónico ya está registrado.')

class LoginForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired()]
    )
    submit = SubmitField('Iniciar Sesión')

class EditProfileForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[
            DataRequired(),
            Length(min=3, max=80)
        ]
    )
    email = StringField(
        'Correo Electrónico',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    submit = SubmitField('Guardar Cambios')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, field):
        if field.data != self.original_username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('El nombre de usuario ya está en uso.')

    def validate_email(self, field):
        if field.data != self.original_email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('El correo electrónico ya está en uso.')