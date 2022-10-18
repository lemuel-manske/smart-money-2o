from enum import Enum, auto

class Moedas(Enum):
	BRAZIL = "R$"
	USDOLAR = "U$"
	EUR = "€"
	LIBRA = "£"
	IENE = "¥"

class Instituicoes(Enum):
	NUBANK = "NUBANK"
	INTER = "INTER"
	BRADESCO = "BRADESCO"
	
class TipoTransacao(Enum):
	DESPESA = auto()
	RECEITA = auto()