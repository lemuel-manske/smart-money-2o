from enum import Enum, auto

class Moedas(Enum):
	BRAZIL = "R$"
	USDOLAR = "U$"
	EUR = "€"
	LIBRA = "£"
	IENE = "¥"

class Instituicoes(Enum):
	NUBANK = auto()
	INTER = auto()
	BRADESCO = auto()
	
class TipoTransacao(Enum):
	DESPESA = auto()
	RECEITA = auto()