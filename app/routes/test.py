'''
@app.route('/teste')
def teste_db():
	user = Usuario(
		nome='lemuel',
		email='lemuelkaue@gmail.com',
		senha='123'
	)

	db.session.add(user)
	db.session.commit()

	conta_bancaria = ContaBancaria(
		moeda=Moedas.BRAZIL,
		saldo=800,
		instituicao=Instituicoes.NUBANK,
		id_usuario=1
	)

	db.session.add(conta_bancaria)
	db.session.commit()

	return user.json()
'''