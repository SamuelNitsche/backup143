function updatecount() {
	var tasks = new Task();
	var taskcount = tasks.get_taskcount();
	$("#running h1").html(taskcount[0]);
	$("#waiting h1").html(taskcount[1]);
	$("#failed h1").html(taskcount[2]);
}
$( document ).ready(function() {
	updatecount();
});
setInterval(updatecount, 10000);