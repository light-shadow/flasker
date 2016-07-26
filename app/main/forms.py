# coding: utf-8
from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class NameForm(Form):
    name = StringField(u'您的名字', validators=[Required()])
    submit = SubmitField('提交')


class EditProfileForm(Form):
    name = StringField(u'您的真实姓名', validators=[Length(0, 64)])
    location = StringField(u'位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于自己')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名只能包含字母, '
                                          u'数字，点和下划线')])
    confirmed = BooleanField(u'确认')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于自己')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被人注册了，：（')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名不可用！')


class PostForm(Form):
    body = PageDownField(u"此刻什么萦绕你的心头，把她写下来吧！", validators=[Required()])
    submit = SubmitField(u'提交')


class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField(u'提交')
