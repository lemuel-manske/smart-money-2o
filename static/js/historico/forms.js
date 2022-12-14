jQuery(function($) {
	$(document.body).on('click', '.excluir-transacao', function () {
		let transacao_id = $(this).closest('tr').find('th').attr('id');

		$.ajax({
			url: 'http://localhost:5000/api/delete/transacao',
			method: 'DELETE',
			xhrFields: {
				withCredentials: true
			},
			headers: {
				'X-CSRF-TOKEN':getCookie('csrf_access_token')
			},

			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify({
				id_transacao: parseInt(transacao_id)
			}),

			success: (res) => {
				location.reload()
			},

			error: (xhr) => {
				response = xhr.responseJSON;
				console.log(response);
			}
		})
	})
	
	$(document.body).on('click', '.efetuar-resolver', function () {
		let transacao_id = $(this).closest('tr').find('th').attr('id');
		
		$.ajax({
			url: 'http://localhost:5000/api/create/transacao/realizar',
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
				id_transacao: parseInt(transacao_id)
			}),
			
			success: (res) => {
				location.reload()
			},
			
			error: (xhr) => {
				response = xhr.responseJSON;
				console.log(response);
			}
		})
	})

	$(document.body).on('click', '.excluir-transferencia', function () {
		let transferencia_id = $(this).closest('tr').find('th').attr('id');
	
		$.ajax({
			url: 'http://localhost:5000/api/delete/transferencia',
			method: 'DELETE',
			xhrFields: {
				withCredentials: true
			},
			headers: {
				'X-CSRF-TOKEN':getCookie('csrf_access_token')
			},
	
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify({
				id_transferencia: parseInt(transferencia_id)
			}),
	
			success: (res) => {
				location.reload()
			},
	
			error: (xhr) => {
				response = xhr.responseJSON;
				console.log(response);
			}
		})
	})

	$(document.body).on('click', '.excluir-conta-bancaria', function () {
		let conta_id = $(this).closest('tr').find('th').attr('id');
	
		$.ajax({
			url: 'http://localhost:5000/api/delete/conta-bancaria',
			method: 'DELETE',
			xhrFields: {
				withCredentials: true
			},
			headers: {
				'X-CSRF-TOKEN':getCookie('csrf_access_token')
			},
	
			contentType: 'application/json',
			dataType: 'json',
			data: JSON.stringify({
				id_conta_bancaria: parseInt(conta_id)
			}),
	
			success: (res) => {
				location.reload()
			},
	
			error: (xhr) => {
				response = xhr.responseJSON;
				console.log(response);
			}
		})
	})
})