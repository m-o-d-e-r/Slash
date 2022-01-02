var menu__closed = true;

$('document').ready(function () {
	$('.menu_btn').on('click', function (e) {
		menu__closed = !menu__closed;
		e.preventDefault;
		$(this).toggleClass('menu_btn_acttiv');
		$('.menu_nav').toggleClass('nav_acttiv');

		if (menu__closed)
		{
			$('.header').css('grid-template-columns', '95% 5%')
			$('.menu').css('grid-template-columns', '100% 0%');
			$('.nav__ > a').css('display', "none");
		} else {
			$('.header').css('grid-template-columns', '65% 35%');
			$('.menu').css('grid-template-columns', '10% 90%');
			$('.nav__ > a').css('display', "block");
		}
	});
});