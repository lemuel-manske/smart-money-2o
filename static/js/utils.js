function get_fields_values(...fields) {
	return fields.map((id) => $(id).val());
}

function get_select_fields_values(...fields) {
	return fields.map((id) => $(`${id} option:selected`).attr('value'));
}

function get_select_fields_id(...fields) {
	return fields.map((id) => $(`${id} option:selected`).attr('id'));
}

function get_check_box_fields_values(...fields) {
	return fields.map((id) => $(`${id}`).is(':checked'));
}

function show_error(field, msg) {
	$(field).toggleClass('is-invalid', true);
	$(field).parent().toggleClass('is-invalid', true);
	$(field + '-erro').text(msg);
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

function remover_erros() {
	$('.form-control').on('input', function() {
		$(this).removeClass('is-invalid');
	});
	$('.form-floating').on('input', function() {
		$(this).removeClass('is-invalid');
	});
	$('select').on('change', function() {
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

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
}

function set_user_moeda() {
	$.ajax({
		url: 'http://localhost:5000/api/user/minha-conta',
		method: 'GET',
		

		success: (res) => {
			localStorage.setItem('moeda', res.msg.moeda)
		}
	})
}