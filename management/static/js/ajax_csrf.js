$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		var csrftoken = $.cookie('csrftoken');
		xhr.setRequestHeader('X-CSRFToken', csrftoken);
	}
});
