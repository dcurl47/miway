from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required

class LoginForm(Form):
    start = TextField('start', validators = [Required()])
    #openid = TextField('openid', validators = [Required()])
    end = TextField('end', validators = [Required()])
    place = SelectField('place', choices=[('restaurant','Restaurant'),('gas station'),('hotel')],default= ('restaurant'))
    place = SelectField('stops', choices = [('restaurant','Restaurant'),('gas','Gas station'),('hist_site','Historical Site')])
    remember_me = BooleanField('remember_me', default = False)
