let criar_article_conta_bancaria = (id, moeda, instituicao, saldo) => {
	return `<article class="col" data-id-conta-bancaria="${id}">
		<div class="card rounded-4 shadow">
			<div class="d-flex flex-column px-5 pt-4 pb-3">
				<div class="text-center pb-3 pt-2">
					<svg height="5em" width="5em">
						<use xlink:href="#banco" />
					</svg>
				</div>

				<h3 class="d-flex">
					${moeda}
					<p class="ms-2" id="saldo">${saldo}</p>
				</h3>
				<h5>${instituicao}</h5>


				<table class="table" id="tabela-conta-bancaria-1">
					<thead>
						<tr>
							<th scope="col">#</th>
							<th scope="col">Valor</th>
							<th scope="col">Categoria</th>
							<th scope="col">Conta bancária</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<th scope="row">1</th>
							<td>Mark</td>
							<td>Otto</td>
							<td>@mdo</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</article>
`}

let criar_article_transacoes = (cor_hex, ) => {
	return `<article class="col">
	<div class="card rounded-4 shadow">
		<div class="d-flex flex-column px-5 py-5 pb-3">
			<div class="d-flex align-items-center pb-2">
				<svg fill="#198754" class="me-3" height="2em" width="2em">
					<use xlink:href="#arrow-up" />
				</svg>
				<h3 class="mb-0 fw-bold">RECEITAS</h3>
			</div>
			<h3 class="d-flex">
				{{ currency_symbol }}
				<p class="ms-2" id="valor-receitas">00,00</p>
			</h3>
			<table class="table" id="tabela-receitas">
				<thead>
					<tr>
						<th scope="col"></th>
						<th scope="col">Valor</th>
						<th scope="col">Categoria</th>
						<th scope="col">Conta bancária</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<th scope="row">1</th>
						<td>Mark</td>
						<td>Otto</td>
						<td>@mdo</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</article>
`}