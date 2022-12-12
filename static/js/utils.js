function getFieldsValues(...fields) {
	return fields.map((id) => $(id).val());
}

function getSelectFieldsValues(...fields) {
	return fields.map((id) => $(`${id} option:selected`).attr('value'));
}

function getSelectFieldsId(...fields) {
	return fields.map((id) => $(`${id} option:selected`).attr('id'));
}

function getCheckBoxFieldsValues(...fields) {
	return fields.map((id) => $(`${id}`).is(':checked'));
}

function showError(field, msg) {
	$(field).toggleClass('is-invalid', true);
	$(field).parent().toggleClass('is-invalid', true);
	$(field + '-erro').text(msg);
}

function completedFields(...fields) {
	let tmp = true;
	for (let field of fields) {
		if (!$(field).val()) {
			showError(field, 'Preencha o campo.');
			tmp = false;
		}
	}
	return tmp;
}

function removeErrors() {
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

function checkFlashMessage() {
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

function setMoeda() {
	$.ajax({
		url: 'http://localhost:5000/api/user/minha-conta',
		method: 'GET',
		
		success: (res) => {
			localStorage.setItem('moeda', res.msg.moeda)
		}
	})
}