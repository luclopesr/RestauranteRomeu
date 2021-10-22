from flask import Flask, render_template
from flask.helpers import url_for
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, EmailField
from wtforms.fields.html5 import DateField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/reserva'
app.config['SECRET_KEY'] = 'Arrozbom'

db = SQLAlchemy(app)

class Reserva(db.Model):
    name = db.Column(db.String(80))
    email = db.Column(db.String(100), primary_key = True)
    data = db.Column(db.String(10))
    horario = db.Column(db.String(8))
    qtd_pessoas = db.Column(db.Integer)
    mesa = db.Column(db.String(7))

class ReservaForm(FlaskForm):
    name = StringField("Nome: ", validators=[DataRequired()])
    email = EmailField('Email: ', [validators.DataRequired(), validators.Email()])
    data = DateField('Data: ', format='%Y-%m-%d')
    horario = SelectField('Horário: ', choices=[('12:00'), ('14:00'), ('16:00'), ('18:00'), ('20:00'), ('22:00')])
    qtd_pessoas = SelectField("N° de Pessoas: ", choices=[('1'), ('2'), ('3'), ('4'), ('5'), ('6'), ('7'), ('8'), ('9'), ('10')], validators=[DataRequired()])
    mesa = SelectField("N° da Mesa: ", choices=[('Mesa 1'), ('Mesa 2'), ('Mesa 3'), ('Mesa 4'), ('Mesa 5'), ('Mesa 6'), ('Mesa 7'), ('Mesa 8'), ('Mesa 9'), ('Mesa 10'), ('Mesa 11')], validators=[DataRequired()])
    submit = SubmitField("ENVIAR")

@app.route('/name', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def cadastro():
    form = ReservaForm()

    if form.validate_on_submit():
        validar = Reserva.query.filter_by(data = form.data.data).first()
        if validar:
            if (validar.horario == form.horario.data ) and (validar.mesa == form.mesa.data):
                return render_template("erroalert.html", form = form)
        new_reserva = Reserva(name=form.name.data, email=form.email.data, data=form.data.data, horario=form.horario.data, qtd_pessoas=form.qtd_pessoas.data, mesa=form.mesa.data)
        db.session.add(new_reserva)
        db.session.commit()
        return render_template("successalert.html", form = form)
    return render_template("name.html", form = form)
