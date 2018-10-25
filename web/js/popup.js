function showpopup (title, content){
	$("#popup").show();
	$("#popup-content").html("<h2>"+title+"</h2><br/>"+content);
}
$(document).click(function(e) {
	var $target = $(e.target);
	var popup = $("#popup");
	var popupBackground = $("#popup-bg");
	if ($target.is(popupBackground)) {
		popup.hide();
	}
});