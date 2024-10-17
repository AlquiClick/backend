from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class MarcaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Guardar')
