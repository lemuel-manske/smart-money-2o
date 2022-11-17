from geral.config import *
from modelo.Pessoa import *

@app.route("/atualizar/<string:classe>", methods=['put'])
def atualizar(classe):
    # preparar uma resposta otimista
    resposta = jsonify({"resultado": "ok", "detalhes": "ok"})
    # receber as informações do novo objeto
    dados = request.get_json()  
    try:  
        if classe == "Pessoa":
            if 'id' not in dados: # não tem o atributo id?
                resposta = jsonify({"resultado": "erro", 
                            "detalhes": "Atributo id não encontrado"})
            else:
                id = dados['id']
                alguem = Pessoa.query.get(id) # localizar a pessoa
                if alguem is None: # se não encontrou
                    resposta = jsonify({"resultado": "erro", 
                                "detalhes": f"Objeto não encontrado, id: {id}"})
                else:
                    # atualizar os campos (esta parte dá pra melhorar :-)
                    alguem.nome = dados['nome'] # if dados['nome'] is not None else alguem.nome
                    alguem.email = dados['email']
                    alguem.senha = dados['senha']
                    db.session.commit()  # efetivar a atualização
        else:
            resposta = jsonify({"resultado": "erro", "detalhes": f"Classe não encontrada: {classe}"})        
        
    except Exception as e:  # em caso de erro...
        # informar mensagem de erro
        resposta = jsonify({"resultado": "erro", "detalhes": str(e)})
    # adicionar cabeçalho de liberação de origem
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta  # responder!

''' 
RESULTADOS DE TESTES:

$ curl -X PUT -d '{"id":1, "nome":"Teresa", "email":"te@gmail.com", "senha":"123456789"}' -H "Content-Type:application/json" localhost:5000/atualizar/Pessoa 
{
  "detalhes": "ok", 
  "resultado": "ok"
}

$ curl localhost:5000/retornar/Pessoa/1
{
  "detalhes": {
    "email": "te@gmail.com", 
    "id": 1, 
    "nome": "Teresa", 
    "senha": "123456789"
  }, 
  "resultado": "ok"
}

curl -X PUT -d '{"nome":"Paulo", "email":"pa@gmail.com", "senha":"123456789"}' -H "Content-Type:application/json" localhost:5000/atualizar/Pessoa 
{
  "detalhes": "Atributo id n\u00e3o encontrado", 
  "resultado": "erro"
}

AUSÊNCIA DO CAMPO SENHA:
$ curl -X PUT -d '{"id":1, "nome":"Teresa", "email":"te@gmail.com"}' -H "Content-Type:application/json" localhost:5000/atualizar/Pessoa {
  "detalhes": "'senha'", 
  "resultado": "erro"
}

'''