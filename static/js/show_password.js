jQuery(function($) {
	$(".toggle-visibility-button").on("click", function() {
		let type = ($(this).is(':checked') ? 'text' : 'password');
		let campo = $('.form').find('.toggle-visibility');

		campo.attr('type', type);
	});
})