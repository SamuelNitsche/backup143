function slide() {
	$('#tasks-wrap #hidden-div').slideToggle({
	  direction: "up"
	}, 300);
	$(this).toggleClass('clientsClose');
}
function updatelist() {
	var tasks = new Task();
	$("#tasks-content").html(tasks.get_runningtasks());
}
$( document ).ready(function() {
	updatelist();
});
setInterval(updatelist, 10000);
