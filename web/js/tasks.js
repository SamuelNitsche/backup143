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
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					var t_running = $(data).find('running').text();
					if( t_running > 0){
						t_html = t_html + "<h3>" + t_running + " active tasks</h3>";
						t_html = t_html + "<table>";
						t_html = t_html + "<tr><th>Taskname</th><th>Action</th><th>State</th><th></th></tr>";
						$(data).find('task').each(function(){
							var t_id = $(this).find('id').text();
							var t_name = $(this).find('name').text();
							var t_action = $(this).find('action').text();
							var t_state = $(this).find('state').text();
							if(t_state == "running"){
								var taskinfo = self.get_taskinfo(t_id);
								t_html = t_html + "<tr onclick='var task = new Task(); task.get_tasklog("+t_id+");'><td>" + t_name + "</td><td>" + t_action + "</td><td>" + t_state + "</td><td><i class='fa fa-spinner fa-spin'></i></td></tr>";
							}
						});
					} else {
						t_html = t_html + "<h3>No running tasks!</h3>";
					}
				} else {
					var error = $(data).find('message').text();
					t_html = error;
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
		var t_state = "";
		var t_backupid = "";
		var t_backuptyp = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/tasks",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					$(data).find('task').each(function(){
						if($(this).find('id').text() == id){
							t_id = $(this).find('id').text();
							t_name = $(this).find('name').text();
							t_action = $(this).find('action').text();
							t_schedule = $(this).find('schedule').text();
							t_last_run = $(this).find('last_run').text();
							t_state = $(this).find('state').text();
							t_backupid = $(this).find('backupid').text();
							t_backuptyp = $(this).find('backuptyp').text();
						}
					});
				} else {
					var error = $(data).find('message').text();
					return error;
				}
			}
		});
		return Array(t_id,t_name,t_action,t_schedule,t_last_run,t_state,t_backupid,t_backuptyp);
	}
    
	open_backuptasksettings(id){
		var taskinfo = this.get_taskinfo(id);
        var html = "<table style='width:100%;'>";
		html = html + "<tr><td><label>Name: </label></td><td><input type='text' id='task_name' value='"+taskinfo[1]+"'/></td></tr>";
		html = html + "<tr><td><label>Backuptyp: </label></td><td><input type='text' id='task_backuptyp' value='"+taskinfo[7]+"'/></td></tr>";
        var schedule = taskinfo[3].split(' ');
        if(schedule[0].length < 2){
            schedule[0] = "0" + schedule[0];
        }
        if(schedule[1].length < 2){
            schedule[1] = "0" + schedule[1];
        }
		html = html + "<tr><td><label>Time: </label></td><td><input type='time' id='task_time' value='"+schedule[1]+":"+schedule[0]+"'/></td></tr>";
        html = html + "</table>";
        html = html + "<table style='text-align:center; width:100%;'>";
        html = html + "<tr><th>MON</th><th>TUE</th><th>WED</th><th>THU</th><th>FRI</th><th>SAT</th><th>SUN</th></tr>";
        html = html + "<tr><td><input type='checkbox' name='task_days' value='1'></td><td><input type='checkbox' name='task_days' value='2'></td><td><input type='checkbox' name='task_days' value='3'></td><td><input type='checkbox' name='task_days' value='4'></td><td><input type='checkbox' name='task_days' value='5'></td><td><input type='checkbox' name='task_days' value='6'></td><td><input type='checkbox' name='task_days' value='7'></td></tr>";
        html = html + "</table>";
		html = html + "<button class='danger' onclick='var task = new Task(); task.delete_backuptask(\""+String(id)+"\");'>Delete</button><button class='default' onclick='var task = new Task(); task.update_backuptask(\""+String(id)+"\");'>Update</button>";
        showpopup("Settings: "+taskinfo[1], html);
        var days = schedule[4].split(',');
        days.forEach(function(item){
            $(':checkbox[value='+item+']').prop('checked', true);
        });
	}
    
    delete_backuptask(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/deletetask",
			dataType: "xml",
			async: false,
			data: { "id": id },
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					showpopup("Success", "Successfully deleted Task!");
					$('#js_poollist').html(self.get_pools());
				} else {
					var error = $(data).find('message').text()
					showpopup("ERROR", error);
				}
			}
		});
	}
    
	update_backuptask(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		
		var name = $('#task_name').val();
		var backuptyp = $('#task_backuptyp').val();
		var time = $('#task_time').val();
        var daylist = "";
		var days = document.getElementsByName('task_days');
        for (var i=0, n=days.length;i<n;i++){
            if (days[i].checked){
                daylist += ","+days[i].value;
            }
        }
        if (daylist) daylist = daylist.substring(1);
        
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/updatetask",
			dataType: "xml",
			async: false,
			data: { "id": id, "name": name, "backuptyp": backuptyp, "time": time, "days": daylist },
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					showpopup("Success", "Successfully updated Task!");
					$('#js_backuplist').html(self.get_backups());
				} else {
					var error = $(data).find('message').text();
					showpopup("ERROR", error);
				}
			}
		});
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
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					t_html = t_html + "<table>";
					$(data).find('message').each(function(){
						t_html = t_html + "<tr><td>" + $(this).find('datetime').text() + "</td><td>" + $(this).find('value').text() + "</td>";
					});
					t_html = t_html + "</table>"; 
				} else {
					var error = $(data).find('message').text();
					t_html = error;
				}
			}
		});
	showpopup("Logs",t_html);
	}
    
    get_taskbybackup(backupid){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
        var t_html = "";
    
        $.ajax({
            type: "post",
            url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/backuptasks",
            dataType: "xml",
            async: false,
            data: { "id": backupid },
            xhrFields: { withCredentials:true },
            success: function(data) {
                var apistatus = $(data).find('status').text();
                if(apistatus == "OK"){
                    t_html = t_html + "<h1>Tasks <span class='addbtn' onclick='var task = new Task(); task.createbackuppopup("+ backupid +");'>+</span></h1>";
                    t_html = t_html + "<table style='width:100%; text-align:center;'>";
                    t_html = t_html + "<tr><th>Name</th><th>Schedule</th><th>State</th></tr>";
                    $(data).find('task').each(function(){
                        t_html = t_html + "<tr onclick='task = new Task(); task.open_backuptasksettings(\"" + $(this).find('id').text() + "\")'><td>" + $(this).find('name').text() + "</td><td>" + $(this).find('schedule').text() + "</td><td>" + $(this).find('state').text() + "</td></tr>";
                    });
                    t_html = t_html + "</table>"; 
                } else {
                    var error = $(data).find('message').text();
                    t_html = error;
                }
            }
        });
        return t_html;
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
                var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					running = $(data).find('running').text();
					waiting = $(data).find('waiting').text();
					failed = $(data).find('failed').text();
				} else {
					var error = $(data).find('message').text();
					return error;
				}
			}
		});
		return Array(running, waiting, failed);
	}
    
    create_backuptask(){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		
		var name = $('#task_name').val();
		var action = 'backup';
        var backupid = $('#task_backupid').val();
		var backuptyp = $('#task_backuptyp').val();
		var time = $('#task_time').val();
        var daylist = "";
		var days = document.getElementsByName('task_days');
        for (var i=0, n=days.length;i<n;i++){
            if (days[i].checked){
                daylist += ","+days[i].value;
            }
        }
        if (daylist) daylist = daylist.substring(1);
		
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/createtask",
			dataType: "xml",
			async: false,
			data: { "name": name, "action": action, "backupid": backupid, "backuptyp": backuptyp, "time": time, "days": daylist },
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					showpopup("Success", "Successfully created Task!");
					$('#js_backuplist').html(self.get_backups());
				} else {
					var error = $(data).find('message').text()
					showpopup("ERROR", error);
				}
			}
		});
	}
    
    createbackuppopup(type, backupid=0){
        var html = "<table style='width:100%;'>";
        html = html + "<tr><td><label>Name: </label></td><td><input type='text' id='task_name'/></td></tr>";
        html = html + "<input type='hidden' id='task_backupid' value='"+backupid+"'/>";
        html = html + "<tr><td><label>Backuptyp: </label></td><td><input type='text' id='task_backuptyp'/></td></tr>";
        html = html + "<tr><td><label>Time: </label></td><td><input type='time' id='task_time'/></td></tr>";
        html = html + "</table>";
        html = html + "<br/>";
        html = html + "<table style='text-align:center; width:100%;'>";
        html = html + "<tr><th>MON</th><th>TUE</th><th>WED</th><th>THU</th><th>FRI</th><th>SAT</th><th>SUN</th></tr>";
        html = html + "<tr><td><input type='checkbox' name='task_days' value='1'></td><td><input type='checkbox' name='task_days' value='2'></td><td><input type='checkbox' name='task_days' value='3'></td><td><input type='checkbox' name='task_days' value='4'></td><td><input type='checkbox' name='task_days' value='5'></td><td><input type='checkbox' name='task_days' value='6'></td><td><input type='checkbox' name='task_days' value='7'></td></tr>";
        html = html + "</table>";
        html = html + "<br/>";
        html = html + "<br/>";
        html = html + "<button class='default' onclick='var task = new Task(); task.create_backuptask();'>Create</button>";
        html = html + "<br/>";
        html = html + "<br/>";
        html = html + "<b>NOTE</b> For incremental and differential you should plan 1 additional Full Backup!";
        showpopup("Create Backuptask", html);
    }
}