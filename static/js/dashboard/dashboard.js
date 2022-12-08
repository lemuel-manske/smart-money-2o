// Resgatar TRANSAÇÕES
$.ajax({
	url: 'http://localhost:5000/api/list/transacoes',
	method: 'GET',
	headers: {
		'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
	},
	
	success: (res) => {
		let dados = (JSON.parse(JSON.stringify(res)))
		let despesas = [];
		let receitas = [];

		for (transacao of dados) {
			if (transacao.tipo === 'DESPESA') {
				despesas.push(transacao)
			}
			else {
				receitas.push(transacao)
			}
		}
	}
})

// Resgatar TRANSFERENCIAS
$.ajax({
	url: 'http://localhost:5000/api/list/transferencias',
	method: 'GET',
	headers: {
		'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
	},
	
	success: (res) => {
		let transferencias = (JSON.parse(JSON.stringify(res)))
	}
})