from geral.config import *
from modelo.Pessoa import Pessoa

def run():
    print("TESTE DE PESSOA")
    
    p1 = Pessoa(nome = "João da Silva", email = "josilva@gmail.com", 
    senha = "097253")
    p2 = Pessoa(nome = "Maria Oliveira", email = "molive@gmail.com", 
        senha = "73658")        
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    print(p1, p2)