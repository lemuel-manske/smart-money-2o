function get_fields_values(...fields) {
	return fields.map((id) => $(id).val());
}

function showError(field, msg) {
	$(field).toggleClass('is-invalid', true);
	$(field).parent().toggleClass('is-invalid', true);
	$(field + '-erro').text(msg);
}

function showSuperError(id, msg) {
	$(id).text(msg);
}

function completed_fieds(...fields) {
	let tmp = true;
	for (let field of fields) {
		if (!$(field).val()) {
			showError(field, 'Preencha o campo.');
			tmp = false;
		}
	}
	return tmp;
}

function cleanErrors() {
	$('.form-control').on('input', function() {
		$(this).removeClass('is-invalid');
	});
	$('.form-floating').on('input', function() {
		$(this).removeClass('is-invalid');
	});
}