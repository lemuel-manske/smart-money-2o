# smart-money-2o
Web development project, made with Flask.

`pip install -r requirements.txt`
`execute run.py`

curl 191.52.6.57:5000/login -X POST -H "Content-Type: application/json" --data '{ "email":"lemuelkaue@gmail.com", "senha":"123"}'

/login

	Realiza o login do usuário via POST.
	Realiza request de dados em json (email e senha), 
	validando os mesmos (`get_validade`).
	Returns:
		CÓD. 200 (OK): Criação de JWT (identidade id) e 
			retorna objeto usuário em formato json.
		CÓD. 401 (UNAUTHORIZED): Senha incorreta.
		CÓD. 404 (NOT_FOUND): Usuário não encontrado 
			no banco de dados.
 
  /cadastro
  
	Realiza registro de um novo usuário via POST.
	Realiza request de dados em json (email, senha e nome),
	validando os mesmos (`get_validate`).
	Realiza o login imediatamente após confirmação de sucesso (JWT).
	Returns:
		CÓD. 200 (OK): Criação de JWT (identidade id) e 
			retorna objeto usuário em formato json.
		CÓD. 409 (CONFLICT): Usuário já existe (filtro p/ email).
  
/atualizar-conta

	Realiza a alteração dos dados do usuário via POST.
	Realiza request de dados em json (email, senha, nova_senha e nome),
	validando os mesmos (`get_validate`).
	Returns:
		CÓD. 200 (OK): Atualiza os dados e retorna objeto 
			usuário em formato json.
		CÓD. 401 (UNAUTHORIZED): Senha incorreta.
 
  
  /minha-conta
  
	Retorna os dados da conta do usuário com login na sessão.
	Returns:
		CÓD. 200 (OK): Retorno dos dados do usuário em
			formato json.
  
/enum

	Retorna classes enumeradores existentes.
  
  /listar
  
	Rota de listagem genérica.
	Extrai a nome da classe através do URL e retorna as
	informações contempladas pela conta do usuário na 
	sessão (JWT necessário).
	Returns:
		CÓD. 200 (OK): Retorno de informações em formato json.
		CÓD 404 (NOT_FOUND): Nome da classe informada não contempla
			nenhum modelo do banco de dados.
  
  /criar/conta-bancaria
  
	Realiza o cadastro de uma nova conta bancária 
	na conta do usuário via POST.
	Realiza request de dados em json (tipo de moeda, saldo e instituição
	bancária), validando os mesmos (`get_validate`).
	Para moeda e instituição é realizado verificação de 'compatibilidade'
	com os tipos presentes em classes enumeradoras `Moeda` e `Instituicao` 
	(`choices.py`).
	Returns:
		CÓD. 200 (OK): Cadastro da conta bancária e retorno dos dados 
			cadastrados em formato json.
		CÓD 404 (NOT_FOUND): Moeda ou instituição bancária informada não 
			compatíveis com os valores presentes nos enumeradores.
  
  /criar/transacao/
  
	Realiza o cadastro de uma nova transação 
	na conta do usuário via POST.
	Realiza request de dados em json (valor, descrição, resolvido, 
	id_categoria e id_conta_bancaria), validando os mesmos (`get_validate`).
	Para o parâmetro `tipo` na URL, é realizado verificação de 
	correspondência com os valores presentes na classe
	enumeradora `TipoTransacao`.
	O id de categoria informado deve corresponder ao mesmo tipo informado por
	URL, isto é, 'despesa' para ambos ou 'receita' para ambos.
	Returns:
		CÓD. 200 (OK): Cadastro de nova transação e retorno dos dados 
			cadastrados em formato json.
		CÓD 401 (UNAUTHORIZED): O id da categoria informado não corresponde;
			parâmetro na URL não corresponde a nenhum valor na classe `TipoTransacao`
		CÓD 404 (NOT_FOUND): Nenhuma conta bancária ou categoria com o 
			id informado foi encontrada.
  
  /criar/categoria/
  
	Realiza o cadastro de uma nova categoria 
	na conta do usuário via POST.
	Realiza request de dados em json (nome e ícone), validando os 
	mesmos (`get_validate`).
	Para o tipo de categoria verificação de 'compatibilidade'
	com os tipos presentes na classe enumeradora `TipoTransacao` 
	(choices.py).
	Returns:
		CÓD. 200 (OK): Cadastro da categoria e retorno dos dados 
			cadastrados em formato json.
		CÓD 401 (BAD_REQUEST): Tipo de categoria informado não 
			compatível com 'despesa' ou 'receita'.
