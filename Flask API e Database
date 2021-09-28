from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/reservas'

db = SQLAlchemy(app)

class Reserva(db.Model):
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100), primary_key = True)
    mesa = db.Column(db.Integer, unique=True)
    data = db.Column(db.String(10), unique=True)
    hora = db.Column(db.String(5), unique=True)
    qtd_pessoas = db.Column(db.Integer)

    def to_json(self):
        return {"nome": self.nome, "email": self.email, "mesa": self.mesa,
                "data": self.data, "hora": self.hora, "qtd_pessoas": self.qtd_pessoas}

#seleciona reservas
@app.route("/reserva", methods=["GET"])
def seleciona_usuarios():
    reservas_objetos = Reserva.query.all()
    reservas_json = [reserva.to_json() for reserva in reservas_objetos]
    print(reservas_json)

    return gera_response(200, "reservas", reservas_json, "Reservas listadas")

#seleciona reserva individual
@app.route("/reserva/<email>", methods=["GET"])
def seleciona_reserva(email):
    reserva_objeto = Reserva.query.filter_by(email=email).first()
    reserva_json = reserva_objeto.to_json()

    return gera_response(200, "reserva", reserva_json)   

#cadastro
@app.route("/reserva", methods=["POST"])
def cria_reserva():

    body = request.get_json()

    if("nome" not in body):
        return gera_response(400, "O parâmetro nome é obrigatório!")

    if("email" not in body):
        return gera_response(400, "O parâmetro email é obrigatório!")

    if("data" not in body):
        return gera_response(400, "O parâmetro data é obrigatório!")

    if("hora" not in body):
        return gera_response(400, "O parâmetro hora é obrigatório!")
    
    if("qtd_pessoas" not in body):
        return gera_response(400, "O parâmetro qtd_pessoas é obrigatório!")
    
    if("mesa" not in body):
        return gera_response(400, "O parâmetro mesa é obrigatório!")

    reserva = Reserva(nome=body["nome"], email=body["email"], mesa=body["mesa"], data=body["data"], 
                          hora=body["hora"], qtd_pessoas=body["qtd_pessoas"])
    db.session.add(reserva)
    db.session.commit()
    return gera_response(201, "reserva", reserva.to_json(), "Reserva realizada!")
    
# Atualizar reserva
@app.route("/reserva/<email>", methods=["PUT"])
def atualiza_reserva(email):
    #pega a reserva
    reserva_objeto = Reserva.query.filter_by(email=email).first()
    #pega as modificações
    body = request.get_json()

    try:
        if('nome' in body):
            reserva_objeto.nome = body['nome']
        if('mesa' in body):
            reserva_objeto.mesa = body['mesa']
        if('data' in body):
            reserva_objeto.data = body['data']
        if('hora' in body):
            reserva_objeto.hora = body['hora']
        if('qtd_pessoas' in body):
            reserva_objeto.qtd_pessoas = body['qtd_pessoas']

        db.session.add(reserva_objeto)
        db.session.commit()
        return gera_response(200, "reserva", reserva_objeto.to_json(), "Atualizado com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "reserva", {}, "Erro ao atualizar!")

#Deleta reserva
@app.route("/reserva/<email>", methods=["DELETE"])
def deleta_usuario(email):
    reserva_objeto = Reserva.query.filter_by(email=email).first()

    try:
        db.session.delete(reserva_objeto)
        db.session.commit()
        return gera_response(200, "reserva", reserva_objeto.to_json(), "Deletado com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "reserva", {}, "Erro ao deletar!")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

app.run()
