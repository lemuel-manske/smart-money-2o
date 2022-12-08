const fields = {
	despesa: {
		contas_bancarias_select: "#contas-bancarias-despesa",
		categorias_select: "#categorias-despesa",
		valor: "#valor-despesa",
		status: "#status-despesa",
		descricao: "#descricao-despesa"
	},
	receita: {
		contas_bancarias_select: "#contas-bancarias-receita",
		categorias_select: "#categorias-receita",
		valor: "#valor-receita",
		status: "#status-receita",
		descricao: "#descricao-receita"
	},
	conta_bancaria: {
		nome: "#nome-conta-bancaria",
		saldo: "#saldo-conta-bancaria",
		moeda_select: '#selecionar-moeda',
		instituicao_select: '#instituicao-bancaria'
	},
	transferencia: {
		valor: "#valor-transferencia",
		contas_bancarias_origem_select: "#contas-bancarias-origem",
		contas_bancarias_destino_select: "#contas-bancarias-destino"
	}
}

jQuery(function($) {
	// Resgatar MOEDAS
	$.ajax({
		url: 'http://localhost:5000/enum/moedas',
		method: 'GET',
		
		success: (res) => {
			let data = (JSON.parse(JSON.stringify(res)));

			let moedas = data['Moedas'];

			$.each(moedas, function (i, moeda) {
				$(fields.conta_bancaria.moeda_select).append(
					$('<option>', {
						value: i,
						text: moeda,
					})
				)
			})	
		}
	})

	// Resgatar INSTITUIÇÕES BANCÁRIAS
	$.ajax({
		url: 'http://localhost:5000/enum/instituicao-bancaria',
		method: 'GET',
		
		success: (res) => {
			let data = (JSON.parse(JSON.stringify(res)));

			let instituicoes_bancarias = data['Instituicoes'];

			$.each(instituicoes_bancarias, function (i, inst) {
				$(fields.conta_bancaria.instituicao_select).append(
					$('<option>', {
						value: i,
						text: inst,
					})
				)
			})	
		}
	})

	// Resgatar CATEGORIAS PARA DESPESAS e RECEITAS
	$.ajax({
		url: 'http://localhost:5000/api/list/categorias',
		method: 'GET',
		headers: {
			'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
		},
		
		success: (res) => {
			let dados = (JSON.parse(JSON.stringify(res)))
			let categorias_despesa = [];
			let categorias_receita = [];

			for (categoria of dados) {
				if (categoria.tipo === 'DESPESA') {
					categorias_despesa.push(categoria)
				}
				else {
					categorias_receita.push(categoria)
				}
			}
			
			$.each(categorias_despesa, function (i, categoria) {
				$(fields.despesa.categorias_select).append(
					$('<option>', {
						'value': categoria.icone,
						'id': categoria.id,
						'text': categoria.nome,
					})
				)
			})

			$.each(categorias_receita, function (i, categoria) {
				$(fields.receita.categorias_select).append(
					$('<option>', {
						'value': categoria.icone,
						'id': categoria.id,
						'text': categoria.nome,
					})
				)
			})
		}
	})

	// Resgatar todas as CONTAS BANCÁRIAS do USUÁRIO
	$.ajax({
		url: 'http://localhost:5000/api/list/contas-bancarias',
		method: 'GET',
		headers: {
			'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
		},
		
		success: (res) => {
			let contas_bancarias = (JSON.parse(JSON.stringify(res)));
			
			$.each(contas_bancarias, function (i, conta) {
				$(fields.despesa.contas_bancarias_select).append(
					$('<option>', {
						'value': conta.nome,
						'id': conta.id,
						'text': conta.nome,
					})
				)

				$(fields.receita.contas_bancarias_select).append(
					$('<option>', {
						'value': conta.nome,
						'id': conta.id,
						'text': conta.nome,
					})
				)

				$(fields.transferencia.contas_bancarias_origem_select).append(
					$('<option>', {
						'value': conta.nome,
						'id': conta.id,
						'text': conta.nome,
					})
				)

				$(fields.transferencia.contas_bancarias_destino_select).append(
					$('<option>', {
						'value': conta.nome,
						'id': conta.id,
						'text': conta.nome,
					})
				)
			})
		}
	})
})	