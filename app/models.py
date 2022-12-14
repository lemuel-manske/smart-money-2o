from enum import Enum
from typing import Type, TypeVar

from sqlalchemy.sql import func
from sqlalchemy import inspect

from app import db
from app.utils.enums import Instituicoes, Moedas, TipoTransacao
from app.utils import do_add_commit


T = TypeVar('T')

def get_val(self, field: str) -> str:
	'''
	Retorna o valor de `field`, utilizando
	__getattribute__, verificando a compatibilidade
	com `Enum` (captura `value` do campo) e 
	`db.Model` (captura `to_json` do campo).

	Args:
		self: Any;
		field: str;

	Returns:
		Caso sub-classe de `Enum`: `value`;
		Caso sub-classe de `db.Model`: `to_json()`;
		Se não: valor normal;
	'''
	v = self.__getattribute__(field)

	if issubclass(type(v), Enum):
		return v.value
	elif issubclass(type(v), db.Model):
		return v.json()
	else:
		return v

def to_json(*fields) -> dict:
	'''
	Retorna um dicionário (chave e valor) contendo os
	atributos da classe (como chave) e seus respectivos valores.
	'''
	return lambda self: {
		field: get_val(self, field) for field in fields
	}

class BaseModelClass():
	@classmethod
	def criar_instancia(cls: Type[T], **kwargs) -> T:
		'''
		Realiza a criação de instância de modelo ´db.Model´.
		Adiciona e salva as alterações no banco de dados
		automaticamente `do_add_commit`.

		Args:
			kwargs: Dicionário contendo dados necessários
				para criação.

		Returns:
			inst: Instância de modelo do tipo `cls` criada.
		'''
		inst = cls(**kwargs)
		do_add_commit(inst)

		return inst
	
	def atualizar_instancia(self, **kwargs) -> None:
		'''
		Realiza o update dos atributos de uma instancia de 
		modelo `db.Model`. Salva as alterações automaticamente
		no banco de dados `db.session.commit()`.

		Não permite modificação do campo `id`.
		
		Args:
			kwargs: Dicionário contendo novos dados parciais 
				ou totais.
		
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

	moeda = db.Column(db.Enum(Moedas), nullable=False, default=(Moedas.REAL))

	premium = db.Column(db.Boolean, nullable=False, default=False) # True | False

	json = to_json('id', 'nome', 'email', 'senha', 'moeda', 'premium')	

	contas_bancarias = db.relationship('ContaBancaria', backref='usuario', lazy='select', cascade="all, delete-orphan")
	categorias = db.relationship('Categoria', backref='usuario', lazy='select', cascade="all, delete-orphan")
	transacoes = db.relationship('Transacao', backref='usuario', lazy='select', cascade="all, delete-orphan")
	transferencias = db.relationship('Transferencia', backref='usuario', lazy='select', cascade="all, delete-orphan")

	def __str__(self) -> str:
		return f'<Usuario: id:{self.id}, nome:{self.nome}, email:{self.email}, \
			senha:{self.senha}, moeda:{self.moeda}, premium:{self.premium}>'


class ContaBancaria(BaseModelClass, db.Model):
	__tablename__ = 'conta_bancaria'

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.Text, nullable=False)
	saldo = db.Column(db.Numeric, nullable=False)
	instituicao = db.Column(db.Enum(Instituicoes), nullable=False)

	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

	transacoes = db.relationship('Transacao', backref='conta_bancaria', lazy='select', cascade="all, delete-orphan")
	
	transferencias_realizadas = db.relationship('Transferencia', backref='conta_bancaria_origem', \
		lazy='select', foreign_keys='Transferencia.id_conta_bancaria_origem', cascade="all, delete-orphan")
	transferencias_recebidas = db.relationship('Transferencia', backref='conta_bancaria_destino', \
		lazy='select', foreign_keys='Transferencia.id_conta_bancaria_destino', cascade="all, delete-orphan")

	json = to_json('id', 'nome', 'saldo', 'instituicao', 'usuario')

	def __str__(self) -> str:
		return f'<ContaBancaria: id:{self.id}, nome:{self.nome}, \
			saldo:{self.saldo}, instituicao:{self.instituicao}, \
				id_usuario:{self.id_usuario}>'

class Transacao(BaseModelClass, db.Model):
	__tablename__ = 'transacao'

	id = db.Column(db.Integer, primary_key=True)
	valor = db.Column(db.Numeric, nullable=False)
	tipo = db.Column(db.Enum(TipoTransacao), nullable=False) # despesa | receita
	descricao = db.Column(db.Text, nullable=False)
	resolvido = db.Column(db.Boolean, nullable=False, default=False)
		# pago e não pago (despesa) | recebido e não recebido(receita)
		# caso a transação ainda não foi concluída, o saldo da conta bancária não é reavido
	data_origem = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
	
	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
	id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
	id_conta_bancaria = db.Column(db.Integer, db.ForeignKey('conta_bancaria.id'), nullable=False)

	json = to_json('id', 'tipo', 'valor', 'descricao', 'resolvido', \
		'data_origem', 'usuario', 'categoria', 'conta_bancaria')
	
	def realizar_transacao(self) -> None:
		'''
		Realiza a transação (despesa ou receita),
		reavendo o saldo da conta bancária.

		Returns:
			None.
		'''
		if self.resolvido:
			if self.tipo == TipoTransacao.DESPESA:
				self.conta_bancaria.saldo -= self.valor
			else:
				self.conta_bancaria.saldo += self.valor
				
			db.session.commit()

	def excluir_transacao(self) -> None:
		'''
		Realiza a exlusão de uma transação (despesa ou receita),
		reavendo o saldo da conta bancária.
		
		Returns:
			None.
		'''
		if self.resolvido:
			if self.tipo == TipoTransacao.DESPESA:
				self.conta_bancaria.saldo += self.valor
			else:
				self.conta_bancaria.saldo -= self.valor
				
			db.session.commit()

	def __str__(self) -> str:
		return f'<Transacao: id:{self.id}, tipo:{self.tipo}, valor:{self.valor}, \
			descricao:{self.descricao}, resolvido:{self.resolvido}, data_origem:{self.data_origem}, \
				id_usuario: {self.id_usuario}, id_categoria:{self.id_categoria}, id_conta_bancaria:{self.id_conta_bancaria}>'


class Categoria(BaseModelClass, db.Model):
	__tablename__ = 'categoria'

	id = db.Column(db.Integer, primary_key=True)
	tipo = db.Column(db.Enum(TipoTransacao), nullable=False) # despesa | receita
	nome = db.Column(db.Text, nullable=False)
	icone = db.Column(db.Text, nullable=False)

	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

	json = to_json('id', 'tipo', 'nome', 'icone', 'usuario')

	transacoes = db.relationship('Transacao', backref='categoria', lazy='select')

	def __str__(self) -> str:
		return f'<Categoria: id:{self.id}, tipo:{self.tipo}, nome:{self.nome}, \
			icone:{self.icone}, id_usuario: {self.id_usuario}>'

class Transferencia(BaseModelClass, db.Model):
	__tablename__ = 'transferencia'

	id = db.Column(db.Integer, primary_key=True)
	valor = db.Column(db.Numeric, nullable=False)
	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
	id_conta_bancaria_origem = db.Column(db.Integer, db.ForeignKey('conta_bancaria.id'), nullable=False)
	id_conta_bancaria_destino = db.Column(db.Integer, db.ForeignKey('conta_bancaria.id'), nullable=False)

	json = to_json('id', 'valor', 'usuario', 'conta_bancaria_origem', 'conta_bancaria_destino')

	def realizar_transferencia(self) -> None:
		'''
		Realiza a transferência entre contas bancárias,
		reavendo o saldo da conta bancária origem e adicionando
		na conta bancária destino.

		Returns:
			None.
		'''
		self.conta_bancaria_origem.saldo -= self.valor
		self.conta_bancaria_destino.saldo += self.valor

		db.session.commit()

	def excluir_transferencia(self) -> None:
		'''
		Remove a transferência entre contas bancárias,
		reavendo o saldo da conta bancária origem e destino.

		Returns:
			None.
		'''
		self.conta_bancaria_origem.saldo += self.valor
		self.conta_bancaria_destino.saldo -= self.valor

		db.session.commit()

	def __str__(self) -> str:
		return f'<Transferencia: id:{self.id}, valor:{self.valor}, \
			id_usuario: {self.id_usuario}, id_conta_origem:{self.id_conta_bancaria_origem}, \
				id_conta_destino:{self.id_conta_bancaria_destino}>'