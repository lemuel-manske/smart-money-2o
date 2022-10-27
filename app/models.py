from calendar import month
from datetime import timedelta
from enum import Enum

from sqlalchemy.sql import func

from app import db
from app.utils.choices import Instituicoes, Moedas, TipoTransacao


def get_val(self, field):
	v = self.__getattribute__(field)

	if issubclass(type(v), Enum):
		return v.name
	else:
		return v

def to_json(*fields):
	return lambda self: { 
		field: get_val(self, field) for field in fields 
	}

class Usuario(db.Model):
	__tablename__ = 'usuario'

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.Text, nullable=False)
	email = db.Column(db.Text, nullable=False, unique=True)
	senha = db.Column(db.Text, nullable=False)
	premium = db.Column(db.Boolean, nullable=False, default=False) # True | False

	contas_bancarias = db.relationship('ContaBancaria', backref='usuario', lazy='select')

	json = to_json('id', 'nome', 'email', 'senha', 'premium')	

	def __str__(self):
		return f'<Usuario: id:{self.id}, nome:{self.name}, email:{self.email}, \
			senha:{self.password}, premium:{self.premium}>'


class ContaBancaria(db.Model):
	__tablename__ = 'conta_bancaria'

	id = db.Column(db.Integer, primary_key=True)
	moeda = db.Column(db.Enum(Moedas), nullable=False, default=(Moedas.BRAZIL))
	saldo = db.Column(db.Numeric, nullable=False)
	instituicao = db.Column(db.Enum(Instituicoes), nullable=False)

	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

	despesas = db.relationship('Transacao', backref='conta_bancaria', lazy='select')

	json = to_json('id', 'moeda', 'saldo', 'instituicao', 'id_usuario')

	def __str__(self):
		return f'<ContaBancaria: id:{self.id}, moeda:{self.moeda}, \
			saldo:{self.saldo}, instituicao:{self.instituicao}, id_usuario:{self.id_usuario}>'

class Transacao(db.Model):
	__tablename__ = 'transacao'

	id = db.Column(db.Integer, primary_key=True)
	tipo = db.Column(db.Enum(TipoTransacao), nullable=False) # despesa | receita
	valor = db.Column(db.Numeric, nullable=False)
	descricao = db.Column(db.Text, nullable=False)
	resolvido = db.Column(db.Boolean, nullable=False, default=False) # pago (despesa) x recebido (receita)
	data_origem = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.utcnow())

	id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'))
	id_conta_bancaria = db.Column(db.Integer, db.ForeignKey('conta_bancaria.id'))

	json = to_json('id', 'tipo', 'valor', 'descricao', 'resolvido', \
		'data_origem', 'id_categoria', 'id_conta_bancaria')

	def __str__(self):
		return f'<Transacao: id:{self.id}, tipo:{self.tipo}, valor:{self.valor}, \
			descricao:{self.descricao}, resolvido:{self.resolvido}, data_origem:{self.data_origem}, \
				id_categoria:{self.id_categoria}, id_conta_bancaria:{self.id_conta_bancaria}>'


class Categoria(db.Model):
	__tablename__ = 'categoria'

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.Text, nullable=False)
	icone = db.Column(db.Text, nullable=False)

	# mercado, vestuario, saude, ...

	transacoes = db.relationship('Transacao', backref='categoria', lazy='select')

	json = to_json('id', 'nome', 'icone')

	def __str__(self):
		return f'<Categoria: id:{self.id}, nome:{self.nome}, icone:{self.icone}>'