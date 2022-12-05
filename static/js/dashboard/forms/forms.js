const fields = {
	despesa: {
		contas_bancarias_select: "#contas-bancarias-despesa",
		categorias_select: "#categorias-despesa",
		valor: "#valor-despesa",
		status: "#status-despesa",
		descricao: "#descricao-despesa"
	}
}

jQuery(function($) {
	
	cleanErrors();

	$('#despesa-submit').on('click', function () {
		despesa_fields = fields.despesa

		let [ contas_bancarias_select, categorias_select, valor, foi_pago, descricao ] = get_validate(
			despesa_fields.contas_bancarias_select,
			despesa_fields.categorias_select,
			despesa_fields.valor,
			despesa_fields.status,
			despesa_fields.descricao)

		is_error = !completed_fieds(despesa_fields.valor, despesa_fields.descricao)

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/create/'
			})
		}
	})
})