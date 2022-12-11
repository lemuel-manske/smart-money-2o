const DASHBOARD_FIELDS = {
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
		instituicao_select: '#instituicao-bancaria'
	},
	transferencia: {
		valor: "#valor-transferencia",
		contas_bancarias_origem_select: "#contas-bancarias-origem",
		contas_bancarias_destino_select: "#contas-bancarias-destino"
	}
}

jQuery(function($) {
	// Resgatar INSTITUIÇÕES BANCÁRIAS
	$.ajax({
		url: 'http://localhost:5000/enum/instituicao-bancaria',
		method: 'GET',
		
		success: (res) => {
			let data = (JSON.parse(JSON.stringify(res)));

			let instituicoes_bancarias = data['Instituicoes'];

			$.each(instituicoes_bancarias, function (i, inst) {
				$(DASHBOARD_FIELDS.conta_bancaria.instituicao_select).append(
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
				$(DASHBOARD_FIELDS.despesa.categorias_select).append(
					$('<option>', {
						'value': categoria.icone,
						'id': categoria.id,
						'text': categoria.nome,
					})
				)
			})

			$.each(categorias_receita, function (i, categoria) {
				$(DASHBOARD_FIELDS.receita.categorias_select).append(
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

		success: (res) => {
			let contas_bancarias = (JSON.parse(JSON.stringify(res)));
			
			$.each(contas_bancarias, function (i, conta) {
				$(DASHBOARD_FIELDS.despesa.contas_bancarias_select).append(
					$('<option>', {
						'value': conta.nome,
						'id': conta.id,
						'text': conta.nome,
					})
				)

				$(DASHBOARD_FIELDS.receita.contas_bancarias_select).append(
					$('<option>', {
						'value': conta.nome,
						'id': conta.id,
						'text': conta.nome,
					})
				)

				$(DASHBOARD_FIELDS.transferencia.contas_bancarias_origem_select).append(
					$('<option>', {
						'value': conta.nome,
						'id': conta.id,
						'text': conta.nome,
					})
				)

				$(DASHBOARD_FIELDS.transferencia.contas_bancarias_destino_select).append(
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