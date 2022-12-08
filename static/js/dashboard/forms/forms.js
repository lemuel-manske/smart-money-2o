jQuery(function($) {

	clean_errors();
	
	check_flash_message();

	$('#conta-bancaria-submit').on('click', function () {
		conta_bancaria_fields = fields.conta_bancaria;

		let [ nome, saldo ] = get_fields_values(conta_bancaria_fields.nome, conta_bancaria_fields.saldo)
		let [ moeda, instituicao ] = get_select_fields_values(conta_bancaria_fields.moeda_select, 
				conta_bancaria_fields.instituicao_select)

		is_error = !completed_fieds(conta_bancaria_fields.saldo, conta_bancaria_fields.nome)

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/create/conta-bancaria',
				method: 'POST',
				headers: {
					'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
				},
				contentType: 'application/json',
				dataType: 'json',
				data: JSON.stringify({
					nome: nome,
					saldo: saldo,
					moeda: moeda,
					instituicao: instituicao
				}),
				
				success: (res) => {
					sessionStorage.setItem('flash_message', `Conta bancária "${nome}" adicionada com sucesso!`);
					
					location.reload();
				},

				error: (xhr) => {
					response = xhr.responseJSON;
					console.log(response)
				}
			})
		}	
	})

	$('#despesa-submit').on('click', function () {
		despesa_fields = fields.despesa;
		
		let [ valor, descricao ] = get_fields_values(despesa_fields.valor, despesa_fields.descricao);
		let [ conta_bancaria, categoria ] = get_select_fields_id(despesa_fields.contas_bancarias_select,
			despesa_fields.categorias_select);
		let [ status ] = get_check_box_fields_values(despesa_fields.status);
		
		is_error = !completed_fieds(despesa_fields.valor, despesa_fields.descricao);

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/create/transacao/despesa',
				method: 'POST',
				headers: {
					'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
				},
				contentType: 'application/json',
				dataType: 'json',
				data: JSON.stringify({
					valor: valor,
					descricao: descricao,
					resolvido: status,
					id_conta_bancaria: parseInt(conta_bancaria),
					id_categoria: parseInt(categoria)
				}),
				
				success: (res) => {
					sessionStorage.setItem('flash_message', `Despesa adicionada com sucesso!`);
					
					location.reload();
				},

				error: (xhr) => {
					response = xhr.responseJSON;
					console.log(response)
				}
			})
		}
	})

	$('#receita-submit').on('click', function () {
		receita_fields = fields.receita;
		
		let [ valor, descricao ] = get_fields_values(receita_fields.valor, receita_fields.descricao);
		let [ conta_bancaria, categoria ] = get_select_fields_id(receita_fields.contas_bancarias_select,
			receita_fields.categorias_select);
		let [ status ] = get_check_box_fields_values(receita_fields.status);

		is_error = !completed_fieds(receita_fields.valor, receita_fields.descricao);

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/create/transacao/receita',
				method: 'POST',
				headers: {
					'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
				},
				contentType: 'application/json',
				dataType: 'json',
				data: JSON.stringify({
					valor: valor,
					descricao: descricao,
					resolvido: status,
					id_conta_bancaria: parseInt(conta_bancaria),
					id_categoria: parseInt(categoria)
				}),
				
				success: (res) => {
					sessionStorage.setItem('flash_message', `Receita adicionada com sucesso!`);
					
					location.reload();
				},

				error: (xhr) => {
					response = xhr.responseJSON;
					console.log(response)
				}
			})
		}
	})

	$('#transferencia-submit').on('click', function () {
		transferencia_fields = fields.transferencia;
		
		let [ valor ] = get_fields_values(transferencia_fields.valor, transferencia_fields.descricao);
		let [ conta_destino, conta_origem ] = get_select_fields_id(
			transferencia_fields.contas_bancarias_destino_select,
			transferencia_fields.contas_bancarias_origem_select);

		is_error = !completed_fieds(transferencia_fields.valor);

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/create/transferencia',
				method: 'POST',
				headers: {
					'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
				},
				contentType: 'application/json',
				dataType: 'json',
				data: JSON.stringify({
					valor: valor,
					id_conta_bancaria_origem: parseInt(conta_origem),
					id_conta_bancaria_destino: parseInt(conta_destino)
				}),
				
				success: (res) => {
					sessionStorage.setItem('flash_message', `Transferência adicionada com sucesso!`);
					
					location.reload();
				},

				error: (xhr) => {
					response = xhr.responseJSON;
					show_error(transferencia_fields[response.target], response.msg);
				}
			})
		}
	})



	// $.ajax({
	// 	url: 'http://localhost:5000/api/list/contas-bancarias',
	// 	method: 'GET',
	// 	headers: {
	// 		'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
	// 	},
		
	// 	success: (res) => {
	// 		// Pegar somente os primeiros 4 elementos
	// 		let contas_bancarias = (JSON.parse(
	// 			JSON.stringify(res))).slice(0, 4)
			
	// 		for (conta of contas_bancarias) {
	// 			$('#contas-bancarias-resume').append(
	// 				criar_article_conta_bancaria(conta.id, conta.moeda, conta.instituicao, parseFloat(conta.saldo).toFixed(2))
	// 			);
	// 		}
	// 	}
	// })

	// $.ajax({
	// 	url: 'http://localhost:5000/api/list/categorias',
	// 	method: 'GET',
	// 	headers: {
	// 		'Authorization': 'Bearer ' + localStorage.getItem('x-sm-update-bearer-token')
	// 	},
		
	// 	success: (categorias) => {
	// 		for (cat of categorias) {
	// 			alert(cat)
	// 		}
	// 	}
	// })

	// $('#despesa-submit').on('click', function () {
	// 	despesa_fields = fields.despesa

	// 	let [ contas_bancarias_select, categorias_select, valor, foi_pago, descricao ] = get_validate(
	// 		despesa_fields.contas_bancarias_select,
	// 		despesa_fields.categorias_select,
	// 		despesa_fields.valor,
	// 		despesa_fields.status,
	// 		despesa_fields.descricao)

	// 	is_error = !completed_fieds(despesa_fields.valor, despesa_fields.descricao)

	// 	if (!is_error) {
	// 		$.ajax({
	// 			url: 'http://localhost:5000/api/create/'
	// 		})
	// 	}
	// })
})