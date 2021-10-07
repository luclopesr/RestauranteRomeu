from flask import Flask, render_template, redirect
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import DateField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields.html5 import DateField, TimeField

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/reservas'
app.config['SECRET_KEY'] = 'Arrozbom'

db = SQLAlchemy(app)

class Reserva(db.Model):
    name = db.Column(db.String(80))
    email = db.Column(db.String(100), primary_key = True) 
    date = db.Column(db.String(10))
    hora = db.Column(db.String(5))
    qtd_pessoas = db.Column(db.Integer)
    mesa = db.Column(db.Integer)

class ReservaForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    date = DateField("Data", validators=[DataRequired()], format='%Y-%m-%d')
    hora = TimeField("Horário", validators=[DataRequired()], format='%H:%M')
    qtd_pessoas = IntegerField("N° de Pessoas", validators=[DataRequired()])
    mesa = IntegerField("N° da Mesa", validators=[DataRequired()]) 
    submit = SubmitField("Enviar")

@app.route('/name', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def cadastro():
    form = ReservaForm()
    
    if form.validate_on_submit():
        new_name = Reserva(name=form.name.data, email=form.email.data, date=form.date.data, hora=form.hora.data, qtd_pessoas=form.qtd_pessoas.data, mesa=form.mesa.data)
        db.session.add(new_name)
        db.session.commit()
        return redirect(url_for('cadastro'))
    return render_template("name.html", form = form)
    