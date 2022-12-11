let criar_article_conta_bancaria = (conta_bancaria) => {
	return `<article class="col">
		<div class="card rounded-4 shadow">
			<div class="d-flex flex-column px-5 pt-4 pb-3">
				<div class="d-flex align-items-center pb-3 pt-2">
					<svg class="pe-3" height="4em" width="4em">
						<use xlink:href="#bank" />
					</svg>
					<h3>${conta_bancaria.nome}</h3>
				</div>
				<h5>${conta_bancaria.instituicao}</h5>

				<h3 class="d-flex mb-2">
					${conta_bancaria.usuario.moeda}
					<p class="ms-2" id="saldo">${parseFloat(conta_bancaria.saldo).toFixed(2)}</p>
				</h3>

				<h5>Suas transações</h5>
				
				<table class="table" id="tabela-conta-bancaria-${conta_bancaria.id}">
					<thead>
						<tr>
							<th scope="col"></th>
							<th scope="col">Valor</th>
							<th scope="col">Tipo</th>
							<th scope="col">Categoria</th>
						</tr>
					</thead>
					<tbody>
						<tr id="tabela-conta-bancaria-${conta_bancaria.id}-default-row">
							<th scope='row'>...</th>
							<td>...</td>
							<td>...</td>
							<td>...</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</article>
`}