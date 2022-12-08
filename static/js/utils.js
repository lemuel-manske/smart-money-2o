function get_fields_values(...fields) {
	return fields.map((id) => $(id).val());
}

function get_select_fields_values(...fields) {
	return fields.map((id) => $(`${id} option:selected`).attr('value'));
}

function show_error(field, msg) {
	$(field).toggleClass('is-invalid', true);
	$(field).parent().toggleClass('is-invalid', true);
	$(field + '-erro').text(msg);
}

function show_super_error(id, msg) {
	$(id).text(msg);
}

function completed_fieds(...fields) {
	let tmp = true;
	for (let field of fields) {
		if (!$(field).val()) {
			show_error(field, 'Preencha o campo.');
			tmp = false;
		}
	}
	return tmp;
}

function clean_errors() {
	$('.form-control').on('input', function() {
		$(this).removeClass('is-invalid');
	});
	$('.form-floating').on('input', function() {
		$(this).removeClass('is-invalid');
	});
}

function check_flash_message() {
	if (sessionStorage.getItem('flash_message')) {
		let flash_message = sessionStorage.getItem('flash_message');

		$('.toast-body').append(flash_message);

		let toast = new bootstrap.Toast(document.getElementById('flash-message'))
		toast.show()
		
		sessionStorage.removeItem('flash_message')
	}
}