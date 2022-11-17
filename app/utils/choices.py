from enum import Enum


class EnumBase(Enum):

	@classmethod
	def representation(cls):
		return {
			cls.__name__: [ attr for attr in cls._member_names_ ]
		}

	@classmethod
	def has_name(cls, name):
		'''
		Verifica se a classe enumeradora possui o nome especificado.
		'''
		return name in cls._member_names_ 


class Moedas(EnumBase):
	'''
	BRAZIL = "R$"
	US_DOLAR = "U$"
	EUR = "€"
	LIBRA = "£"
	IENE = "¥"
	'''
	BRAZIL = "R$"
	US_DOLAR = "U$"
	EUR = "€"
	LIBRA = "£"
	IENE = "¥"


class Instituicoes(EnumBase):
	'''
	NUBANK = "NUBANK"
	INTER = "INTER"
	BRADESCO = "BRADESCO"
	'''
	NUBANK = "NUBANK"
	INTER = "INTER"
	BRADESCO = "BRADESCO"

	
class TipoTransacao(EnumBase):
	'''
	DESPESA = "DESPESA"
	RECEITA = "RECEITA"
	'''
	DESPESA = "DESPESA"
	RECEITA = "RECEITA"