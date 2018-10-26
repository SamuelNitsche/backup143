class Pool {
	constructor(id) {
		this.taskid = id;
	}
	
	get_pools() {
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		var p_html = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/pools",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				var p_pools = $(data).find('amount').text();
				if( p_pools > 0){
					p_html = p_html + "<table>";
					p_html = p_html + "<tr><th>Name</th><th>FileSystem</th><th>Host</th></tr>";
					$(data).find('pool').each(function(){
						var p_id = $(this).find('id').text();
						var p_name = $(this).find('name').text();
						var p_system = $(this).find('system').text();
						var p_host = $(this).find('host').text();
						p_html = p_html + "<tr onclick='var pool = new Pool(); pool.open_poolsettings(\""+String(p_id)+"\");'><td>" + p_name + "</td><td>" + p_system + "</td><td>" + p_host + "</td></tr>";
					});
				} else {
					p_html = p_html + "<h3>No Pools!</h3>";
				}
			}
		});
		return p_html;
	}
	
	get_poolinfo(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var p_id = "";
		var p_name = "";
		var p_system = "";
		var p_host = "";
		var p_port = "";
		var p_username = "";
		var p_password = "";
		var p_path = "";
		var p_ownerid = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/pools",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				$(data).find('pool').each(function(){
					if($(this).find('id').text() == id){
						p_id = $(this).find('id').text();
						p_name = $(this).find('name').text();
						p_system = $(this).find('system').text();
						p_host = $(this).find('host').text();
						p_port = $(this).find('port').text();
						p_username = $(this).find('username').text();
						p_password = $(this).find('password').text();
						p_path = $(this).find('path').text();
						p_ownerid = $(this).find('ownerid').text();
					}
				});
			}
		});
		return Array(p_id,p_name,p_system,p_host,p_port,p_username,p_password,p_path,p_ownerid);
	}
	
	open_poolsettings(id){
		var poolinfo = this.get_poolinfo(id);
		var html = "Name: <input type='text' id='pool_name' value='"+poolinfo[1]+"'/><br/>";
		html = html + "File System: <input type='text' id='pool_system' value='"+poolinfo[2]+"'/><br/>";
		html = html + "Host: <input type='text' id='pool_host' value='"+poolinfo[3]+"'/><br/>";
		html = html + "Port: <input type='text' id='pool_port' value='"+poolinfo[4]+"'/><br/>";
		html = html + "Username: <input type='text' id='pool_username' value='"+poolinfo[5]+"'/><br/>";
		html = html + "Password: <input type='text' id='pool_password' value='"+poolinfo[6]+"'/><br/>";
		html = html + "Path: <input type='text' id='pool_path' value='"+poolinfo[7]+"'/><br/>";
		html = html + "<button onclick='var pool = new Pool(); pool.delete_pool(\""+String(id)+"\");'>Delete</button><button onclick='var pool = new Pool(); pool.update_pool(\""+String(id)+"\");'>Update</button>";
		showpopup("Settings: "+poolinfo[1], html);
	}
	
	delete_pool(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/deletepool",
			dataType: "xml",
			async: false,
			data: { "id": id },
			xhrFields: { withCredentials:true },
			success: function(data) {
				showpopup("Success", "Successfully deleted Pool!");
				$('#js_backuplist').html(self.get_backups());
			}
		});
	}
	
	update_pool(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		
		var name = $('#pool_name').val();
		var system = $('#pool_system').val();
		var host = $('#pool_host').val();
		var port = $('#pool_port').val();
		var username = $('#pool_username').val();
		var password = $('#pool_password').val();
		var path = $('#pool_path').val();
		
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/updatepool",
			dataType: "xml",
			async: false,
			data: { "id": id, "name": name, "system": system, "host": host, "port": port, "username": username, "password": password, "path": path },
			xhrFields: { withCredentials:true },
			success: function(data) {
				showpopup("Success", "Successfully updated Pool!");
				$('#js_poollist').html(self.get_pools());
			}
		});
	}
	
}

$( document ).ready(function() {
	if ($("#js_poollist").length > 0){
		var pool = new Pool();
		$('#js_poollist').html(pool.get_pools());
	}
});