 toggleChevron = function(e) {
$(e.target)
		.prev('.panel-heading')
		.find("i.indicator")
		.toggleClass('fa-caret-down fa-caret-right');
};

$().ready(
	function(){
		$('#accordion').on('hidden.bs.collapse', toggleChevron);
		$('#accordion').on('shown.bs.collapse', toggleChevron);
	});

		