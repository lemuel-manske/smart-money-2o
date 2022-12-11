jQuery(function($) {

	remover_erros();
	
	check_flash_message();

	$('#conta-bancaria-submit').on('click', function () {
		conta_bancaria_fields = DASHBOARD_FIELDS.conta_bancaria;

		let [ nome, saldo ] = get_fields_values(conta_bancaria_fields.nome, conta_bancaria_fields.saldo)
		let [ instituicao ] = get_select_fields_values(conta_bancaria_fields.instituicao_select)

		is_error = !completed_fieds(conta_bancaria_fields.saldo, conta_bancaria_fields.nome)

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/create/conta-bancaria',
				method: 'POST',
				xhrFields: {
					withCredentials: true
				},
				headers: {
					'X-CSRF-TOKEN':getCookie('csrf_access_token')
				},
				contentType: 'application/json',
				dataType: 'json',
				data: JSON.stringify({
					nome: nome,
					saldo: saldo,
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
		despesa_fields = DASHBOARD_FIELDS.despesa;
		
		let [ valor, descricao ] = get_fields_values(despesa_fields.valor, despesa_fields.descricao);
		let [ conta_bancaria, categoria ] = get_select_fields_id(despesa_fields.contas_bancarias_select,
			despesa_fields.categorias_select);
		let [ status ] = get_check_box_fields_values(despesa_fields.status);
		
		is_error = !completed_fieds(despesa_fields.valor, despesa_fields.descricao);

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/create/transacao/despesa',
				method: 'POST',
				xhrFields: {
					withCredentials: true
				},
				headers: {
					'X-CSRF-TOKEN':getCookie('csrf_access_token')
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
		receita_fields = DASHBOARD_FIELDS.receita;
		
		let [ valor, descricao ] = get_fields_values(receita_fields.valor, receita_fields.descricao);
		let [ conta_bancaria, categoria ] = get_select_fields_id(receita_fields.contas_bancarias_select,
			receita_fields.categorias_select);
		let [ status ] = get_check_box_fields_values(receita_fields.status);

		is_error = !completed_fieds(receita_fields.valor, receita_fields.descricao);

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/create/transacao/receita',
				method: 'POST',
				xhrFields: {
					withCredentials: true
				},
				headers: {
					'X-CSRF-TOKEN':getCookie('csrf_access_token')
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
		transferencia_fields = DASHBOARD_FIELDS.transferencia;
		
		let [ valor ] = get_fields_values(transferencia_fields.valor, transferencia_fields.descricao);
		let [ conta_destino, conta_origem ] = get_select_fields_id(
			transferencia_fields.contas_bancarias_destino_select,
			transferencia_fields.contas_bancarias_origem_select);

		is_error = !completed_fieds(transferencia_fields.valor);

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/create/transferencia',
				method: 'POST',
				xhrFields: {
					withCredentials: true
				},
				headers: {
					'X-CSRF-TOKEN':getCookie('csrf_access_token')
				},
				contentType: 'application/json',
				dataType: 'json',
				data: JSON.stringify({
					valor: valor,
					id_conta_bancaria_origem: parseInt(conta_origem),
					id_conta_bancaria_destino: parseInt(conta_destino)
				}),
				
				success: (res) => {
					sessionStorage.setItem('flash_message', 'Transferência adicionada com sucesso!');
					
					location.reload();
				},

				error: (xhr) => {
					response = xhr.responseJSON;
					show_error(transferencia_fields[response.target], response.msg);
				}
			})
		}
	})

	$('#logout').on('click', function () {
		$.ajax({
			url: 'http://localhost:5000/api/user/logout',
			method: 'GET',
			xhrFields: {
				withCredentials: true
			},
			headers: {
				'X-CSRF-TOKEN':getCookie('csrf_access_token')
			},
			
			success: (res) => {
				location.reload()
			}
		})
	})
})