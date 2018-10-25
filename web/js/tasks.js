class Task {
	constructor(id) {
		this.taskid = id;
	}
	
	get_runningtasks() {
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		var t_html = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/tasks",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				var t_running = $(data).find('running').text();
				if( t_running > 0){
					t_html = t_html + "<h3>" + t_running + " active tasks</h3>";
					t_html = t_html + "<table>";
					t_html = t_html + "<tr><th>Taskname</th><th>Action</th><th>Status</th><th></th></tr>";
					$(data).find('task').each(function(){
						var t_id = $(this).find('id').text();
						var t_name = $(this).find('name').text();
						var t_action = $(this).find('action').text();
						var t_status = $(this).find('status').text();
						if(t_status == "running"){
							var taskinfo = self.get_taskinfo(t_id);
							//alert(JSON.stringify(JSON.stringify(JSON.stringify(taskinfo, null, 4)), null, 4), null, 4);
							t_html = t_html + "<tr onclick='var task = new Task(); task.get_tasklog("+t_id+");'><td>" + t_name + "</td><td>" + t_action + "</td><td>" + t_status + "</td><td><i class='fa fa-spinner fa-spin'></i></td></tr>";
						}
					});
				} else {
					t_html = t_html + "<h3>No running tasks!</h3>";
				}
			}
		});
		return t_html;
	}
	
	get_taskinfo(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var t_id = "";
		var t_name = "";
		var t_action = "";
		var t_schedule = "";
		var t_last_run = "";
		var t_planned_time = "";
		var t_status = "";
		var t_backupid = "";
		var t_onetime = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/tasks",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				$(data).find('task').each(function(){
					if($(this).find('id').text() == id){
						t_id = $(this).find('id').text();
						t_name = $(this).find('name').text();
						t_action = $(this).find('action').text();
						t_schedule = $(this).find('schedule').text();
						t_last_run = $(this).find('last_run').text();
						t_planned_time = $(this).find('planned_time').text();
						t_status = $(this).find('status').text();
						t_backupid = $(this).find('backupid').text();
						t_onetime = $(this).find('onetime').text();
					}
				});
			}
		});
		return Array(t_id,t_name,t_action,t_schedule,t_last_run,t_planned_time,t_status,t_backupid,t_onetime);
	}
	
	get_tasklog(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var t_html = "";
		
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/tasklog",
			dataType: "xml",
			async: false,
			data: { "id": id },
			xhrFields: { withCredentials:true },
			success: function(data) {
				t_html = t_html + "<table>";
				$(data).find('message').each(function(){
					t_html = t_html + "<tr><td>" + $(this).find('datetime').text() + "</td><td>" + $(this).find('value').text() + "</td>";
				});
				t_html = t_html + "</table>"; 
			}
		});
	showpopup("Logs",t_html);
	}
	
	get_taskcount(){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var running = "";
		var waiting = "";
		var failed = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/tasks",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				running = $(data).find('running').text();
				waiting = $(data).find('waiting').text();
				failed = $(data).find('failed').text();
			}
		});
		
		return Array(running, waiting, failed);
	}
}