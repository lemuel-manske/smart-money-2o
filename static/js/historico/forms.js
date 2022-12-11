jQuery(function($) {
	$(document.body).on('click', '.excluir-transacao', function () {
		let transacao_id = $(this).closest('tr').find('th').attr('id');
		
		console.log(transacao_id)

		// ajax
	})
})