from enum import Enum


class EnumBase(Enum):

	@classmethod
	def to_json(cls):
		'''
		Cria um dicionário de representação das classes enumeradoras,
		contendo chave e valor atribuídos.
		'''
		return {
			cls.__name__: { attr: cls[attr].value for attr in cls._member_names_ }
		}

	@classmethod
	def has_name(cls, name):
		'''
		Verifica se a classe enumeradora possui o nome especificado.
		'''
		return name in cls._member_names_ 


class Moedas(EnumBase):
	'''
	REAL = "R$"
	US_DOLAR = "U$"
	EUR = "€"
	LIBRA = "£"
	IENE = "¥"
	'''
	REAL = "R$"
	US_DOLAR = "U$"
	EURO = "€"
	LIBRA = "£"
	IENE = "¥"


class Instituicoes(EnumBase):
	'''
	NUBANK = "NUBANK"
	INTER = "INTER"
	BRADESCO = "BRADESCO"
	'''
	NUBANK = "Nubank"
	BANCO_INTER = "Banco Inter"
	BRADESCO = "Bradesco"
	CARTEIRA = "Carteira"
	
class TipoTransacao(EnumBase):
	'''
	DESPESA = "DESPESA"
	RECEITA = "RECEITA"
	'''
	DESPESA = "DESPESA"
	RECEITA = "RECEITA"