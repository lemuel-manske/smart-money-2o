from enum import Enum
from typing import Type, TypeVar

from sqlalchemy.sql import func
from sqlalchemy import inspect

from app import db
from app.utils.choices import Instituicoes, Moedas, TipoTransacao
from app.utils import do_add_commit


T = TypeVar('T')

def get_val(self, field: str) -> str:
	'''
	Captura o valor do campo (`self.__gettattribute`),
	realizando verificação de compatibilidade com Enum,
	retornando o nome do enumerador ou simplesmente o atributo,
	caso não seja uma instancia de Enum.
	'''
	v = self.__getattribute__(field)

	if issubclass(type(v), Enum):
		return v.name
	else:
		return v

def to_json(*fields) -> dict:
	'''
	Retorna um dicionário contendo os atributos da classe.
	'''
	return lambda self: {
		field: get_val(self, field) for field in fields
	}

class BaseModelClass():
	@classmethod
	def create(cls: Type[T], **kwargs) -> T:
		'''
		Realiza a criação de instância de modelo (´db.Model´).
		Adiciona e salva as alterações no banco de dados 
		automaticamente (`do_add_commit`).

		Args:
			kwargs: Dicionário contendo dados necessários.

		Returns:
			inst: Instância de modelo criada
		'''
		inst = cls(**kwargs)
		do_add_commit(inst)

		return inst
	
	def update(self, **kwargs) -> None:
		'''
		Realiza o update dos atributos de uma instancia de 
		modelo (`db.Model`). Salva as alterações automaticamente
		no banco de dados.
		
		Args:
			kwargs: Dicionário contendo novos dados.
		
		Returns:
			None.
		'''
		attributes = inspect(self).attrs
		for attr in attributes:
			if attr.key in kwargs and attr.key != 'id':
				self.__setattr__(attr.key, kwargs[attr.key])
			
		db.session.commit()
		

class Usuario(BaseModelClass, db.Model):
	__tablename__ = 'usuario'

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.Text, nullable=False)
	email = db.Column(db.Text, nullable=False, unique=True)
	senha = db.Column(db.Text, nullable=False)
	premium = db.Column(db.Boolean, nullable=False, default=False) # True | False

	json = to_json('id', 'nome', 'email', 'senha', 'premium')	

	contas_bancarias = db.relationship('ContaBancaria', backref='usuario', lazy='select')
	categorias = db.relationship('Categoria', backref='usuario', lazy='select')
	transacoes = db.relationship('Transacao', backref='usuario', lazy='select')
	transferencias = db.relationship('Transferencia', backref='usuario', lazy='select')

	def __str__(self) -> str:
		return f'<Usuario: id:{self.id}, nome:{self.name}, email:{self.email}, \
			senha:{self.password}, premium:{self.premium}>'


class ContaBancaria(BaseModelClass, db.Model):
	__tablename__ = 'conta_bancaria'

	id = db.Column(db.Integer, primary_key=True)
	moeda = db.Column(db.Enum(Moedas), nullable=False, default=(Moedas.BRAZIL))
	saldo = db.Column(db.Numeric, nullable=False)
	instituicao = db.Column(db.Enum(Instituicoes), nullable=False)

	json = to_json('id', 'moeda', 'saldo', 'instituicao', 'id_usuario')

	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

	despesas = db.relationship('Transacao', backref='conta_bancaria', lazy='select')
	transferencias = db.relationship('Transferencia', backref='conta_bancaria', lazy='select')

	def __str__(self) -> str:
		return f'<ContaBancaria: id:{self.id}, moeda:{self.moeda}, \
			saldo:{self.saldo}, instituicao:{self.instituicao}, \
				id_usuario:{self.id_usuario}>'

class Transacao(BaseModelClass, db.Model):
	__tablename__ = 'transacao'

	id = db.Column(db.Integer, primary_key=True)
	tipo = db.Column(db.Enum(TipoTransacao), nullable=False) # despesa | receita
	valor = db.Column(db.Numeric, nullable=False)
	descricao = db.Column(db.Text, nullable=False)
	resolvido = db.Column(db.Boolean, nullable=False, default=False)
		# pago e não pago (despesa) | recebido e não recebido(receita)
	data_origem = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
	
	json = to_json('id', 'tipo', 'valor', 'descricao', 'resolvido', \
		'data_origem', 'id_categoria', 'id_conta_bancaria')

	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
	id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
	id_conta_bancaria = db.Column(db.Integer, db.ForeignKey('conta_bancaria.id'), nullable=False)

	def do_transacao(self, conta_bancaria: ContaBancaria) -> None:
		'''
		Realiza a transação (despesa ou receita),
		reavendo o saldo da conta bancária.

		Args:
			conta_bancaria: Instância de objeto `ContaBancaria`.

		Returns:
			None.
		'''
		if self.resolvido:
			if self.tipo == TipoTransacao.DESPESA:
				conta_bancaria.saldo -= self.valor
			else:
				conta_bancaria.saldo += self.valor
				
			db.session.commit()

	def __str__(self) -> str:
		return f'<Transacao: id:{self.id}, tipo:{self.tipo}, valor:{self.valor}, \
			descricao:{self.descricao}, resolvido:{self.resolvido}, data_origem:{self.data_origem}, \
				id_categoria:{self.id_categoria}, id_conta_bancaria:{self.id_conta_bancaria}>'


class Categoria(BaseModelClass, db.Model):
	__tablename__ = 'categoria'

	id = db.Column(db.Integer, primary_key=True)
	tipo = db.Column(db.Enum(TipoTransacao), nullable=False) # despesa | receita
	nome = db.Column(db.Text, nullable=False)
	icone = db.Column(db.Text, nullable=False)

	json = to_json('id', 'nome', 'icone')

	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

	transacoes = db.relationship('Transacao', backref='categoria', lazy='select')

	def __str__(self) -> str:
		return f'<Categoria: id:{self.id}, tipo:{self.tipo}, nome:{self.nome}, icone:{self.icone}>'

class Transferencia(BaseModelClass, db.Model):
	__tablename__ = 'transferencia'

	id = db.Column(db.Integer, primary_key=True)
	valor = db.Column(db.Numeric, nullable=False)
	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
	id_conta_bancaria_origem = db.Column(db.Integer, db.ForeignKey('conta_bancaria.id'), nullable=False)
	id_conta_bancaria_destino = db.Column(db.Integer, db.ForeignKey('conta_bancaria.id'), nullable=False)

	def __str__(self) -> str:
		return f'<Transferencia: id:{self.id}, valor:{self.valor}, \
			conta_origem:{self.id_conta_bancaria_origem}, conta_destino:{self.id_conta_bancaria_destino}>'