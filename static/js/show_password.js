jQuery(function($) {
	$(".toggle-visibility-button").on("click", function() {
		let type = ($(this).is(':checked') ? 'text' : 'password');
		let campo = $(this).closest('.show-password-group').find('.toggle-visibility');

		campo.attr('type', type);
	});
})