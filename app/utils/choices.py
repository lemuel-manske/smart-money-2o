from enum import Enum


class EnumBase(Enum):

	@classmethod
	def has_name(cls, name):
		return name in cls._member_names_ 

class Moedas(EnumBase):
	BRAZIL = "R$"
	US_DOLAR = "U$"
	EUR = "€"
	LIBRA = "£"
	IENE = "¥"

class Instituicoes(EnumBase):
	NUBANK = "NUBANK"
	INTER = "INTER"
	BRADESCO = "BRADESCO"
	
class TipoTransacao(EnumBase):
	DESPESA = "DESPESA"
	RECEITA = "RECEITA"