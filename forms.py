from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, FileField, FloatField,BooleanField,SelectField, SubmitField
from wtforms.validators import DataRequired, length, DataRequired, Email

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=8, max=16)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    remember = BooleanField("Remember me")

class ProductForm(FlaskForm):
    name = StringField("Name")
    description = StringField("Description")
    price = FloatField("Price")
    img = FileField("Choose product's Image", validators=[FileAllowed(["png", "jpeg", "jpg", "webp"])])
    category = SelectField("Category", choices=[
        ("motherboard", "Motherboard"),
        ("cpu", "CPU"),
        ("cpucooler", "CPU Cooler"),
        ("ram", "RAM"),
        ("gpu", "GPU"),
        ("psu", "PSU"),
        ("hdd", "HDD"),
        ("ssd", "SSD"),
        ("m2", "M.2"),
        ("cases", "Cases"),
        ("casefan", "Case Fans")
    ])
    submit = SubmitField("Submit")