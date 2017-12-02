from flask_wtf import FlaskForm as Form
from flask_babel import gettext
from wtforms import StringField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from .models import User, Payment


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    email = StringField('email', validators=[DataRequired()])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append(gettext(
                'This nickname has invalid characters. '
                'Please use letters, numbers, dots and underscores only.'))
            return False
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append(gettext(
                'This nickname is already in use. '
                'Please choose another one.'))
            return False
        return True


class NewPaymentForm(Form):
    payment_name = StringField('quiz_name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[Length(min=0, max=140)])

    def __init__(self, original_payment_name, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_payment_name = original_payment_name

    def validate(self):
        if not Form.validate(self):
            return False
        if self.payment_name.data == self.original_payment_name:
            return True
        # Check similarity to a nickname
        if self.payment_name.data != User.make_valid_nickname(self.payment_name.data):
            self.payment_name.errors.append(gettext(
                'This payment name has invalid characters. '
                'Please use letters, numbers, dots and underscores only.'))
            return False
        payment = Payment.query.filter_by(payment_name=self.payment_name.data).first()
        if payment:
            self.payment_name.errors.append(gettext(
                'This payment name is already in use. '
                'Please choose another one.'))
            return False
        return True


class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
