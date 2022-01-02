$('document').ready(function () {
	$('.left').on('click', function (e) {
		e.preventDefault;
		$('.canvSettings').toggleClass('canvSettingsActive');
	});

	$('.admin').on('click', function (e) {
		e.preventDefault;
		$('.letter_for_admin').toggleClass('letter_for_adminActive');
	});
});