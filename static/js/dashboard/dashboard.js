const ARTICLES = {
	despesa: {
		valor_despesas: '#valor-despesas',
		tabela_despesas: '#tabela-despesas'
	},
	receita: {
		valor_receitas: '#valor-receitas',
		tabela_receitas: '#tabela-receitas'
	},
	transferencia: { 
		valor_transferencias: '#valor-transferencias',
		tabela_transferencias: '#tabela-transferencias'
	},
	contas_bancarias: '#contas-bancarias-resume'
}

const MOEDA_USUARIO = localStorage.getItem('moeda');

// Resgatar contas bancárias
$.ajax({
	url: 'http://localhost:5000/api/list/contas-bancarias',
	method: 'GET',
	
	success: (res) => {
		let contas_bancarias = (JSON.parse(JSON.stringify(res)));

		$('#msg-sem-contas-bancarias').toggleClass('d-none', !(contas_bancarias.length === 0));

		$.each(contas_bancarias, function(i , conta) {
			$(ARTICLES.contas_bancarias).append(
				criar_article_conta_bancaria(conta)
			)
		})
	}
})

// Resgatar TRANSAÇÕES
$.ajax({
	url: 'http://localhost:5000/api/list/transacoes',
	method: 'GET',

	success: (res) => {
		let transacoes = JSON.parse(JSON.stringify(res));

		let despesas = [];
		let despesas_total = 0.0;

		let receitas = [];
		let receitas_total = 0.0;

		for (transacao of transacoes) {
			if (transacao.tipo === 'DESPESA') {
				despesas.push(transacao);
				despesas_total += parseFloat(transacao.valor);
			}
			else {
				receitas.push(transacao);
				receitas_total += parseFloat(transacao.valor);
			}
		}

		$(ARTICLES.despesa.valor_despesas).append(`${MOEDA_USUARIO} ${despesas_total.toFixed(2)}`);

		$(ARTICLES.receita.valor_receitas).append(`${MOEDA_USUARIO} ${receitas_total.toFixed(2)}`);
	
		$.each(despesas.slice(0, 2), function(i, despesa) {
			$('#despesas-default-row').toggleClass('d-none', !(despesas.length === 0));

			$(`${ARTICLES.despesa.tabela_despesas} tbody`).append(`
				<tr>
					<th scope='row'>${despesa.id}</th>
					<td>${MOEDA_USUARIO} ${parseFloat(despesa.valor).toFixed(2)}</td>
					<td>
						<svg class="pe-1" width="24" height="24" role="img" aria-label="${despesa.categoria.nome}">
							<use xlink:href="#${despesa.categoria.icone}" />
						</svg>
						${despesa.categoria.nome}
					</td>
					<td>${despesa.conta_bancaria.nome}</td>
				</tr>
			`);
		});

		$.each(receitas.slice(0, 2), function(i, receita) {
			$('#receitas-default-row').toggleClass('d-none', !(receitas.length === 0));

			$(`${ARTICLES.receita.tabela_receitas} tbody`).append(`
				<tr>
					<th scope='row'>${receita.id}</th>
					<td>${MOEDA_USUARIO} ${parseFloat(receita.valor).toFixed(2)}</td>
					<td>
						<svg class="pe-1" width="24" height="24" role="img" aria-label="${receita.categoria.nome}">
							<use xlink:href="#${receita.categoria.icone}" />
						</svg>
						${receita.categoria.nome}
					</td>
					<td>${receita.conta_bancaria.nome}</td>
				</tr>
			`);
		})


		$.each(transacoes.slice(0, 3), function(i, transacao) {
			$(`#tabela-conta-bancaria-${transacao.conta_bancaria.id}-default-row`).toggleClass('d-none', !(transacoes.length === 0));

			$(`#tabela-conta-bancaria-${transacao.conta_bancaria.id} tbody`).append(`
				<tr>
					<th scope='row'>${transacao.id}</th>
					<td>${MOEDA_USUARIO} ${parseFloat(transacao.valor).toFixed(2)}</td>
					<td>${transacao.tipo}</td>
					<td>
						<svg class="pe-1" width="24" height="24" role="img" aria-label="${transacao.categoria.nome}">
							<use xlink:href="#${transacao.categoria.icone}" />
						</svg>
						${transacao.categoria.nome}
					</td>
				</tr>
			`)
		})
	}
})

// Resgatar TRANSFERENCIAS
$.ajax({
	url: 'http://localhost:5000/api/list/transferencias',
	method: 'GET',
	
	success: (res) => {
		let transferencias = (JSON.parse(JSON.stringify(res)));
		let transferencias_total = 0.0;

		for (transf of transferencias) {
			transferencias_total += parseFloat(transf.valor);
		}

		$(ARTICLES.transferencia.valor_transferencias).append(`${MOEDA_USUARIO} ${transferencias_total.toFixed(2)}`);

		$.each(transferencias.slice(0, 2), function(i, transf) {
			$('#transferencias-default-row').toggleClass('d-none', !(transferencias.length === 0));

			$(`${ARTICLES.transferencia.tabela_transferencias} tbody`).append(
				`<tr>
					<th scope='row'>${transf.id}</th>
					<td>${MOEDA_USUARIO} ${parseFloat(transf.valor).toFixed(2)}</td>
					<td>${transf.conta_bancaria_origem.nome}</td>
					<td>${transf.conta_bancaria_destino.nome}</td>
				</tr>`
			);
		});
	}
})