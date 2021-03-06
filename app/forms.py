from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required

class LoginForm(Form):
    start = TextField('Start:', validators = [Required()])
    #openid = TextField('openid', validators = [Required()])
    end = TextField('End:', validators = [Required()])
    
    place = SelectField('Stop on the way:', choices = [('restaurant','Restaurant'),('gas','Gas station'),('hotel','Hotel'),('drug','Pharmacy')])
    partroute=SelectField('When to stop:', choices = [('middle','middle'),('beginning','beginning'),('end','end')],default=('middle','middle'))
    remember_me = BooleanField('remember_me', default = False)
