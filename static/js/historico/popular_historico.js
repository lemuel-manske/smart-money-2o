const ARTICLES = {
	despesa: {
		valor_despesas: '#valor-despesas',
		tabela_despesas: '#tabela-despesas',
		despesas_pagas: '#despesas-pagas',
		despesas_nao_pagas: '#despesas-nao-pagas'
	},
	receita: {
		valor_receitas: '#valor-receitas',
		tabela_receitas: '#tabela-receitas',
		receitas_pagas: '#receitas-recebidas',
		receitas_nao_pagas: '#receitas-nao-recebidas'
	},
	transferencia: {
		valor_transferencias: '#valor-transferencias',
		tabela_transferencias: '#tabela-transferencias'
	},
	contas_bancarias: {
		saldo_contas_bancarias: '#saldo-contas-bancarias',
		tabela_contas_bancarias: '#tabela-contas-bancarias'
	}
}

const MOEDA_USUARIO = localStorage.getItem('moeda');

jQuery(function($) {
	// Resgatar TRANSAÇÕES
	$.ajax({
		url: 'http://localhost:5000/api/list/transacoes',
		method: 'GET',

		success: (res) => {
			let transacoes = JSON.parse(JSON.stringify(res));

			let despesas = [];
			let despesas_totais_nao_pagas = 0.0;
			let despesas_totais_pagas = 0.0;

			let receitas = [];
			let receitas_totais_nao_recebidas = 0.0;
			let receitas_totais_recebidas = 0.0;

			for (transacao of transacoes) {
				if (transacao.tipo === 'DESPESA') {
					if (transacao.resolvido) {
						despesas_totais_pagas += parseFloat(transacao.valor);
					} else {
						despesas_totais_nao_pagas += parseFloat(transacao.valor);
					}
					despesas.push(transacao);
				}
				else {
					if (transacao.resolvido) {
						receitas_totais_recebidas += parseFloat(transacao.valor);
					} else {
						receitas_totais_nao_recebidas += parseFloat(transacao.valor);
					}
					receitas.push(transacao);
				}
			}

			$(ARTICLES.despesa.valor_despesas).append(`${MOEDA_USUARIO} ${(despesas_totais_nao_pagas + despesas_totais_pagas).toFixed(2)}`);
			$(ARTICLES.despesa.despesas_pagas).append(`${MOEDA_USUARIO} ${despesas_totais_pagas.toFixed(2)}`);
			$(ARTICLES.despesa.despesas_nao_pagas).append(`${MOEDA_USUARIO} ${despesas_totais_nao_pagas.toFixed(2)}`);

			$(ARTICLES.receita.valor_receitas).append(`${MOEDA_USUARIO} ${(receitas_totais_nao_recebidas + receitas_totais_recebidas).toFixed(2)}`);
			$(ARTICLES.receita.receitas_pagas).append(`${MOEDA_USUARIO} ${receitas_totais_recebidas.toFixed(2)}`);
			$(ARTICLES.receita.receitas_nao_pagas).append(`${MOEDA_USUARIO} ${receitas_totais_nao_recebidas.toFixed(2)}`);
		
			$.each(despesas, function(i, despesa) {
				$('#despesas-default-row').toggleClass('d-none', !(despesas.length === 0));

				$(`${ARTICLES.despesa.tabela_despesas} tbody`).append(`
					<tr>
						<th scope="row" id="${despesa.id}">
						${
							despesa.resolvido? 
								`
									<svg fill="#198754" width="18" height="18" role="img" aria-label="Pago">
										<use xlink:href="#circle-check" />
									</svg>
								` : 
								`
									<svg fill="#FFC944" width="18" height="18" role="img" aria-label="Não pago">
										<use xlink:href="#exclamation-point" />
									</svg>
								`
						}
						</th>
						<td>${MOEDA_USUARIO} ${parseFloat(despesa.valor).toFixed(2)}</td>
						<td>
							<svg class="pe-1" width="24" height="24" role="img" aria-label="${despesa.categoria.nome}">
								<use xlink:href="#${despesa.categoria.icone}" />
							</svg>
							${despesa.categoria.nome}
						</td>
						<td>${despesa.conta_bancaria.nome}</td>
						<td>${despesa.descricao}</td>
						<td>
							${
								despesa.resolvido? 
								`
								<ul class="d-flex list-unstyled">
									<li class="px-2">
										<a type="button" class="excluir-transacao">
											<svg fill="#dc3545" width="24" height="24" role="img" aria-label="Excluir">
												<use xlink:href="#circle-x" />
											</svg>
										</a>
									</li>
								</ul>
								` : 
								`
								<ul class="d-flex list-unstyled">
									<li class="px-1">
										<a type="button" class="excluir-transacao">
											<svg fill="#dc3545" width="24" height="24" role="img" aria-label="Excluir">
												<use xlink:href="#circle-x" />
											</svg>
										</a>
									</li>

									<li class="px-2">
										<a type="button" class="efetuar-resolver">
											<svg fill="#198754" width="24" height="24" role="img" aria-label="Efetuar">
												<use xlink:href="#circle-check" />
											</svg>
										</a>	
									</li>
								</ul>
								`
							}
						</td>
					</tr>
				`);
			});

			$.each(receitas, function(i, receita) {
				$('#receitas-default-row').toggleClass('d-none', !(receitas.length === 0));

				$(`${ARTICLES.receita.tabela_receitas} tbody`).append(`
					<tr>
						<th scope="row" id="${receita.id}">
							${
								receita.resolvido? 
									`
										<svg fill="#198754" width="18" height="18" role="img" aria-label="Recebido">
											<use xlink:href="#circle-check" />
										</svg>
									` : 
									`
										<svg fill="#FFC944" width="18" height="18" role="img" aria-label="Não recebido">
											<use xlink:href="#exclamation-point" />
										</svg>
									`
							}
						</th>
						<td>${MOEDA_USUARIO} ${parseFloat(receita.valor).toFixed(2)}</td>
						<td>
							<svg class="pe-1" width="24" height="24" role="img" aria-label="${receita.categoria.nome}">
								<use xlink:href="#${receita.categoria.icone}" />
							</svg>
							${receita.categoria.nome}
						</td>
						<td>${receita.conta_bancaria.nome}</td>
						<td>${receita.descricao}</td>
						<td>
							${
								receita.resolvido? 
								`
								<ul class="d-flex list-unstyled">
									<li class="px-1">
										<a type="button" class="excluir-transacao">
											<svg fill="#dc3545" width="24" height="24" role="img" aria-label="Excluir">
												<use xlink:href="#circle-x" />
											</svg>
										</a>
									</li>
								</ul>
								` : 
								`
								<ul class="d-flex list-unstyled">
									<li class="px-1">
										<a type="button" class="excluir-transacao" onclick="console.log('oi')>
											<svg fill="#dc3545" width="24" height="24" role="img" aria-label="Excluir">
												<use xlink:href="#circle-x" />
											</svg>
										</a>
									</li>
									
									<li class="px-1">
										<a type="button" class="efetuar-resolver">
											<svg fill="#198754" width="24" height="24" role="img" aria-label="Efetuar">
												<use xlink:href="#circle-check" />
											</svg>
										</a>	
									</li>
								</ul>
								`
							}
						</td>
					</tr>
				`);
			})
		}
	})

	// Resgatar TRANSFERENCIAS
	$.ajax({
		url: 'http://localhost:5000/api/list/transferencias',
		method: 'GET',

		success: (res) => {
			let transferencias = JSON.parse(JSON.stringify(res));

			let valor_transferencias = 0.0;

			for (transf of transferencias) {
				valor_transferencias += parseFloat(transf.valor);
			}

			$(ARTICLES.transferencia.valor_transferencias).append(`${MOEDA_USUARIO} ${(valor_transferencias).toFixed(2)}`);
		
			$.each(transferencias, function(i, transf) {
				$('#transferencias-default-row').toggleClass('d-none', !(transferencias.length === 0));

				$(`${ARTICLES.transferencia.tabela_transferencias} tbody`).append(`
					<tr>
						<th scope="row" id="${transf.id}">${MOEDA_USUARIO} ${parseFloat(transf.valor).toFixed(2)}</th>
						<td>${transf.conta_bancaria_origem.nome}</td>
						<td>${transf.conta_bancaria_destino.nome}</td>
						<td>
							<ul class="d-flex list-unstyled">
								<li class="px-2">
									<a type="button" class="excluir-transferencia">
										<svg fill="#dc3545" width="24" height="24" role="img" aria-label="Excluir">
											<use xlink:href="#circle-x" />
										</svg>
									</a>
								</li>
							</ul>
						</td>
					</tr>
				`);
			});
		}
	})

	// Resgatar CONTAS BANCÁRIAS
	$.ajax({
		url: 'http://localhost:5000/api/list/contas-bancarias',
		method: 'GET',

		success: (res) => {
			let contas = JSON.parse(JSON.stringify(res));

			let saldo_contas = 0.0;

			for (conta of contas) {
				saldo_contas += parseFloat(conta.saldo);
			}

			$(ARTICLES.contas_bancarias.saldo_contas).append(`${MOEDA_USUARIO} ${(saldo_contas).toFixed(2)}`);
		
			$.each(contas, function(i, conta) {
				$('#contas-bancarias-default-row').toggleClass('d-none', !(contas.length === 0));

				$(`${ARTICLES.contas_bancarias.tabela_contas_bancarias} tbody`).append(`
					<tr>
						<th scope="row" id="${conta.id}">${MOEDA_USUARIO} ${parseFloat(conta.saldo).toFixed(2)}</th>
						<td>${conta.nome}</td>
						<td>${conta.instituicao}</td>
						<td>
							<ul class="d-flex list-unstyled">
								<li class="px-2">
									<a type="button" class="excluir-conta-bancaria">
										<svg fill="#dc3545" width="24" height="24" role="img" aria-label="Excluir">
											<use xlink:href="#circle-x" />
										</svg>
									</a>
								</li>
							</ul>
						</td>
					</tr>
				`);
			});
		}
	})
})