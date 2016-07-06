# coding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'让我保持登录状态')
    submit = SubmitField(u'登录')


class RegistrationForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'密码只能包含字母, '
                                          u'数字, 点和下划线')])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message=u'密码前后必须一致！')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册过了,:(')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被注册过了,:(')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'原密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message=u'密码前后必须一致！')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('更换密码')


class PasswordResetRequestForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重置邮箱')


class PasswordResetForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message=u'密码前后必须一致！')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('此邮箱未注册！')


class ChangeEmailForm(Form):
    email = StringField(u'新邮箱', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'更新邮箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册了:(')
