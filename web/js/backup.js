class Backup {
	
	get_backups() {
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		var b_html = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/backups",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					var b_backups = $(data).find('amount').text();
					if( b_backups > 0){
						b_html = b_html + "<table>";
						b_html = b_html + "<thead><tr><th>Source</th><th>Destination</th><th>Compare</th><th>Encryption</th><th>Compression</th></tr></thead>";
						$(data).find('backup').each(function(){
							var b_id = $(this).find('id').text();
							var b_pool_src = $(this).find('pool_src').text();
							var b_pool_dst = $(this).find('pool_dst').text();
							var b_compare = $(this).find('compare').text();
							var b_encrypt = $(this).find('encrypt').text();
							var b_compression = $(this).find('compression').text();
							
							var pool = new Pool();
							var srcpoolinfo = pool.get_poolinfo(b_pool_src);
							var dstpoolinfo = pool.get_poolinfo(b_pool_dst);
							
							if(b_encrypt == '0'){
								b_encrypt = 'inactive';
							} else {
								b_encrypt = 'active';
							}
							
							b_html = b_html + "<tr onclick='var backup = new Backup(); backup.open_backupsettings(\""+String(b_id)+"\");'><td>" + srcpoolinfo[1] + "</td><td>" + dstpoolinfo[1] + "</td><td>" + b_compare + "</td><td>" + b_encrypt + "</td><td>" + b_compression + "</td></tr>";
						});
					} else {
						b_html = b_html + "<h3>No Backups!</h3>";
					}
				} else {
					var error = $(data).find('message').text();
					return error;
				}
			}
		});
		return b_html;
	}
	
	get_backupinfo(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var b_id = "";
		var b_pool_src = "";
		var b_pool_dst = "";
		var b_compare = "";
		var b_encrypt = "";
		var b_compression = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/backups",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					$(data).find('backup').each(function(){
						if($(this).find('id').text() == id){
							b_id = $(this).find('id').text();
							b_pool_src = $(this).find('pool_src').text();
							b_pool_dst = $(this).find('pool_dst').text();
							b_compare = $(this).find('compare').text();
							b_encrypt = $(this).find('encrypt').text();
							b_compression = $(this).find('compression').text();
						}
					});
				} else {
					var error = $(data).find('message').text();
					return error;
				}
			}
		});
		return Array(b_id,b_pool_src,b_pool_dst,b_compare,b_encrypt,b_compression);
	}
	
	open_backupsettings(id){
		var backupinfo = this.get_backupinfo(id);
        var html = "<table style='width:100%;'>";
        html = html + "<tr><td><label>Source Pool: </label></td><td><select id='backup_pool_src'>";
        var pool = new Pool();
        html = html + pool.get_pooldropdown();
        html = html + "</select></td></tr>";
        html = html + "<tr><td><label>Destination Pool: </label></td><td><select id='backup_pool_dst'>";
        var pool = new Pool();
        html = html + pool.get_pooldropdown();
        html = html + "</select></td></tr>";
		html = html + "<tr><td><label>Compare: </label></td><td><select id='backup_compare'>";
        html = html + "<option value='hash'>Hash</option>";
        html = html + "<option value='binary'>Binary</option>";
        html = html + "</select></td></tr>";
		html = html + "<tr><td><label>Encrypt: </label></td><td><select id='backup_encrypt'>";
        html = html + "<option value='0'>deactivated</option>";
        html = html + "<option value='1'>activated</option>";
        html = html + "</select></td></tr>";
		html = html + "<tr><td><label>Compression: </label></td><td><select id='backup_compression'>";
        html = html + "<option value='none'>None</option>";
        html = html + "<option value='zip'>ZIP</option>";
        html = html + "<option value='tar'>TAR</option>";
        html = html + "</select></td></tr>";
		html = html + "<tr><td><button class='danger' onclick='var backup = new Backup(); backup.delete_backup(\""+String(id)+"\");'>Delete</button></td><td><button class='default' onclick='var backup = new Backup(); backup.update_backup(\""+String(id)+"\");'>Update</button></td></tr>";
        html = html + "</table>";
        var task = new Task();
        html = html + task.get_taskbybackup(id);
        showpopup("Settings", html);
        $("#backup_pool_src").val(backupinfo[1]);
        $("#backup_pool_dst").val(backupinfo[2]);
        $("#backup_compare").val(backupinfo[3]);
        $("#backup_encrypt").val(backupinfo[4]);
        $("#backup_compression").val(backupinfo[5]);
	}
	
	delete_backup(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
        
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/deletebackup",
			dataType: "xml",
			async: false,
			data: { "id": id },
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					showpopup("Success", "Successfully deleted Backup!");
					$('#js_backuplist').html(self.get_backups());
				} else {
					var error = $(data).find('message').text()
					showpopup("ERROR", error);
				}
			}
		});
	}
	
	update_backup(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		
		var pool_src = $('#backup_pool_src').val();
		var pool_dst = $('#backup_pool_dst').val();
		var compare = $('#backup_compare').val();
		var encrypt = $('#backup_encrypt').val();
		var compression = $('#backup_compression').val();
		
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/updatebackup",
			dataType: "xml",
			async: false,
			data: { "id": id, "pool_src": pool_src, "pool_dst": pool_dst, "compare": compare, "encrypt": encrypt, "compression": compression },
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					showpopup("Success", "Successfully updated Backup!");
					$('#js_backuplist').html(self.get_backups());
				} else {
					var error = $(data).find('message').text()
					showpopup("ERROR", error);
				}
			}
		});
	}
    
    create_backup(){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		
		var pool_src = $('#backup_pool_src').val();
		var pool_dst = $('#backup_pool_dst').val();
		var compare = $('#backup_compare').val();
		var encrypt = $('#backup_encrypt').val();
		var compression = $('#backup_compression').val();
		
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/createbackup",
			dataType: "xml",
			async: false,
			data: { "pool_src": pool_src, "pool_dst": pool_dst, "compare": compare, "encrypt": encrypt, "compression": compression },
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					showpopup("Success", "Successfully created Backup!");
					$('#js_backuplist').html(self.get_backups());
				} else {
					var error = $(data).find('message').text()
					showpopup("ERROR", error);
				}
			}
		});
	}
    
    createpopup(){
        var html = "<table style='width:100%;'>";
		html = html + "<tr><td><label>Source Pool: </label></td><td><select id='backup_pool_src'>";
        var pool = new Pool();
        html = html + pool.get_pooldropdown();
        html = html + "</select></td></tr>";
		html = html + "<tr><td><label>Destination Pool: </label></td><td><select id='backup_pool_dst'>";
        var pool = new Pool();
        html = html + pool.get_pooldropdown();
        html = html + "</select></td></tr>";
		html = html + "<tr><td><label>Compare: </label></td><td><select id='backup_compare'>";
        html = html + "<option value='hash'>Hash</option>";
        html = html + "<option value='binary'>Binary</option>";
        html = html + "</select></td></tr>";
		html = html + "<tr><td><label>Encrypt: </label></td><td><select id='backup_encrypt'>";
        html = html + "<option value='0'>deactivated</option>";
        html = html + "<option value='1'>activated</option>";
        html = html + "</select></td></tr>";
		html = html + "<tr><td><label>Compression: </label></td><td><select id='backup_compression'>";
        html = html + "<option value='none'>None</option>";
        html = html + "<option value='zip'>ZIP</option>";
        html = html + "<option value='tar'>TAR</option>";
        html = html + "</select></td></tr>";
        html = html + "<tr><td><button class='default' onclick='var backup = new Backup(); backup.create_backup();'>Create</button></td></tr>";
        showpopup("Create Backup", html);
    }
	
}

$( document ).ready(function() {
	if ($("#js_backuplist").length > 0){
		var pool = new Backup();
		$('#js_backuplist').html(pool.get_backups());
	}
});