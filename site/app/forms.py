from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class SearchForm(Form):
    request = TextField('request', validators = [Required()])
    limit = TextField('limit', validators = [Required()])