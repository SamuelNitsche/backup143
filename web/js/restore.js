class Restore {
    get_tasksdropdown(){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
        
        var p_html = "";
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
                        if($(this).find('action').text() == "backup"){
                            p_html = p_html + "<option value='"+$(this).find('id').text()+"'>"+$(this).find('name').text()+"</option>";
                        }
					});
				} else {
					var error = $(data).find('message').text();
					return error;
				}
			}
		});
		return p_html;
    }
    
    get_backupfiledropdown(taskid){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
        
        var p_html = "";
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/backupfileslistbytask",
			dataType: "xml",
			async: false,
            data: { "taskid": taskid },
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					$(data).find('backupfile').each(function(){
                        p_html = p_html + "<option value='"+$(this).find('id').text()+"'>"+$(this).find('date').text()+"</option>";
					});
				} else {
					var error = $(data).find('message').text();
					return error;
				}
			}
		});
		return p_html;
    }
}

$(document).ready(function () {
    var task = new Task();
    task.createrestorediv();
	$('#js_restorelist').html(task.get_restores());
    var active = $('#task_taskid').val();
    var restore = new Restore();
    $("#task_backupfilesid").html(restore.get_backupfiledropdown(active));
    $("#task_taskid").change(function () {
        var val = $(this).val();
        var restore = new Restore();
        $("#task_backupfilesid").html(restore.get_backupfiledropdown(val));
    });
});